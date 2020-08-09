import re
import json
import enum
import asyncio
import http.client

#
import aiohttp

# Local
from .General import BloxUser
from .Groups import BloxGroup
from .Errors import *
from .response import BloxResponse

FFDoPrint = True
FFPrintHttp = True



csrfTokenRegex = re.compile(r"Roblox.XsrfToken.setToken\('(.+)'\)")
rbxRootDomain:http.client.HTTPSConnection = None


class HttpContentType():
    ApplicationJson = "application/json"
    ApplicationXml = "application/xml"
    ApplicationUrlEncoded = 2
    PlainText = 3
    XmlText = 4



class HttpMethodType(enum.Enum):
    GET = 0
    POST = 1
    PATCH = 2
    DELETE = 3
    OPTIONS = 4


class BloxClient():

    __headers:dict = None
    __cookies:dict = None

    __authenticated:bool = False
    __clientSettings:dict = None

    def __init__(self, verbose=False, loop=None):

        self.__headers = {}
        self.__cookies = {}

        self.__authenticated = False
        self.__clientSettings = {}

        self.verbose = verbose
        self.loop = asyncio.get_event_loop() if loop is None else loop


    async def connect(self, authCookie):
        '''
        Creates the connection header and verifies the connection
        '''
        self.__setCookie(".ROBLOSECURITY", authCookie, None)
        self._session = aiohttp.ClientSession(loop=self.loop)
        csrfToken = await self.__updateCSRFToken(self.__headers.copy())

        newCookies = {}
        success = await self.__validateLogin(self.__headers.copy())
        if not success:
            if self.verbose:
                print("> .ROBLOSECURITY Cookie Expired <")
            raise Exception(".ROBLOSECURITY Cookie Expired")

        self.__authenticated = True
        await self.__updateCSRFToken(self.__headers.copy())

        await self.http_request("GET", "www.roblox.com", "/")

        print("> RobloxWebClient Connection Established <")
        if hasattr(self, 'ready'):
            try:
                await self.ready()
            finally:
                await self._session.close()


    def run(self, auth_cookie):
        '''
        Starts the connect coroutine and runs the loop
        '''
        loop = self.loop

        async def start():
            await self.connect(auth_cookie)

        def kill_loop(f):
            loop.stop()

        runner = asyncio.ensure_future(start(), loop=loop) 
        runner.add_done_callback(kill_loop)
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            return # Should clean remnant tasks
        finally:
            runner.remove_done_callback(kill_loop) # If we keep this it will be executed after the loop is stopped and raise an Error
    
    def event(self, coro):
        '''
        Registers an event and calls it at appropriate times
        '''
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                'event registered must be a coroutine function'
                )
        
        setattr(self, coro.__name__, coro)

        return coro

    async def __validateLogin(self, headers) -> bool:

        if FFDoPrint:
            if self.verbose:
                print("Validating Auth")

        x = await self.request(method='GET', url="https://www.roblox.com/my/settings/json", data=None, headers=headers)

        try:
            self.__clientSettings = json.loads(x.text)
        except:
            return False

        if self.__clientSettings["UserId"] != None:
            return True
        else:
            return False

    async def fetch_friend_requests(self):

        list_members = []

        uri = "/v1/my/friends/requests?sortOrder=Asc&limit={0}".format(100)
        hook = await self.http_request(
            "GET",
            "friends.roblox.com",
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
            "friends.roblox.com",
            uri + "&cursor=" + str(next_page)
            )
            data = json.loads(hook.text)
            next_page = data.get("nextPageCursor")
            list_members.extend(create_user(data.get("data")))

        self._friend_requests = list_members
        return list_members

    def __setHeader(self, key, value):
        self.__headers[key] = value


    def __setCookie(self, key, value, cookieProps):
        self.__cookies[key] = value

        cookieList = []
        for k,v in self.__cookies.items():
            cookieList.append(k)
            cookieList.append("=")
            cookieList.append(v)
            cookieList.append(";")

        self.__setHeader("Cookie", "".join(cookieList))

    async def request(self, method ,url, data=None, headers=None):
        async with self._session.request(method=method, url=url, data=data, headers=headers) as resp:
            assert resp.status == 200
            text = await resp.text()
            return BloxResponse(status=resp.status, text=text, headers=resp.headers)

    async def __updateCSRFToken(self, headers):
        response = await self.request(method='GET', url='https://www.roblox.com/', data=None, headers=headers)

        if response.status == 302:
            conn = http.client.HTTPSConnection("www.roblox.com")
            conn.request("GET", response.headers.get("location"), None, headers)
            response = conn.getresponse()

        token = re.findall(
            csrfTokenRegex,
            response.text
        )

        if len(token) > 0:
            if self.__headers.get("X-CSRF-TOKEN", None) != token[0]:
                if FFDoPrint:
                    if self.verbose:
                        print("> Updated X-CSRF-TOKEN " + token[0] + " <")
                self.__setHeader("X-CSRF-TOKEN", token[0])


    async def get_user(self, username: str):
        response = await self.http_request(
        "GET",
        "api.roblox.com",
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
            "groups.roblox.com",
            "/v1/groups/" + str(group_id) + "/roles",
            None,
            None
        )
        if hook.status != 200:
            raise PyBlox.RobloxApi.RobloxApiError.RobloxApiError(
                response.status,
                hook.text
            )
        roles = json.loads(hook.text)["roles"]
        return BloxGroup(client=self, group_id=group_id, roles=roles)

    def getAccountSettings(self):
        return self.__clientSettingsfr

    async def http_request(self, method, domain, url, content = None, content_type = None) -> BloxResponse:
        global rbxRootDomain

        if not self.__authenticated:
            raise PyBloxException(
                "BloxClient is not Connected!"
                )

        #I WILL TRY TO FIND A BETTER WAY TO DO THIS!
        await self.__updateCSRFToken(self.__headers)

        #Request
        if self._session != None:

            payload_headers = self.__headers.copy()
            if content_type == None:
                content_type = 'application/json'
            payload_headers["Content-Type"] = content_type
            url = "https://" + domain + url
            response = await self.request(method=method, url=url, data=content, headers=payload_headers)

        return response

    @property
    def friend_requests(self):
        if hasattr(self, '_friend_requests'):
            return self._friend_requests
        else:
            raise AttributeNotFetched(
                "friend_requests"
                )
