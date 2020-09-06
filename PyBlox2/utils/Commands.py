import asyncio
from ..Errors import *

class Commander:
    
    async def start_listening(self, client, commands, listening_to):
        self.__commands = commands
        self.__client = client
        self.__listening_to = listening_to
        self.__last_message = 0
        self.prefix = client.prefix
        await self.start_loop()

    async def start_loop(self):
        while True:
            await self.check_messages()
            await asyncio.sleep(5)

    async def check_messages(self):
        hook = await self.__client.http_request(
            "GET",
            "groups.roblox.com",
            "/v1/groups/{}/wall/posts?limit=10&sortOrder=Desc".format(self.__listening_to.id)
            )
        for msg in hook.json()['data']:
            if await self.check_entity(msg):
                await self.process_new_message(msg)

    async def check_entity(self, msg):
        if msg["id"] > self.__last_message:
            if self.__last_message != 0:
                return True
            self.__last_message = msg["id"]
        return False

    async def process_new_message(self, msg):
        text = msg["body"]
        flags = str.split(text, " ")
        ctx = await self.generate_context(msg)
        await self.__client._emit("message", ctx)
        if flags[0].startswith(self.prefix):
            flags[0] = flags[0].replace(self.prefix, "")
            await self.process_command(flags, ctx)

    async def process_command(self, flags, ctx):
        function_name = flags.pop(0)
        args = tuple(flags)
        try:
            await self.__client.push_command(function_name, ctx, args)
        except (TypeError, CustomEventException) as e:
            if await self.__client._emit("error", (ctx, e)):
                return
            raise MissingRequiredArgument(
                function_name
                )

    async def generate_context(self, msg):
        try:
            member = await self.__listening_to.get_member(msg["poster"]["username"])
        except:
            member = await self.__client.get_user(msg["poster"]["username"])
        return Context(member, msg["body"])

class Context:
    def __init__(self, user, ctt):
        self.user = user
        self.content = ctt




