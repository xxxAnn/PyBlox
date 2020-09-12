# Builtin
import re
import json
import enum
import asyncio
import http.client

import aiohttp

from .User import BloxUser
from .Groups import BloxGroup
from .Errors import *
from .Response import BloxResponse
from .Base import DataContainer, Emitter, CommandEmitter
from .utils import HttpClient, Url, Cache, Commander


rbxRootDomain:http.client.HTTPSConnection = None

class BloxClient:

    def __init__(self, verbose=False, loop=None, prefix: str="!"):

        self.__authenticated = False
        self.__client_settings = {}
        self.__listener = Emitter() 
        self.__commands = CommandEmitter() 
        self.__commander = Commander() 
        self.__cache = Cache()
        self.prefix = prefix

        self.verbose = verbose
        self.loop = asyncio.get_event_loop() if loop == None else loop
        self.__http = HttpClient(self.loop) 

    def run(self, auth_cookie, **kwargs):
        '''
        Starts the connect coroutine and runs the loop
        '''
        loop = self.loop

        async def start():
            try:
                user_data = await self.__http.connect(auth_cookie)
                self.user = BloxUser(self, user_data[0], user_data[1])
                await self._emit("ready", ("I'm ready",))
                if kwargs["group_id"]:
                    listening_group = await self.get_group(kwargs.pop("group_id"))
                    await self.__commander.start_listening(self, self.__commands, listening_group)
            except KeyboardInterrupt:
                pass
            except Exception:
                raise
            finally:
                await self.__http.close()

        async def close_session():
            await self.__http.close()

        def kill_loop(f):
            loop.stop()

        runner = asyncio.ensure_future(start(), loop=loop) 
        runner.add_done_callback(kill_loop)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            runner.remove_done_callback(kill_loop)
    
    def event(self, coro):
        '''
        Registers an event
        '''
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                'event registered must be a coroutine function'
                )

        self.__listener.add(coro.__name__, coro)

        return coro
    
    def command(self, coro):
        '''
        Registers a command
        '''
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                'event registered must be a coroutine function'
                )

        self.__commands.add(coro.__name__, coro)

        return coro

    async def _emit(self, event: str, payload):
        '''
        Shorthand for self.__listner.fire
        '''
        try:
            return await self.__listener.fire(event, payload)
        except Exception:
            raise

    async def push_command(self, name, ctx, args):
        '''
        Shorthand for self.__commands.fire
        '''
        try:
            await self.__commands.fire(name, ctx, args)
        except Exception:
            raise

    async def fetch(self, value):

        if "friend_requests" in value:
            list_members = []

            access = Url("friends", "/v1/my/friends/requests?sortOrder=Asc&limit=100")

            def create_user(list):

                result_list = []

                for user_dict in list:
                    result_list.append(BloxUser(client=self, user_id=str(user_dict.get("id")), username=user_dict.get("name")))

                return result_list

            hook = await access.get()
            data = hook.json
            list_members.extend(create_user(data.get("data")))

            done = False

            next_page = data.get("nextPageCursor")
        
            while not done:

                if not isinstance(next_page, str):
                    done = True
                    continue

                hook = await access.get()
                data = hook.json
                next_page = data.get("nextPageCursor")
                list_members.extend(create_user(data.get("data")))

            self._friend_requests = list_members
            return list_members

    async def get_user(self, username: str, user_id=None):

        if user_id:
            access = Url("default", "/users/%id%", id=user_id)
            hook = await access.get()
            username = hook.json.get("Username")
            return await self.get_user(username=username, user_id=None)

        if self.__cache.get_user(username):
            return self.__cache.get_user(username)

        access = Url("default", "/users/get-by-username?username=%username%", username=username)
        hook = await access.get()

        id = hook.json["Id"]
        user = BloxUser(client=self, user_id=id, username=username)
        self.__cache.add_user(username, user)
        return user

    async def get_group(self, group_id: str):
        if self.__cache.get_group(str(group_id)):
            return self.__cache.get_group(str(group_id))

        # Just confirmation that the group actually exists
        access = Url("groups", "/v1/groups/%group_id%/roles", group_id=group_id) 
        hook = await access.get()

        roles = hook.json["roles"]
        group = BloxGroup(client=self, group_id=group_id, roles=roles)
        self.__cache.add_group(str(group_id),group)
        return group

    @property
    def friend_requests(self):
        if hasattr(self, '_friend_requests'):
            return self._friend_requests
        else:
            raise AttributeNotFetched(
                "friend_requests"
                )
