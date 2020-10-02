import logging
import re
import asyncio

import aiohttp

from ..Response import BloxResponse
from ..Errors import HttpError


csrfTokenRegex = re.compile(r"Roblox.XsrfToken.setToken\('(.+)'\)")
logger = logging.getLogger(__name__)


ENDPOINTS = {
    "groups": "groups.roblox.com",
    "friends": "friends.roblox.com",
    "default": "api.roblox.com"
}

class HttpClient:
    """
    Manages low level interactions with the API

    .. note::
        This class is a singleton
    """
    __instance = None

    @staticmethod
    def get():
        return HttpClient.__instance

    def __init__(self, loop, headers: dict={}):
        self.__headers = headers
        self.__loop = loop
        self.__cookies = {}
        self.__authed = False
        HttpClient.__instance = self

    async def close(self):
        await self.__session.close()

    async def connect(self, roblosecurity):
        """
        Prepares the cookie and returns the user logged in as

        Returns
        -------
        :class:`.BloxUser`
            The user that this roblosecurity token is pointing to
        """
        self.__set_cookie(".ROBLOSECURITY", roblosecurity, None)
        self.__session = aiohttp.ClientSession()
        user = await self.__complete_login(self.__headers.copy())

        self.__authed = True
        logger.info("Connection Established")
        return user

    async def __complete_login(self, headers):
        logger.info("Validating Auth")

        try:
            resp = await Url("www.roblox.com", "/my/settings/json").get()
        except HttpError as e:
            logger.critical("Login failed")
            raise

        resp = resp.json
        
        return [resp.get("UserId"), resp.get("Name")]

    async def __raw_request(self, method, url, data=None, headers=None) -> BloxResponse:
        token = "None"
        if headers:
            if headers.get("X-CSRF-TOKEN", False):
                token = headers.get("X-CSRF-TOKEN", False)
        logger.debug("Requesting url {} with token {}".format(url, token))
        try:
            async with self.__session.request(method=method, url=url, data=data, headers=headers) as resp:
                text = await resp.text()
                return BloxResponse(status=resp.status, text=text, headers=resp.headers)
        except Exception as e:
            raise

    async def request(self, method, url, data=None, headers=None, retries=0):
        """
        Request to the API, returns a BloxResponse or raises an HttpError

        Returns
        -------
        :class:`.BloxResponse`
            The response from the API

        Raises
        -------
        :exc:`.HttpError`
            The API returned an error code
        """
        if not headers:
            headers = self.__headers
        response = await self.__raw_request(method='GET', url='https://www.roblox.com/home', headers=headers)
            
        token = re.findall(
            csrfTokenRegex,
            response.text
        )

        self.__headers["X-CSRF-TOKEN"] = token[0]

        if method == "GET":
            headers["content-type"] = "application/json"
        response = await self.__raw_request(method, url, data, headers)

        if not response.status == 200:
            if not retries>0:
                await self.request(method, url, data, retries=retries+1)
            HttpError.error(response)
        else:
            return response

    # Helper
    def __set_header(self, key, value):
        self.__headers[key] = value

    # Helper
    def __set_cookie(self, key, value, cookieProps):
        self.__cookies[key] = value

        cookie_list = []
        for k,v in self.__cookies.items():
            cookie_list.append(k)
            cookie_list.append("=")
            cookie_list.append(v)
            cookie_list.append(";")

        self.__set_header("Cookie", "".join(cookie_list))


class Url:
    """
    Aesthetic object for making requests to the API

    Parameters
    -----------
    endpoint: :class:`str`
        The endpoint, either one of the ones specified in the ENDPOINTS constant or the fully written endpoint (ie ``roblox.com``)
    url: :class:`str`
        The subdomain to append to the endpoint, with values to replace surrounded by '%' (ie ``/users/%id%``)
    parameters: :class:`dict`
        The value with which replace the '%' surrounded identifiers in the *url* parameter (ie ``id=user.id``)
    """
    def __init__(self, endpoint: str, url: str, **params):
        self.__fullurl = endpoint + url
        self.__unparsedparams = params

        endpoint = ENDPOINTS.get(str.lower(endpoint), endpoint)
        self.__http = HttpClient.get()
        if params:
            for k, v in params.items():
                url = url.replace('%'+k+'%', str(v), 1)
        url = endpoint + url
        self.__url = "https://" + url

    @property
    def url(self):
        return self.__url

    def extend(self, extension_url, **params):
        """
        .. warning::
            this is purely experimental

        Example
        --------

        .. code-block:: python

            url = Url("friends", "/v1/users/%user_id%/friends", user_id=...)
            url.extend("/count")
        """
        url = self.__fullurl + extension_url
        fullparams = self.__unparsedparams.extend(params)
        return Url("", url, **fullparams)

    # HTTP methods 

    async def get(self, data=None, headers=None):
        """
        Sends a get request to the url

        Parameters
        -----------
        data
            payload to send with the request
        headers
            headers to send with the request
        """
        return await self.__http.request("GET", self.__url, data, headers)

    async def post(self, data=None, headers=None):
        """
        Sends a post request to the url

        Parameters
        -----------
        data
            payload to send with the request
        headers
            headers to send with the request
        """
        return await self.__http.request("POST", self.__url, data, headers)

    async def put(self, data=None, headers=None):
        """
        Sends a put request to the url

        Parameters
        -----------
        data
            payload to send with the request
        headers
            headers to send with the request
        """
        return await self.__http.request("PUT", self.__url, data, headers)

    async def delete(self, data=None, headers=None):
        """
        Sends a delete request to the url

        Parameters
        -----------
        data
            payload to send with the request
        headers
            headers to send with the request
        """
        return await self.__http.request("DELETE", self.__url, data, headers)

    async def patch(self, data=None, headers=None):
        """
        Sends a patch request to the url

        Parameters
        -----------
        data
            payload to send with the request
        headers
            headers to send with the request
        """
        return await self.__http.request("PATCH", self.__url, data, headers)
      

        