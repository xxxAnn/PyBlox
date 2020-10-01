import logging

logger = logging.getLogger(__name__)

class Cache:
    """
    Cache object storing pre-existing information

    Attrs:
        N/A

    Meths:
        add_{name} where name is the name of the pool
        get_{name} were name is the name of the pool

        Examples:
            >> cache.add_user("identifier", user_object)
            >> cached_user = cache.get_user("identifier")
            >> assert cached_user == user_object

    This object should only be used locally by the library
    """
    def __getattr__(self, attr):

        if attr.startswith("add_"):
            attr = attr.replace("add_", "")

            def __wrap(k, v):
                logger.debug("Adding an object of type {0} identified by {1} to the cache".format(attr, k))
                try:
                    getattr(self, attr)[k] = v
                except:
                    setattr(self, attr, {k: v})

            return __wrap

        elif attr.startswith("get_"):
            attr = attr.replace("get_", "")

            def __wrap(k):
                logger.debug("Checking cache for an object of type {0} identified by {1}".format(attr, k))
                try:
                    return getattr(self, attr).get(k)
                except (TypeError, AttributeError):
                    setattr(self, attr, {})
                    return None

            return __wrap