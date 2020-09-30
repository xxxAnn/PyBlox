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