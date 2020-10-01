import json

class BloxResponse:
    """
    A response from the Roblox API

    Attributes
    -----------
    status: :class:`int`
    text: :class:`str`
    headers: Optional[:class:`aiohttp.CIMultiDictProxy`]
    """
    def __init__(self, status, text: str, headers=None):
        self.status = status
        self.text = text
        if headers:
            self.headers = headers

    @property
    def json(self):
        """
        Returns the text attribute parsed with json
        """
        return json.loads(self.text)
