import json
import time


# Local
from .Errors import *
from .Base import BloxType
from .General import BloxUser
from .Ranks import BloxRank
from .Settings import BloxSettings
from .Member import BloxMember
from .utils.Endpoints import *


class BloxGroup(BloxType):

    def __init__(self, client, group_id, roles):
        super().__init__(client)
        self.id = str(group_id)
        self.roles = roles
        self.can_fetch("join_requests", "members", "name")

    def __str__(self):
        return self.name
    
    async def fetch_name(self):
        hook = await self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + self.id
            )
        
        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.text
            )
        name = json.loads(hook.text).get("name", None)
        
        if name == None:
            raise PyBloxException(
                "Group name is invalid"
                )

        return name

    async def _cvrt_dict_blox_member(self, list):
        real_list = []
        for user_dict in list:
            real_list.append(BloxMember(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username"), group=self))

        return real_list

    async def get_role(self, name: str):
        hook = await self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(self.id) + "/roles"
            )
        
        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.text
            )
        data = json.loads(hook.text)
        roles = data.get("roles")

        for dicto in roles:
            if dicto.get("name") == name:
                return BloxRank(payload=dicto, guild=self)

    async def get_member(self, username: str):
        user = await self.client.get_user(username)
        return BloxMember(client=self.client, user_id=user.id, username=username, group=self)

    async def fetch_members(self):
        '''
        Returns a list of all the group's members
        '''
        list_members = []

        uri = "/v1/groups/{0}/users?sortOrder=Asc&limit={1}".format(self.id, 100)

        hook = await self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            uri
            )

        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.text
            )

        def create_members(group, list):

            result_list = []

            for user_info_dict in list:
                user_dict = user_info_dict.get("user")
                result_list.append(BloxMember(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username"), group=group))

            return result_list

        data = json.loads(hook.text)
        list_members.extend(create_members(self, data.get("data")))

        done = False

        next_page = data.get("nextPageCursor")
        
        while not done:

            if not isinstance(next_page, str):
                done = True
                continue

            hook = await self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            uri + "&cursor=" + str(next_page)
            )
            data = json.loads(hook.text)
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

        uri = "/v1/groups/{0}/users?sortOrder=Asc&limit={1}".format(self.id, 100)

        hook = self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            uri
            )

        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.text
            )

        def create_users(list):

            result_list = []

            for user_info_dict in list:
                user_dict = user_info_dict.get("requester")
                result_list.append(BloxUser(client=self.client, user_id=str(user_dict.get("userId")), username=user_dict.get("username")))

            return result_list

        data = json.loads(hook.text)
        list_members.extend(create_users(data.get("data")))

        done = False

        next_page = data.get("nextPageCursor")
        
        while not done:

            if not isinstance(next_page, str):
                done = True
                continue

            hook = self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            uri + "&cursor=" + str(next_page)
            )

            data = json.loads(hook.text)
            next_page = data.get("nextPageCursor")
            list_members.extend(create_users(data.get("data")))

        return list_members

    async def fetch_settings(self):
        '''
        Get the group's settings and return them as BloxSettings object
        '''
        hook = await self.client.http_request(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(self.id) + "/settings"
            )

        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.text
            )

        data = json.loads(hook.text)

        return BloxSettings(payload=data)
        
