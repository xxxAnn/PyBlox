import logging

logger = logging.getLogger(__name__)

class HttpError(BaseException):
    """
    Parent class for all HTTP errors
    """
    NotFound = "404 Not Found"
    Forbidden = "403 Forbidden"
    Unauthorized = "401 Unauthorized"
    UnknownClientError = "Unidentified HTTP error"
    @staticmethod
    def error(data):
        code = data.status
        logger.error("Panicked at HTTP error code {}\nWith data {}".format(code, data.json))
        if code == 404: 
            raise NotFound(data)
        elif code == 403: 
            raise Forbidden(data)
        elif code == 401: 
            raise Unauthorized(data)
        else:
            raise UnknownClientError(data)

class NotFound(HttpError):
    """
    Wrapper for the HTTP 404 code
    """
    def __init__(self, data):
        self.data = data
        super().__init__(HttpError.NotFound)

class Unauthorized(HttpError):
    """
    Wrapper for the HTTP 401 code
    """
    def __init__(self, data):
        self.data = data
        super().__init__(HttpError.Unauthorized)

class Forbidden(HttpError):
    """
    Wrapper for the HTTP 403 code
    """
    def __init__(self, data):
        self.data = data
        super().__init__(HttpError.Forbidden)

class UnknownClientError(HttpError):
    """
    Wrapper for any HTTP code that isn't recognized by HttpError
    """
    def __init__(self, data):
        self.data = data
        super().__init__(HttpError.UnknownClientError)

class PyBloxException(BaseException):
    """
    Parent class for library related errors
    """
    def __init__(self, error_message):
        super(PyBloxException, self).__init__(error_message)
        self.__msg = error_message

class UserBlocked(PyBloxException):

    def __init__(self):
        super().__init__("Attempted to interact with a blocked user")

class NilInstance(PyBloxException):

    def __init__(self):
        super().__init__("Attempted manipulation on non existing instance")

class AttributeNotFetched(PyBloxException):
    
    def __init__(self, attribute):
        error_message = "Attribute '{}' was accessed before being fetched".format(attribute)
        super().__init__(error_message)

class CommandException(PyBloxException):
    """
    Parent class for all exceptions related to commands
    """
    pass

class BadArguments(CommandException):
    """
    Arguments in a command are invalid
    """
    def __init__(self, command_name):
        error_message = "Amount or type of argument(s) is invalid in command {}".format(command_name)
        super().__init__(error_message)
