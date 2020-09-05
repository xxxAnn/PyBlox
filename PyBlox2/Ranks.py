import json
from .Errors import *
from .Base import BloxType
from .utils.Endpoints import *


class BloxRank(BloxType):
    def __init__(self, payload, guild):
        super().__init__()
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
            GROUPS_ENDPOINT,
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