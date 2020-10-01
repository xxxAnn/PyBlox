import asyncio

from .User import BloxUser
from .Groups import BloxGroup
from .Errors import *
from .Response import BloxResponse
from .Base import DataContainer, Emitter, CommandEmitter
from .utils import HttpClient, Url, Cache, Commander, read_pages

class BloxClient:
    """
    Client that manages high level interactions such as commands and events

    Parameters
    -----------
    prefix: :class:`str`
        Prefix for the commander
    loop: :class:`asyncio.AbstractEventLoop`
        Eventloop for the aiohttp client
    user: Optional[:class:`PyBlox2.User.BloxUser`]
        The client's user object :class:`None` if not logged in
    """
    def __init__(self, verbose=False, loop=None, prefix: str="!"):

        self.__listener = Emitter() 
        self.__commands = CommandEmitter() 
        self.__commander = Commander() 
        self.__cache = Cache()
        self.prefix = prefix

        self.__verbose = verbose
        self.loop = asyncio.get_event_loop() if loop == None else loop
        self.__http = HttpClient(self.loop) 

    def run(self, auth_cookie, **kwargs):
        """
        Runs :meth:`PyBlox2.utils.Http.HttpClient.connect` on the :class:`PyBlox2.Client.BloxClient`'s loop

        .. warning::

            This function is blocking, anything called after will not be executed until it returns.

        Parameters
        -----------
        auth_cookie: :class:`str`
            The roblosecurity cookie used to log in
        """
        loop = self.loop

        async def start():
            try:
                user_data = await self.__http.connect(auth_cookie)
                self.user = BloxUser(self, user_data[0], user_data[1])
                await self._emit("ready", ("I'm ready",))
                if kwargs.get("group_id"):
                    listening_group = await self.get_group(kwargs.pop("group_id"))
                    await self.__commander.start_listening(self, self.__commands, listening_group)
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
        except Exception:
            pass
        finally:
            try:
               e = runner.exception()
               if e:
                    if isinstance(e, PyBloxException):
                        print("Oops, something went wrong: {}\nThis exception can be expected and should be handled.".format(e))
                    else:
                        raise runner.exception()
            except asyncio.exceptions.InvalidStateError:
                pass
            finally:
                runner.remove_done_callback(kill_loop)

    async def quit(self):
        """|coro|

        Closes the :class:`aiohttp.ClientSession` and ends the :class:`asyncio.AbstractEventLoop`
        """
        await self.__http.close()
        self.loop.stop()

    def event(self, coro):
        """
        Decorator function which registers an event *coro*

        Parameters
        -----------

        coro: `meth`
            This coroutine must accept at least one argument.

        Raises
        ------

        :exc:`TypeError`
            event registered must be a coroutine function
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                'event registered must be a coroutine function'
                )

        self.__listener.add(coro.__name__, coro)

        return coro
    
    def command(self, coro):
        """
        Decorator function which adds a command `coro`

        Parameters
        -----------

        coro: `meth`
            This coroutine must accept at least one argument.

        Raises
        ------

        :exc:`TypeError`
            event registered must be a coroutine function
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                'event registered must be a coroutine function'
                )

        self.__commands.add(coro.__name__, coro)

        return coro

    async def _emit(self, event: str, payload):
        try:
            return await self.__listener.fire(event, payload)
        except Exception:
            raise

    async def _push_command(self, name, ctx, args):
        try:
            await self.__commands.fire(name, ctx, args)
        except Exception:
            raise

    async def fetch(self, value):
        """|coro|

        Fetches an attribute

        Parameters
        -----------
        value: :class:`str`
           A valid value to fetch, must be one of the following: `friend_requests`

        Returns
        --------
        :class:`list`
            The fetched value or :class:`None` if not found
        """
        if "friend_requests" in value:

            access = Url("friends", "/v1/my/friends/requests?sortOrder=Asc&limit=100")

            def create_user(raw_data):

                return [BloxUser(client=self, user_id=str(user_dict.get("id")), username=user_dict.get("name")) for user_dict in raw_data.get("data")]

            list_members = await read_pages(access, create_user)

            self.__friend_requests = list_members
            return list_members

    async def get_user(self, identifier, **kwargs): 
        """|coro|

        Finds a user through their name or id
        
        Parameters
        -----------
        identifier: :class:`str` | :class:`int`
            The **case_sensitive** userId or username of the player

        Returns
        --------
        :class:`PyBlox2.User.BloxUser`
            The found BloxUser object or :class:`None` if not found
        """
        is_int = True

        try:
            int(identifier)
        except:
            is_int = False

        user_id = None
        username = None

        if is_int:
            user_id = int(identifier)
        else:
            username = str(identifier)

        if user_id:
            access = Url("default", "/users/%id%", id=user_id)
            hook = await access.get()
            username = hook.json.get("Username")
            user = BloxUser(client=self, user_id=user_id, username=username)
            self.__cache.add_user(username, user)
            return user

        if self.__cache.get_user(username):
            return self.__cache.get_user(username)

        if username:
            access = Url("default", "/users/get-by-username?username=%username%", username=username)
            hook = await access.get()
            id = hook.json["Id"] 
            user = BloxUser(client=self, user_id=id, username=username)
            self.__cache.add_user(username, user)
            return user
        
        return None

    async def get_group(self, group_id: str):
        """
        Returns a `BloxGroup` object with the given group id

        This function checks cache
        """
        if self.__cache.get_group(str(group_id)):
            return self.__cache.get_group(str(group_id))

        access = Url("groups", "/v1/groups/%group_id%/roles", group_id=group_id) 
        hook = await access.get()

        roles = hook.json["roles"]
        group = BloxGroup(client=self, group_id=group_id, roles=roles)
        self.__cache.add_group(str(group_id),group)
        return group

    @property
    def friend_requests(self):
        if hasattr(self, '__friend_requests'):
            return self.__friend_requests
        else:
            raise AttributeNotFetched(
                "friend_requests"
                )
