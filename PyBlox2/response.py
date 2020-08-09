
class BloxResponse:
    '''
    A response from the Roblox API

    May or may not have headers
    You can json.loads the text attribute to obtain a JSON structure (if it is 'application/json')

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