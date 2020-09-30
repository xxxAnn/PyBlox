"""
`Groups` is the main module for managing interactions with the group API

Contents:
    `BloxGroup`: `BloxType`

Requires:
    `Errors`: `*`
    `Base`: `BloxType`
    `User`: `BloxUser`
    `Ranks`: `BloxRank`
    `Settings`: `BloxSettings`
    `Member`: `BloxMember`
    `.utils`: `Url`

The following code is provided with: 

    The MIT License (MIT)

    Copyright (c) Kyando 2020

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json
import time

from .Errors import *
from .Base import BloxType
from .User import BloxUser
from .Ranks import BloxRank
from .Settings import BloxSettings
from .Member import BloxMember
from .utils import Url


class BloxGroup(BloxType):
    """
    A handler for a roblox group

    Attrs:
        `id`
        `roles`

    Fetchables:
        `join_requests`
        `name`
        `members`

    Meths:
        async `fetch`:
            >> name = await group.fetch("name") # where `group` is a BloxGroup

    Fetched users *will* be added to cache when using async meth `fetch`
    Attr `roles` will be deprecated in 1.1 in favor of Fetchable `roles`
    """
    def __init__(self, client, group_id, roles):
        super().__init__(client)
        self.id = str(group_id)
        self.roles = roles
        self.can_fetch("join_requests", "members", "name")

    def __str__(self):
        if self.name:
            return self.name
        raise AttributeNotFetched("name")
    
    async def fetch_name(self):
        hook = await Url("groups", "/v1/groups/%id%", id=self.id).get()

        name = hook.json.get("name", None)
        
        if name == None:
            raise PyBloxException(
                "Group name was not found"
                )

        return name

    async def _cvrt_dict_blox_member(self, list):
        real_list = []
        for user_dict in list:
            real_list.append(BloxMember(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username"), group=self))

        return real_list

    async def get_role(self, name: str):
        """
        Returns a BloxRank with the given name
        """
        hook = await Url("groups", "/v1/groups/%id%/roles", id=self.id).get()
        
        data = hook.json
        roles = data.get("roles")

        for bucket in roles:
            if bucket.get("name") == name:
                return BloxRank(payload=bucket, group=self)

    async def get_member(self, username: str):
        user = await self.client.get_user(username)
        return BloxMember(client=self.client, user_id=user.id, username=username, group=self)

    async def fetch_members(self):
        """
        Returns a list of all the group's members
        """
        list_members = []

        access = Url("groups", "/v1/groups/%id%/users?sortOrder=Asc&limit=100", id=self.id)

        hook = await access.get()

        def create_members(group, list):

            result_list = []

            for user_info_dict in list:
                user_dict = user_info_dict.get("user")
                result_list.append(BloxMember(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username"), group=group))

            return result_list

        data = hook.json
        list_members.extend(create_members(self, data.get("data")))

        done = False

        next_page = data.get("nextPageCursor")
        
        while not done:

            if not isinstance(next_page, str):
                done = True
                continue

            data = await access.get()
            data = data.json
            next_page = data.get("nextPageCursor")
            list_members.extend(create_members(self, data.get("data")))
        
        return list_members

    async def fetch_join_requests(self):
        """
        Returns a list of users that request to join the group
        """
        if not self.settings.is_approval_required:
            raise PyBloxException(
                "This group isn't approval required and has no join requests"
                )

        list_members = []

        access = Url("groups", "/v1/groups/%id%/users?sortOrder=Asc&limit=100", id=self.id)

        def create_users(list):

            result_list = []

            for user_info_dict in list:
                user_dict = user_info_dict.get("requester")
                result_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username")))

            return result_list

        data = await access.get()
        data = data.json
        list_members.extend(create_users(data.get("data")))

        done = False

        next_page = data.get("nextPageCursor")
        
        while not done:

            if not isinstance(next_page, str):
                done = True
                continue

            data = await access.get()
            data = data.json
            next_page = data.get("nextPageCursor")
            list_members.extend(create_users(data.get("data")))

        return list_members

    async def fetch_settings(self):
        """
        Returns a `BloxSetting` object
        """
        access = Url("groups", "v1/groups/%id%/settings", id=self.id)
        data = await access.get()
        data = data.json

        return BloxSettings(payload=data)
        
