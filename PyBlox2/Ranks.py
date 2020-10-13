import json

from .Errors import PyBloxException
from .Base import BloxType
from .utils import Url

class BloxRank(BloxType):
    """
    A rank object representing a roleSet in a group

    Attributes
    ----------
    name: :class:`str`
        Name of the role
    id: :class:`str`
        roleSetId of the role
    rank: :class:`int`
        rank of the role (1-255)
    member_count: :class:`int`
        amount of members in the role
    group: :class:`.BloxGroup`
        group this role is attached to
    description: :class:`str`
        description of this role
    members: list[:class:`.BloxMember`]
        |fch|

        list of members of this role
    """
    def __init__(self, payload, group):
        super().__init__(group.client)
        self.name = payload.pop("name")
        self.id = payload.pop("id")
        self.rank = payload.pop("rank")
        self.member_count = payload.pop("memberCount")
        self.description = payload.pop("description")
        self.group = group
        self.can_fetch("members")

    async def fetch_members(self):
        role_id = self.id
        access = Url("groups", "/v1/groups/%group_id%/roles/%id%/users", group_id=self.group.id, id=self.id)
        members_list = []
        hook = await access.get()
        iterable = hook.json["data"]

        result = await self.group._cvrt_dict_blox_member(self, iterable)

        if result == None:
            raise PyBloxException(
                "Could not find members"
                )
        
        return result
