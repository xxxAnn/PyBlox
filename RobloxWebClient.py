import http.client
import re
import json
import enum
import asyncio
import RobloxApi.General as Utilities
import RobloxApi.Groups as GroupModule

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




    def __init__(self, verbose=False):

        self.__headers = {}
        self.__cookies = {}

        self.__authenticated = False
        self.__clientSettings = {}

        self.verbose = verbose

    def connect(self, authCookie, callback=None):

        self.__setCookie(".ROBLOSECURITY", authCookie, None)

        csrfToken = self.__updateCSRFToken(self.__headers.copy())

        newCookies = {}
        success = self.__validateLogin(self.__headers.copy())
        if not success:
            if FFDoPrint:
                print("> .ROBLOSECURITY Cookie Expired <")
            raise Exception(".ROBLOSECURITY Cookie Expired")

        self.__authenticated = True
        self.__updateCSRFToken(self.__headers.copy())

        self.httpRequest("GET", "www.roblox.com", "/")

        # Establish Libraries

        if FFDoPrint:
            print("> RobloxWebClient Connection Established <")
            callback()

    def __validateLogin(self, headers) -> bool:

        if FFDoPrint:
            if self.verbose:
                print("Validating Auth")

        conn = http.client.HTTPSConnection("www.roblox.com")
        conn.request("GET", "/my/settings/json", None, headers)

        try:
            self.__clientSettings = json.loads(conn.getresponse().read().decode("utf-8"))
        except:
            return False

        if self.__clientSettings["UserId"] != None:
            return True
        else:
            return False




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




    def __updateCSRFToken(self, headers):
        conn = http.client.HTTPSConnection("www.roblox.com")
        conn.request("GET", "/home", None, headers)
        response = conn.getresponse()

        if response.status == 302:
            conn = http.client.HTTPSConnection("www.roblox.com")
            conn.request("GET", response.getheader("location"), None, headers)
            response = conn.getresponse()

        token = re.findall(
            csrfTokenRegex,
            response.read().decode('utf-8')
        )

        if len(token) > 0:
            if self.__headers.get("X-CSRF-TOKEN", None) != token[0]:
                if FFDoPrint:
                    if self.verbose:
                        print("> Updated X-CSRF-TOKEN " + token[0] + " <")
                self.__setHeader("X-CSRF-TOKEN", token[0])


    def get_user(self, username: str):
        response = self.httpRequest(
        "GET",
        "api.roblox.com",
        "/users/get-by-username?username=" + username,
        None,
        None
        )

        if response.status != 200:
            raise PyBlox.RobloxApi.RobloxApiError.RobloxApiError(
                response.status,
                response.read().decode("utf-8")
            )

        id = json.loads(response.read().decode("utf-8"))["Id"]
        return Utilities.BloxUser(client=self, user_id=id, username=username)

    def get_group(self, group_id: str):
        hook = self.httpRequest(
            "GET",
            "groups.roblox.com",
            "/v1/groups/" + str(group_id) + "/roles",
            None,
            None
        )

        if hook.status != 200:
            raise PyBlox.RobloxApi.RobloxApiError.RobloxApiError(
                response.status,
                response.read().decode("utf-8")
            )

        roles = json.loads(hook.read().decode("utf-8"))["roles"]
        return GroupModule.BloxGroup(client=self, group_id=group_id, roles=roles)

    def getAccountSettings(self):
        return self.__clientSettings

    def httpRequest(self, method, domain, url, content = None, contentType = None) -> http.client.HTTPResponse:
        global rbxRootDomain

        if not self.__authenticated:
            raise Exception("RobloxWebClient is not Connected!")

        #I WILL TRY TO FIND A BETTER WAY TO DO THIS!
        self.__updateCSRFToken(self.__headers)

        #Sub Domains
        connection:http.client.HTTPSConnection

        if domain != None:
            if FFPrintHttp:
                if self.verbose:
                    print("Requesting: " + domain + url)
            connection = http.client.HTTPSConnection(domain)
        else:
            if FFPrintHttp:
                if self.verbose:
                    print("Requesting: www.roblox.com" + url)
            connection = http.client.HTTPSConnection("www.roblox.com")

        #Request
        if connection != None:

            payloadHeaders = self.__headers.copy()
            if content != None:
                payloadHeaders["Content-Type"] = contentType
                connection.request(method, url, content, payloadHeaders)

            else:
                connection.request(method, url, None, payloadHeaders)


            response = connection.getresponse()


            #Set Cookie Reponse Header
            setCookieHeaders = response.headers.get_all("set-cookie");
            if setCookieHeaders:
                for setData in setCookieHeaders:

                    cookieProps = setData.split(";")

                    if len(cookieProps) > 0:
                        primary = re.findall("(.*?)=(.*)", cookieProps[0])

                        if len(primary) == 1:

                            cookieData = {}
                            cookieName = primary[0][0]
                            cookieValue = primary[0][1]

                            for i in range(1, len(cookieProps)):
                                data = re.findall("(.*?)=(.*)", cookieProps[i])
                                if len(data) == 1:
                                    cookieData[data[0][0]] = data[0][1]

                            self.__setCookie(cookieName, cookieValue, cookieData)

        return response
