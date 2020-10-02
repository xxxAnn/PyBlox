from .User import BloxUser
from .Ranks import BloxRank
from .utils import Url
from .Errors import *

class BloxMember(BloxUser):
    """
    A member object managing a user in relation to a specific group

    .. note::
        This class shouldn't manually be created

    Attributes
    ----------
    id: :class:`str`
        The userId of the user
    group: :class:`.BloxGroup`
        The group this user is member of
    username: :class:`str`
        The username of the user
    friends: list[:class:`.BloxUser`]
        |fch|

        List of this user's friends
    """
    def __init__(self, client, user_id: str, username: str, group):
        super().__init__(client=client, user_id=user_id, username=username)
        self.group = group
        self.__access = Url("groups", "/v1/groups/%group_id%/users/%user_id%", group_id=self.group.id, user_id=self.id) 

    async def set_role(self, role: BloxRank):
        """|coro|

        Changes the user's role in the group

        Parameters
        ----------
        role: :class:`.BloxRank`

        Raises
        ------
        :exc:`.Forbidden`
            You do not have permissions to edit that role
        :exc:`.NilInstance`
            The member doesn't exist or isn't in this group anymore
        """
        payload = "{\"roleId\":" + str(role.id) + "}"
        try:
            await self.__access.patch(payload)
        except UnknownClientError as e:
            if e.data.json['errors'][0]['code'] == 3:
                raise NilInstance
    
    async def kick(self):
        """|coro|

        Kicks the user from the group

        Raises
        ------
        :exc:`.Forbidden`
            You do not have permissions to kick this user
        :exc:`.NilInstance`
            The member doesn't exist or isn't in this group anymore
        """
        await self.__access.delete()