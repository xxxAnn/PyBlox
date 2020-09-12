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
