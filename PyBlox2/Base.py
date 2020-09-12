from .Errors import AttributeNotFetched

class BloxType():
    '''
    The base class for most items
    '''
    def __init__(self, client):
        self.client = client
        self._fetchable = []

    async def fetch(self, attr: str):
        if attr in self._fetchable:
            resp = await self._fetcher(attr)
            setattr(self, "_"+attr, resp)
            return resp

    def can_fetch(self, *data):
        self._fetchable.extend(data)

    async def _fetcher(self, attr): # Default implementation of _fetcher
        coro = getattr(self, "fetch_"+attr) 
        if coro == None:
            raise NotImplementedError("Attribute {0} hasn't been implemented yet for {1}".format(attr, self.__class__.__name__))
        return await coro()
    
    def __getattr__(self, attr):
        if attr in self._fetchable:
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



