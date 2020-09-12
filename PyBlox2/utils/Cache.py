import logging

logger = logging.getLogger(__name__)

class Cache:

    def __getattr__(self, attr):
        if attr.startswith("add_"):
            attr = attr.replace("add_", "")
            def wrap(self, name):
                if not hasattr(self, attr):
                    setattr(self, attr, {})
                if hasattr(self, attr): # This should theoratically always be true
                    getattr(self, attr).get(name)
            return wrap