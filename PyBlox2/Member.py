from .User import BloxUser
from .Ranks import BloxRank
from .utils import Url
from .Errors import *

class BloxMember(BloxUser):
    """
    A Member object with an attached group that acts as a user object with additional methods to manage the user in relation to the group.

    Attrs:
        `id`
        `username` | `name`

    Fetchable:
        `friends`

    Meths:
        async `fetch`:
            >> my_friends = await client.user.fetch("friends") # where `client` is the BloxClient

    Fetched user *will* be added to cache when using async meth `fetch`
    """
    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group
        self.__access = Url("groups", "/v1/groups/%group_id%/users/%user_id%", group_id=self.group.id, user_id=self.id) 

    async def set_role(self, role: BloxRank):
        '''
        Changes the user's role in the group
        '''
        payload = "{\"roleId\":" + str(role.id) + "}"
        try:
            await self.__access.patch(payload)
        except UnknownClientError as e:
            if e.data.json['errors'][0]['code'] == 3:
                raise NilInstance
    
    async def kick(self):
        '''
        kicks the user from the group
        '''
        await self.__access.delete()