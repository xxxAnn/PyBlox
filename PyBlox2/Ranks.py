import json
from .Errors import PyBloxException


class BloxRank:
    def __init__(self, payload, guild):
        self.name = payload.pop("name")
        self.id = payload.pop("id")
        self.rank = payload.pop("rank")
        self.member_count = payload.pop("memberCount")
        self.description = payload.pop("description")
        self.guild = guild

    @property
    def members(self):
        role_id = self.id
        hook = self.guild.client.httpRequest(
            "GET",
            "groups.roblox.com",
            "/v1/groups/" + str(self.guild.id) + "/roles/"+ str(self.id) +"/users"
        )
        members_list = []
        iterable = json.loads(hook.read().decode("utf-8"))["data"]

        result = self.guild._cvrt_dict_blox_member(iterable)

        if result == None:
            raise PyBloxException(
                "Could not find members"
                )

        return result