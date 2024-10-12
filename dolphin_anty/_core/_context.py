from sensei import Router, Manager


class ContextProps(type):
    def __new__(cls, name, bases, attrs):
        attrs['_api_token'] = attrs.get('_api_token')
        attrs['_router'] = attrs.get('_router')
        return super().__new__(cls, name, bases, attrs)

    @property
    def api_token(cls) -> str:
        return cls._api_token

    @api_token.setter
    def api_token(cls, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError('API token must be a string')
        else:
            cls._api_token = value

    @property
    def router(cls) -> Router:
        return cls._router

    @property
    def manager(cls) -> Manager:
        return cls.router.manager
