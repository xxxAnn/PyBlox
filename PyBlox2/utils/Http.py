"""
The MIT License (MIT)

Copyright (c) Kyando 2020

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
        self.__set_cookie(".ROBLOSECURITY", roblosecurity, None)
        self.__session = aiohttp.ClientSession(loop=self.__loop)
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
        logger.debug("Requesting url {}".format(url))
        try:
            async with self.__session.request(method=method, url=url, data=data, headers=headers) as resp:
                text = await resp.text()
                return BloxResponse(status=resp.status, text=text, headers=resp.headers)
        except Exception as e:
            print(e)

    async def request(self, method, url, data=None, headers=None, retries=0):
        if not headers:
            headers = self.__headers

        if method == "GET":
            headers["content-type"] = "application/json"

        response = await self.__raw_request(method, url, data, headers)

        if not response.status == 200:
            if not retries>0:
                logger.debug("Attempting to actualize X-CSRF token after receiving an error")
                await self.__actualize_token()
                await self.request(method, url, data, headers, retries=retries+1)
            HttpError.error(response.status)
        else:
            return response

    async def __actualize_token(self):
        logger.warning("X-CSRF Token is invalid, updating...")
        response = await self.__raw_request(method='GET', url='https://www.roblox.com/')
            
        token = re.findall(
            csrfTokenRegex,
            response.text
        )

        if len(token) > 0:
            if self.__headers.get("X-CSRF-TOKEN", None) != token[0]:
                logger.info(" Updated X-CSRF-TOKEN " + token[0] + " <")
                self.__set_header("X-CSRF-TOKEN", token[0])

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
        '''
        For example:
            url = Url("friends", "/v1/users/%user_id%/friends", user_id=...)
            url.extend("/count")
        (Note: this is purely experimental)
        '''
        url = self.__fullurl + extension_url
        fullparams = self.__unparsedparams.extend(params)
        return Url("", url, **fullparams)

    ''' HTTP methods '''
    async def get(self, data=None, headers=None):
        return await self.__http.request("GET", self.__url, data, headers)

    async def post(self, data=None, headers=None):
        return await self.__http.request("POST", self.__url, data, headers)

    async def put(self, data=None, headers=None):
        return await self.__http.request("PUT", self.__url, data, headers)

    async def delete(self, data=None, headers=None):
        return await self.__http.request("DELETE", self.__url, data, headers)

    async def patch(self, data=None, headers=None):
        return await self.__http.request("PATCH", self.__url, data, headers)
      

        