import json
from .Errors import *


class BloxRank:
    def __init__(self, payload, guild):
        self.name = payload.pop("name")
        self.id = payload.pop("id")
        self.rank = payload.pop("rank")
        self.member_count = payload.pop("memberCount")
        self.description = payload.pop("description")
        self.guild = guild

    async def fetch_members(self):
        role_id = self.id
        hook = self.guild.client.httpRequest(
            "GET",
            "groups.roblox.com",
            "/v1/groups/" + str(self.guild.id) + "/roles/"+ str(self.id) +"/users"
        )
        members_list = []
        iterable = json.loads(hook.read().decode("utf-8"))["data"]

        result = await self.guild._cvrt_dict_blox_member(self, iterable)

        if result == None:
            raise PyBloxException(
                "Could not find members"
                )
        
        self._members = result
        return result
    
    @property
    def members(self):
        if hasattr(self, '_members'):
            return self._members
        else:
            raise AttributeNotFetched(
                    "members"
                )