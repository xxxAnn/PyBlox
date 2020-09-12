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
                logger.debug("Checking cache for an object of type {0} identified by {1}".format(attr, k))
                try:
                    return getattr(self, attr).get(k)
                except (TypeError, AttributeError):
                    setattr(self, attr, {})
                    return None

            return __wrap