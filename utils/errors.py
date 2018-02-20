"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
# File for custom exceptions
# noinspection PyPackageRequirements
from discord.ext import commands


class PostException(Exception):
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


class ServiceError(commands.CommandInvokeError):
    """
    Subclass of commands.CommandInvokeError.
    Raised whenever a request to a service
    returns a failure of some sort.
    """
    pass


class NSFWException(commands.CheckFailure):
    """
    Subclass of commands.CheckFailure.
    Raised whenever a NSFW command is not
    executed in a NSFW channel.
    """
    pass
