import json

class BloxResponse:
    """
    A response from the Roblox API

    Attrs:
        `status`
        `text`
        `headers` -> May or may not exist
        `json`
    """
    def __init__(self, status, text: str, headers=None):
        self.status = status
        self.text = text
        if headers:
            self.headers = headers

    @property
    def json(self):
        return json.loads(self.text)
