class FailedRequest(Exception):
    pass
class NoContent(Exception):
    pass
class WrongNumberOfArguments(Exception):
    def __init__(self, msg="2 arguments should be entered", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
class InvalidArguments(Exception):
    def __init__(self, msg="Correct usage is main.py format1, format2 or main.py format", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)        