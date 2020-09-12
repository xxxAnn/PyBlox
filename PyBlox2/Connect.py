import asyncio
import logging

from .utils import HttpClient
from .User import BloxUser

logger = logging.getLogger(__name__)

class connect:

    def __init__(self, roblosecurity):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        self.__loop = loop
        self.__client = HttpClient(loop=self.__loop)
        self.__auth = roblosecurity

    async def __aenter__(self):
        user_data = await self.__connect()
        self.user = BloxUser(self, user_data[0], user_data[1])
        return self

    async def __connect(self):
        return await self.__client.connect(self.__auth)
        
    async def close(self):
        await self.__client.close()

    async def __aexit__(self, *args):
        logger.info('Closed the connection')

    @property
    def client(self):
        return self.__client