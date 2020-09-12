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

import json

class BloxResponse:
    '''
    A response from the Roblox API

    May or may not have headers

    ----------------------------------------------------------------

    Attributes:

    BloxResponse.status -> HTTP response code
    BloxResponse.text -> The response body (default 'application/json')
    BloxResponse.headers -> (optional) The response's header (a CIMultiDictProxy)

    Property:

    BloxResponse.json -> Virtually equivalent to json.loads(BloxResponse.text)
    '''
    def __init__(self, status, text: str, headers=None):
        self.status = status
        self.text = text
        if headers:
            self.headers = headers

    @property
    def json(self):
        return json.loads(self.text)
