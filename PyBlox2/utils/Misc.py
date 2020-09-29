from ..utils import Url

async def read_pages(access: Url, converter):
    result = []

    hook = await access.get()
    data = hook.json
    result.extend(converter(data.get("data")))

    done = False

    next_page = data.get("nextPageCursor")

    while not done:

        if not isinstance(next_page, str):
            done = True
            continue

        hook = await access.get()
        data = hook.json
        next_page = data.get("nextPageCursor")
        result.extend(converter(data.get("data")))

    return result