
class RobloxApiError(BaseException):
    '''
    Sends Roblox's error message as a Python BaseException
    '''
    def __init__(self, http_status, api_error_message):
        super(RobloxApiError, self).__init__(api_error_message)
        self.__status = http_status
        self.__msg = api_error_message
    

    def getAPIErrorMessage(self):
        return self.__msg

    def getAPIHttpStatus(self):
        return self.__status

class PyBloxException(BaseException):

    def __init__(self, error_message):
        super(PyBloxException, self).__init__(error_message)
        self._msg = error_message


class AttributeNotFetched(PyBloxException):
    
    def __init__(self, attribute):
        error_message = "Attribute '{}' was accessed before being fetched".format(attribute)
        super().__init__(error_message)