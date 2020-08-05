import json
import time

# Local
from .RobloxApiError import *
from .General import BloxUser



GROUPS_ENDPOINT = "groups.roblox.com"


def handle_error(func):
    def wrapper(*args, **kwargs):
        result = func()
        if result.status != 200:
            raise RobloxApiError(
                response.status,
                response.read().decode("utf-8")
            )
    
    return wrapper

class BloxMember(BloxUser):
    '''
    A slightly modified BloxUser object
    '''
    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group

    def get_role(self, name: str):
        hook = self.client.httpRequest(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(self.group.id) + "/roles"
            )
        
        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )
        data = json.loads(hook.read().decode("utf-8"))
        roles = data.get("roles")

        for dicto in roles:
            if dicto.get("name") == name:
                return dicto.get("id")

        return None

    def set_rank(self, role_name: str):
        '''
        Changes the user's role in the group
        '''
        group_id = str(self.group.id)
        role_id = str(self.get_role(role_name))

        hook = self.client.httpRequest(
            "PATCH",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(group_id) + "/users/" + str(self.id),
            "{\"roleId\":" + role_id + "}",
            "application/json"
        )

        if hook.status != 200:
            raise PyBlox2.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )
        return "Success"


class BloxGroup:

    def __init__(self, client, group_id, roles):
        self.client = client
        self.id = str(group_id)
        self.roles = roles
    
    def __str__(self):
        hook = self.client.httpRequest(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + self.id
            )
        
        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )
        name = json.loads(hook.read().decode("utf-8")).get("name")
        return name

    def get_role(self, name: str):
        hook = self.client.httpRequest(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + self.id + "roles"
            )
        
        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )
        data = json.loads(hook.read().decode("utf-8"))
        roles = data.get("roles")

        for dicto in roles:
            if dicto.get("name") == name:
                return dicto.get("id")

        return None

    def _get_role_id_from_rank(self, rank: int):
        role_id = None
        for role in self.roles:
            if role.get("rank") == rank:
                role_id = str(role.get("id"))
        if not role_id:
            return "Rank not found"
        else:
            return role_id

    def get_users_in_rank(self, rank: int):
        role_id = self._get_role_id_from_rank(rank)
        hook = self.client.httpRequest(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + self.id + "/roles/"+ role_id +"/users",
            None,
            None
        )
        members_list = []
        iterable = json.loads(hook.read().decode("utf-8"))["data"]
        for user in iterable:
            members_list.append(user.get("username"))

    def get_member(self, username: str):
        user = self.client.get_user(username)
        return BloxMember(client=self.client, user_id=user.id, username=username, group=self)

    def members(self, limit=0):
        '''
        Returns a list of all the group's members
        '''
        actual_limit = limit
        if limit == 0:
            actual_limit = 100

        list_members = []

        uri = "/v1/groups/{0}/users?sortOrder=Asc&limit={1}".format(self.id, actual_limit)

        hook = self.client.httpRequest(
            "GET",
            GROUPS_ENDPOINT,
            uri
            )

        if hook.status != 200:
            raise RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )

        def create_members(group, list):

            result_list = []

            for user_info_dict in list:
                user_dict = user_info_dict.get("user")
                result_list.append(BloxMember(client=self.client, user_id=str(user_dict.get("id")), username=user_dict.get("username"), group=group))

            return result_list

        data = json.loads(hook.read().decode("utf-8"))
        list_members.extend(create_members(self, data.get("data")))

        done = False

        next_page = data.get("nextPageCursor")
        
        if limit == 0:
            while not done:

                if not isinstance(next_page, str):
                    done = True
                    continue

                hook = self.client.httpRequest(
                "GET",
                GROUPS_ENDPOINT,
                uri + "&cursor=" + str(next_page)
                )
                data = json.loads(hook.read().decode("utf-8"))
                next_page = data.get("nextPageCursor")
                list_members.extend(create_members(self, data.get("data")))


        return list_members