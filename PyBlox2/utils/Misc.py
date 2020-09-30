"""
`Misc` utilities

Contents:
    func `read_pages`

Requires:
    `.utils`: `Url`

The following code is provided with: 

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

from ..utils import Url

CURSOR_IDENTIFIER = "nextPageCursor"

async def read_pages(access: Url, converter):
    """
    Loops through pages using the cursor and returns a list of all the results after using the converter function

    access must be a `get`-able Url object and converter much be a function which takes the received data and converts it 
    to the wanted type or format, this will usually be achieved through the use of list comprehension
    """
    result = []

    hook = await access.get()
    data = hook.json
    result.extend(converter(data))

    done = False

    next_page = data.get(CURSOR_IDENTIFIER)

    while not done:

        if not isinstance(next_page, str):
            done = True
            continue

        hook = await access.get()
        data = hook.json
        next_page = data.get(CURSOR_IDENTIFIER)
        result.extend(converter(data))

    return result