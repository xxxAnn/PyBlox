import logging

logger = logging.getLogger(__name__)

class Cache:

    def __getattr__(self, attr):
        if attr.startswith("add_"):
            attr = attr.replace("add_", "")
            def __wrap(k, v):
                logger.info("Adding to cache")
                try:
                    getattr(self, attr)[k] = v
                except TypeError:
                    setattr(self, attr, {k: v})
            return __wrap
        elif attr.startswith("get_"):
            attr = attr.replace("get_", "")
            def __wrap(k):
                logger.info("Checking cache")
                try:
                    return getattr(self, attr).get(k)
                except TypeError:
                    raise
                    return None
            return __wrap