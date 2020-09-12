import logging

logger = logging.getLogger(__name__)


class RobloxApiError(BaseException):
    '''
    Sends Roblox's error message as a Python BaseException
    '''
    def __init__(self, http_status, api_error_message):
        super(RobloxApiError, self).__init__(api_error_message)
        self.__status = http_status
        self.__msg = api_error_message
    

    def get_api_error_message(self):
        return self.__msg

    def get_api_http_status(self):
        return self.__status

class HttpError(BaseException):
    NotFound = "404 Not Found"
    Forbidden = "403 Forbidden"
    Unauthorized = "401 Unauthorized"
    @staticmethod
    def error(code):
        logger.fatal("Panicked at HTTP error code {}".format(code))
        if code == 404: 
            raise NotFound()
        elif code == 403: 
            raise Forbidden()
        elif code == 401: 
            raise Unauthorized()
        raise HttpError("Received an http error code {}".format(code))

class NotFound(HttpError):
    def __init__(self):
        super().__init__(HttpError.NotFound)

class Unauthorized(HttpError):
    def __init__(self):
        super().__init__(HttpError.Unauthorized)

class Forbidden(HttpError):
    def __init__(self):
        super().__init__(HttpError.Unauthorized)

class PyBloxException(BaseException):

    def __init__(self, error_message):
        super(PyBloxException, self).__init__(error_message)
        self._msg = error_message


class AttributeNotFetched(PyBloxException):
    
    def __init__(self, attribute):
        error_message = "Attribute '{}' was accessed before being fetched".format(attribute)
        super().__init__(error_message)

class CommandException(PyBloxException):
    pass

class BadArguments(CommandException):

    def __init__(self, command_name):
        error_message = "Amount or type of argument(s) is invalid in command {}".format(command_name)
        super().__init__(error_message)
