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
    '''
    def __init__(self, status, text: str, headers=None):
        self.status = status
        self.text = text
        if headers:
            self.headers = headers

    def json(self):
        return json.loads(self.text)