import logging

logger = logging.getLogger(__name__)

class Cache:

    def __getattr__(self, attr):

        if attr.startswith("add_"):
            attr = attr.replace("add_", "")

            def __wrap(k, v):
                logger.debug("Adding an object of type {0} named {1} to the cache".format(attr, k))
                try:
                    getattr(self, attr)[k] = v
                except:
                    setattr(self, attr, {k: v})

            return __wrap

        elif attr.startswith("get_"):
            attr = attr.replace("get_", "")

            def __wrap(k):
                logger.debug("Checking cache for an object of type {0} named {1}".format(attr, k))
                try:
                    return getattr(self, attr).get(k)
                except (TypeError, AttributeError):
                    setattr(self, attr, {})
                    return None

            return __wrap