# File for custom exceptions

class PostException:
    """
    Raised when there's a error in the post()
    wrapper
    """
    pass

class DBLException(PostException):
    """
    Subclass of PostException,
    raised when there's a error while posting to
    discordbots.org
    """
    pass

class DBotsException(PostException):
    """
    Subclass of PostException,
    raised when there's a error while posting to
    bots.discord.pw
    """
    pass

class DogException(PostException):
    """
    Subclass of PostException,
    raised when there's a error while posting to
    Datadog
    """
    pass
