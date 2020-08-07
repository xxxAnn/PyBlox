from .General import BloxUser
from .Errors import RobloxApiError
from .Ranks import BloxRank


GROUPS_ENDPOINT = "groups.roblox.com"


class BloxMember(BloxUser):
    '''
    A slightly modified BloxUser object
    '''
    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group

    def set_role(self, role: BloxRank) -> str:
        '''
        Changes the user's role in the group
        '''
        group_id = str(self.group.id)

        hook = self.client.httpRequest(
            "PATCH",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(self.group.id) + "/users/" + str(self.id),
            "{\"roleId\":" + role_id + "}",
            "application/json"
        )

        if hook.status != 200:
            raise PyBlox2.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )
    
    def kick(self):
        '''
        kicks the user from the group
        '''
        hook = self.client.httpRequest(
            "DELETE",
            "groups.roblox.com",
            "/v1/groups/" + str(self.group.id) + "/users/" + str(self.id)
        )

        if hook.status != 200:
            raise PyBlox2.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.read().decode("utf-8")
            )