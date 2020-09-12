from .User import BloxUser
from .Ranks import BloxRank
from .utils import Url


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
        self.__access = Url("groups", "/v1/groups/%group_id%/users/%user_id%", group_id=self.group.id, user_id=self.id)

    async def set_role(self, role: BloxRank):
        '''
        Changes the user's role in the group
        '''
        payload = "{\"roleId\":" + str(role.id) + "}"
        await self.__access.patch(payload)
    
    async def kick(self):
        '''
        kicks the user from the group
        '''
        await self.__access.delete()