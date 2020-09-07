# Builtin
import re
import json
import enum
import asyncio
import http.client

# Extern
import aiohttp
from printy import printy

# Local
from .General import BloxUser
from .Groups import BloxGroup
from .Errors import *
from .Response import BloxResponse
from .Base import DataContainer, Emitter, CommandEmitter
from .utils.Endpoints import *
from .extra import Commander

csrfTokenRegex = re.compile(r"Roblox.XsrfToken.setToken\('(.+)'\)")
rbxRootDomain:http.client.HTTPSConnection = None

class BloxClient():

    __headers:dict = None
    __cookies:dict = None

    __authenticated:bool = False
    __client_settings:dict = None

    def __init__(self, verbose=False, loop=None, prefix: str="!"):

        self.__headers = {}
        self.__cookies = {}
        self.__printed = ""
        self.__count = 0

        self.__authenticated = False
        self.__client_settings = {}
        self.__listener = Emitter() #
        self.__commands = CommandEmitter() #
        self.__commander = Commander() #
        self.prefix = prefix

        self.verbose = verbose
        self.loop = asyncio.get_event_loop() if loop == None else loop


    async def connect(self, authCookie, **kwargs):
        '''
        Creates the connection header and verifies the connection
        '''
        self.__set_cookie(".ROBLOSECURITY", authCookie, None)
        self._session = aiohttp.ClientSession(loop=self.loop)
        csrfToken = await self.__update_csrf_token(self.__headers.copy())

        newCookies = {}
        success = await self.__validate_login(self.__headers.copy())
        if not success:
            self.print("> .ROBLOSECURITY Cookie Expired <")
            raise Exception(".ROBLOSECURITY Cookie Expired")

        self.__authenticated = True
        await self.__update_csrf_token(self.__headers.copy())

        self.colour_print("> Connection Established <", "cB")
        try:
            await self._emit("ready", ("I'm ready!",))
        except CustomEventException:
            raise
        if kwargs["group_id"]:
            try:
                listening_group = await self.get_group(kwargs.pop("group_id"))
                await self.__commander.start_listening(self, self.__commands, listening_group)
            except KeyboardInterrupt:
                pass
            except Exception:
                raise
            finally:
                await self._session.close()
        await self._session.close()

    def colour_print(self, txt, flag):
        printy(txt, flag)

    def run(self, auth_cookie, **kwargs):
        '''
        Starts the connect coroutine and runs the loop
        '''
        loop = self.loop

        async def start():
            await self.connect(auth_cookie, **kwargs)
            await self._session.close()

        async def close_session():
            await self._session.close()

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
            raise CustomEventException(event)

    async def push_command(self, name, ctx, args):
        '''
        Shorthand for self.__commands.fire
        '''
        try:
            await self.__commands.fire(name, ctx, args)
        except Exception:
            raise CustomEventException(name)

    def print(self, text):
        '''
        Printing additional info for verbose
        '''
        if self.verbose:
            realtext = text
            if text == self.__printed:
                self.__count+=1
            else:
                if self.__count>0:
                    realtext = "\n" + text
                self.__count = 0
            if self.__count>0:
                printy("x{}".format(self.__count), "rB", end="\r")
                return
            printy(realtext, "rB")
            self.__printed = text

    async def __validate_login(self, headers) -> bool:

        self.print("Validating Auth")

        x = await self.request(method='GET', url="https://www.roblox.com/my/settings/json", data=None, headers=headers)

        try:
            self.__client_settings = json.loads(x.text)
        except:
            return False

        if self.__client_settings["UserId"] != None:
            return True
        else:
            return False

    async def fetch(self, value):

        self.print("Fetching: " + value.replace("_", " "))

        if "friend_requests" in value:
            list_members = []

            uri = "/v1/my/friends/requests?sortOrder=Asc&limit={0}".format(100)
            hook = await self.http_request(
                "GET",
                FRIENDS_ENDPOINT,
                uri
                )
            if hook.status != 200:
                raise RobloxApiError(
                    hook.status,
                    hook.read().decode("utf-8")
                )

            def create_user(list):

                result_list = []

                for user_dict in list:
                    result_list.append(BloxUser(client=self, user_id=str(user_dict.get("id")), username=user_dict.get("name")))

                return result_list

            data = json.loads(hook.text)
            list_members.extend(create_user(data.get("data")))

            done = False

            next_page = data.get("nextPageCursor")
        
            while not done:

                if not isinstance(next_page, str):
                    done = True
                    continue

                hook = await self.http_requset(
                "GET",
                FRIENDS_ENDPOINT,
                uri + "&cursor=" + str(next_page)
                )
                data = json.loads(hook.text)
                next_page = data.get("nextPageCursor")
                list_members.extend(create_user(data.get("data")))

            self._friend_requests = list_members
            return list_members

    def __set_header(self, key, value):
        self.__headers[key] = value


    def __set_cookie(self, key, value, cookieProps):
        self.__cookies[key] = value

        cookieList = []
        for k,v in self.__cookies.items():
            cookieList.append(k)
            cookieList.append("=")
            cookieList.append(v)
            cookieList.append(";")

        self.__set_header("Cookie", "".join(cookieList))

    async def request(self, method ,url, data=None, headers=None):
        self.print("Requesting: " + url)
        async with self._session.request(method=method, url=url, data=data, headers=headers) as resp:
            assert resp.status == 200
            text = await resp.text()
            return BloxResponse(status=resp.status, text=text, headers=resp.headers)

    async def __update_csrf_token(self, headers):
        response = await self.request(method='GET', url='https://www.roblox.com/', data=None, headers=headers)

        if response.status == 302:
            self.print("Redirecting")
            conn = http.client.HTTPSConnection("www.roblox.com")
            conn.request("GET", response.headers.get("location"), None, headers)
            response = conn.getresponse()
            
        token = re.findall(
            csrfTokenRegex,
            response.text
        )

        if len(token) > 0:
            if self.__headers.get("X-CSRF-TOKEN", None) != token[0]:
                self.print("> Updated X-CSRF-TOKEN " + token[0] + " <")
                self.__set_header("X-CSRF-TOKEN", token[0])


    async def get_user(self, username: str):
        response = await self.http_request(
        "GET",
        DEFAULT_ENDPOINT,
        "/users/get-by-username?username=" + username,
        None,
        None
        )

        if response.status != 200:
            raise PyBlox.RobloxApi.RobloxApiError.RobloxApiError(
                response.status,
                response.text
            )

        id = json.loads(response.text)["Id"]
        return BloxUser(client=self, user_id=str(id), username=username)

    async def get_group(self, group_id: str):
        hook = await self.http_request(
            "GET",
            GROUPS_ENDPOINT,
            "/v1/groups/" + str(group_id) + "/roles",
            None,
            None
        )
        if hook.status != 200:
            raise PyBlox.RobloxApi.RobloxApiError.RobloxApiError(
                hook.status,
                hook.text
            )
        roles = json.loads(hook.text)["roles"]
        return BloxGroup(client=self, group_id=group_id, roles=roles)

    def get_account_settings(self):
        return self.__client_settings

    async def http_request(self, method, domain, url, content = None, content_type = None) -> BloxResponse:
        global rbxRootDomain
        
        if not self.__authenticated:
            raise PyBloxException(
                "BloxClient is not Connected!"
                )
        

        #I WILL TRY TO FIND A BETTER WAY TO DO THIS!
        await self.__update_csrf_token(self.__headers)

        #Request
        if self._session != None:

            payload_headers = self.__headers.copy()
            if content_type == None:
                content_type = 'application/json'
            payload_headers["Content-Type"] = content_type
            url = "https://" + domain + url
            response = await self.request(method=method, url=url, data=content, headers=payload_headers)
            await self._emit("request", response)

        return response

    @property
    def friend_requests(self):
        if hasattr(self, '_friend_requests'):
            return self._friend_requests
        else:
            raise AttributeNotFetched(
                "friend_requests"
                )
