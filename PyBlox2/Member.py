from .General import BloxUser
from .RobloxApiError import RobloxApiError
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
        Will not return an error
        '''
        group_id = str(self.group.id)
        role_id = str(role.id)

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
        return "Success"
    
    def kick(self):
        '''
        May return an error
        '''
        hook = self.client.httpRequest(
            "DELETE",
            "groups.roblox.com",
            "/v1/groups/" + str(self.group.id) + "/users/" + str(self.id)
        )

        return hook