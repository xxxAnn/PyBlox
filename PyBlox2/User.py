"""
`User` module is a module managing the interactions with players

Contents:
    `BloxUser`: `BloxType`

Requires:
    `Errors`: `*`
    `Base`: `BloxType`
    `.utils`: `Url`

The following code is provided with 

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

from .Errors import *
from .Base import BloxType
from .utils import Url

class BloxUser(BloxType):
    '''
    A handler for a roblox user

    Attrs:
        `id`
        `username` | `name`

    Fetchables:
        `friends`

    Meths:
        async `fetch`:
            >> my_friends = await client.user.fetch("friends") # where `client` is the BloxClient

    Fetched user *will* be added to cache when using async meth `fetch`
    '''
    def __init__(self, client, user_id, username):
        super().__init__(client)
        self.id = str(user_id)
        self.username = username
        self.can_fetch("friends")

    def __repr__(self):
        _dict = {
            "username": self.username,
            "user_id": self.id
            }

        return json.dumps(_dict)

    def __str__(self):
        return self.username
    
    # start auto generated

    async def accept_friend_request(self):
        try:
            hook = await Url("friends", "/v1/users/%id%/accept-friend-request", id=self.id).post()
        except Forbidden:
            raise UserBlocked
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def decline_friend_request(self):
        try:
            hook = await Url("friends", "/v1/users/%id%/decline-friend-request", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def request_friendship(self):
        """
        Will be deprecated in 1.1 in favor of add_friend
        """
        try: 
            hook = await Url("default", "/user/request-friendship?recipientUserId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def unfriend(self):
        try:
            hook = await Url("friends", "/v1/users/%id%/unfriend", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def follow(self):
        try:
            hook = await Url("friends", "/v1/users/%id%/follow", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance
        except Forbidden:
            raise UserBlocked

    async def unfollow(self):
        try:
            hook = await Url("friends", "/v1/users/%id%/unfollow", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance
    
    # TODO: replace with the friends subAPI
    async def block(self):
        try:
            hook = await Url("default", "/userblock/block?userId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    async def unblock(self):
        try:
            hook = await Url("default", "/userblock/unblock?userId=%id%", id=self.id).post()
        except UnknownClientError:
            logger.debug(UnknownClientError.data.text)
            raise NilInstance

    # end auto generated

    async def fetch_friends(self):
        hook = await Url("friends", "/v1/users/%id%/friends", id=self.id).get()

        data = hook.json
        friend_list = []
        for user_dict in data.get("data"):
            friend_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("name")))
        
        if len(friend_list) == 0:
            raise PyBloxException(
                "User has no friends"
                )

        return friend_list

    # Aliases

    @property
    def name(self):
        return self.username

    async def add_friend(self, *args, **kwargs):
        await self.request_friendship()
   
