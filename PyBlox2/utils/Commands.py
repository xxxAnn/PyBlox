import logging

import asyncio

from ..Errors import BadArguments
from ..utils import Url


logger = logging.getLogger(__name__)


class Commander:
    """
    Manages looping through the group wall and checking for commands or messages

    Attributes
    -----------
    prefix: :class:`str`
        The command prefix
    """
    async def start_listening(self, client, commands, listening_to):
        self.__commands = commands
        self.__client = client
        self.__listening_to = listening_to
        self.__already_seen = []
        self.__is_first = True
        self.prefix = client.prefix
        self.__access = Url("groups", "/v1/groups/%group_id%/wall/posts?limit=10&sortOrder=Desc", group_id=self.__listening_to.id)
        await self.start_loop()

    async def start_loop(self):
        await self.__client._emit("start_listening", (self.__listening_to,))
        while True:
            await self.__client._emit("check_messages", (self.__listening_to,))
            await self.check_messages()
            await asyncio.sleep(5)

    async def check_messages(self):
        hook = await self.__access.get()
        for msg in hook.json['data']:
            if self.__is_first:
                    self.__already_seen.append(msg["id"])
            if await self.check_entity(msg):
                await self.process_new_message(msg)
        if self.__is_first:
            self.__is_first = False

    async def check_entity(self, msg):
        if not msg["id"] in self.__already_seen:
           self.__already_seen.append(msg["id"])
           return True
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
        except TypeError as e:
            if await self.__client._emit("error", (ctx, e)):
                return
            raise BadArguments(
                function_name
                )

    async def generate_context(self, msg):
        try:
            member = await self.__listening_to.get_member(msg["poster"]["username"])
        except:
            member = await self.__client.get_user(msg["poster"]["username"])
        return Context(member, msg["body"], id=msg["id"], group_id=self.__listening_to.id)

class Context:
    """
    Context object for message on group wall
    
    .. note::
        This objects checks if its `__user_or_member` has a group to determine wether it is a user or not

    Attributes
    -----------
    user: :class:`.BloxUser`
        The user that sent this message, may be :class:`None`
    member: :class:`.BloxMember`
        The member that sent this message, may be :class:`None`
    content: :class:`str`
        The content of the message sent
    """
    def __init__(self, user, ctt, **kwargs):
        self.__user_or_member = user
        self.content = ctt
        self.__id = kwargs.get("id")
        self.__group_id = kwargs.get("group_id")

    @property
    def member(self):
        if self.__user_or_member.group:
            return self.__user_or_member
        return None

    @property
    def user(self):
        if not self.__user_or_member.group:
            return self.__user_or_member
        return None

    async def delete_message(self):
        access = Url("groups", "/v1/groups/%groupid%/wall/posts/%postid%", groupid=self.__group_id, postid=self.__id)
        await access.delete()



