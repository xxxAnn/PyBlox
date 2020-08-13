from .General import BloxUser
from .Errors import RobloxApiError
from .Ranks import BloxRank


GROUPS_ENDPOINT = "groups.roblox.com"


class BloxMember(BloxUser):
    '''
    A member of a group in Roblox

    Is a descendant of PyBlox2.BloxUser

    ---------------

    Unique methods:
        coroutine set_role(role) -> role must be a PyBlox2.BloxRank
        coroutine kick()

    ---------------

    Unique attributes:
        group -> a PyBlox2.BloxGroup

    '''
    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group

    async def set_role(self, role: BloxRank):
        '''
        Changes the user's role in the group
        '''
        group_id = str(self.group.id)

        hook = await self.client.http_request(
            "PATCH",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(self.group.id) + "/users/" + str(self.id),
            "{\"roleId\":" + role_id + "}",
            "application/json"
        )

        if hook.status != 200:
            raise PyBlox2.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.text
            )
    
    async def kick(self):
        '''
        kicks the user from the group
        '''
        hook = await self.client.http_request(
            "DELETE",
            "groups.roblox.com",
            "/v1/groups/" + str(self.group.id) + "/users/" + str(self.id)
        )

        if hook.status != 200:
            raise PyBlox2.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.text
            )