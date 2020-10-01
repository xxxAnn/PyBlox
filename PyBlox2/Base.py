from .Errors import AttributeNotFetched

class BloxType():
    '''
    Handler for the fetching feature.

    Example: ::

        class MyCustomBloxType(BloxType):

            def __init__(self):
                self.fetchable = []
                self.can_fetch("money")

            def fetch_money(self):
                # Send a request to the API and get the amount of money
                return 200 # For the sake of this example, let's say it's 200

        # In an async context
        MyCustomInstance = MyCustomBloxType()

        MyCustomInstance.money
        >> AttributeNotFetched: Attribute 'money' was accessed before being fetched
        await MyCustomInstance.fetch("money")
        >> 200
        MyCustomInstance.money
        >> 200
    
    Attributes
    ----------
    client: :class:`BloxClient`
        The BloxClient this object is attached to.
    fetchable: :class:`list`
        List of fetchable attributes.

    .. warning::
        
        Will raise `NotImplementedError` the if fetch_{attr}, where {attr} is the name of the attribute, meth doesn't exist.

    .. warning::

        This class shouldn't be used alone, it exists to only to be subclassed.
    '''
    def __init__(self, client):
        self.client = client
        self.fetchable = []

    async def fetch(self, *attrs):
        """
        Fetches an attribute by calling :func:`BloxType._fetcher`
        
        Parameters
        ----------
        \*attrs: :class:`str`
            List of attribute names to fetch
        """
        resp = None
        for attr in attrs:
            if attr in self.fetchable:
                resp = await self._fetcher(attr)
                setattr(self, "_"+attr, resp)
        if resp:
            return resp

    def can_fetch(self, *data):
        """
        Extends the `fetchable` list with the list of attributes providen

        Paramaters
        ----------
        \*attrs: :class:`str`
            List of attribute names that can be fetched        
        """
        self.fetchable.extend(data)

    async def _fetcher(self, attr):
        coro = getattr(self, "fetch_"+attr) 
        if coro == None:
            raise NotImplementedError("Attribute {0} hasn't been implemented yet for {1}".format(attr, self.__class__.__name__))
        return await coro()
    
    def __getattr__(self, attr):
        fetchables = self.fetchable
        if attr in fetchables:
            try:
                return getattr(self, "_"+attr)
            except AttributeError:
                raise AttributeNotFetched(attr)

class DataContainer():
    """
    Abstract class emulating a dict type by using a hidden __data value
    This class still allows access through the object.attribute notation
    """
    def __init__(self):
        self.__data = {}

    def find(self, name):
        """
        Wrapper for :func:`__data.__getitem__`
        """
        if name in self.__data:
            return self.__data[name]
        return None

    def add(self, key, value):
        """
        Wrapper for :func:`__data.__setitem__`
        """
        self.__data[key] = value
        
    def is_empty(self):
        """
        Wrapper for :func:`__data.__bool__`
        """
        if self.__data:
            return False
        return True

    def __getitem__(self, key):
        return self.find(key)
    
    def __setitem__(self, key, value):
        self.add(key, value)

    def __contains__(self, key):
        if key in self.__data:
            return True
        return False

    def __iter__(self):
        return iter(self.__data)
    
    def __getattr__(self, key):
        if self[key]:
            return self[key]
        return None

class Emitter(DataContainer):
    """
    A DataContainer storing coros in its __data and firing them when necessary with a given playload
    """
    def __init__(self):
       super().__init__()

    async def fire(self, name, payload):
        """
        Searches for a coro with the `name` and fires it with the given `payload`

        Returns true if the coro is found and false otherwise

        Parameters
        ----------
        name: :class:`str`
            Name identifying the coro

        payload: :class:`tuple` 
            Payload to be fired with the event
        """
        coro = self.find(name)
        if coro:
            await coro(*payload)
            return True
        return False

class CommandEmitter(Emitter):
    """
    A modified Emitter which fires the coros with a ctx argument and an args argument
    """
    def __init__(self):
       super().__init__()

    async def fire(self, name, ctx, args):
        coro = self.find(name)
        if coro:
            await coro(ctx, *args)



