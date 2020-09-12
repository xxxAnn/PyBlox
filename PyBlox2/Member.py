from .User import BloxUser
from .Ranks import BloxRank
from .utils import Url


class BloxMember(BloxUser):

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