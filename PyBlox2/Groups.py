import json
import time


# Local
from .Errors import *
from .Base import BloxType
from .User import BloxUser
from .Ranks import BloxRank
from .Settings import BloxSettings
from .Member import BloxMember
from .utils import Url


class BloxGroup(BloxType):

    def __init__(self, client, group_id, roles):
        super().__init__(client)
        self.id = str(group_id)
        self.roles = roles
        self.can_fetch("join_requests", "members", "name")

    def __str__(self):
        return self.name or "Unknown"
    
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
        '''
        Returns a list of all the group's members
        '''
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
        '''
        Returns a list of users that request to join the group
        '''
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
        '''
        Get the group's settings and return them as BloxSettings object
        '''
        access = Url("groups", "v1/groups/%id%/settings", id=self.id)
        data = await access.get()
        data = data.json

        return BloxSettings(payload=data)
        
