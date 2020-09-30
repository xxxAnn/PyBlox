import json

from .Errors import *
from .Base import BloxType
from .utils import Url

class BloxRank(BloxType):
    """
    A rank object used to modify a user's rank 
    or modify the name, rank or description of a rank

    Attrs:
        `name`
        `id`
        `rank`
        `member_count`
        `group`: BloxGroup
        `description`
    
    Fetchables:
        `members`: List(Member.BloxMember)

    Meths:
        async `fetch`:
            >> developers = await rank.fetch("members") # where `rank` is a group's developer rank

    Fetched user *will* be added to cache when using async meth `fetch`
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
