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

from .Errors import AttributeNotFetched

class BloxType():
    '''
    The base class for most items
    '''
    def __init__(self, client):
        self.client = client
        self.__fetchable = []

    async def fetch(self, attr: str):
        if attr in self.__fetchable:
            resp = await self._fetcher(attr)
            setattr(self, "_"+attr, resp)
            return resp

    def can_fetch(self, *data):
        self.__fetchable.extend(data)

    async def _fetcher(self, attr):
        coro = getattr(self, "fetch_"+attr) 
        if coro == None:
            raise NotImplementedError("Attribute {0} hasn't been implemented yet for {1}".format(attr, self.__class__.__name__))
        return await coro()
    
    def __getattr__(self, attr):
        if attr in self.__fetchable:
            try:
                return getattr(self, "_"+attr)
            except AttributeError:
                raise AttributeNotFetched(attr)


class DataContainer():
    
    def __init__(self):
        self.__data = {}

    def find(self, name):
        if name in self.__data:
            return self.__data[name]
        return None

    def add(self, key, value):
        self.__data[key] = value
        
    def is_empty(self):
        if self.__data:
            return False
        return True


class Emitter(DataContainer):

    def __init__(self):
       super().__init__()

    async def fire(self, name, payload):
        coro = self.find(name)
        if coro:
            await coro(*payload)
            return True
        return False

class CommandEmitter(Emitter):

    def __init__(self):
       super().__init__()

    async def fire(self, name, ctx, args):
        coro = self.find(name)
        if coro:
            await coro(ctx, *args)



