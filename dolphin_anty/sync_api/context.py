from sensei import Router
from .._core import ContextProps


class Context(metaclass=ContextProps):
    _router = Router(host='https://dolphin-anty-api.com')
