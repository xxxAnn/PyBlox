
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

class CustomEventException(PyBloxException):
    
    def __init__(self, event_name):
        error_message = "There was an error executing the {} event".format(event_name)
        super().__init__(error_message)

class CommandException(PyBloxException):
    pass

class MissingRequiredArgument(CommandException):

    def __init__(self, command_name):
        error_message = "Missing required argument in command {}".format(command_name)
        super().__init__(error_message)

def catch_error(function):

    async def wrapper(*args, **kwargs):
        response = await function(*args, **kwargs)
        if response.status != 200:
            raise RobloxApiError(
                response.status,
                response.text
            )

    return wrapper
