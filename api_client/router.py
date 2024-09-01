from abc import ABC, abstractmethod
from typing import Callable
from ._base_client import _BaseClient
from .client import Client, AsyncClient


class Router(ABC):
    def __new__(cls, client: _BaseClient):
        if isinstance(client, AsyncClient):
            return super().__new__(_AsyncRouter)
        elif isinstance(client, Client):
            return super().__new__(_Router)
        else:
            raise ValueError("Client must be an instance of AsyncClient or Client")

    def __init__(self, client: _BaseClient):
        self._client = client

    @property
    def client(self) -> _BaseClient:
        return self._client

    @abstractmethod
    def get(self, func: Callable):
        pass


class _AsyncRouter(Router):
    def __init__(self, client: AsyncClient):
        super().__init__(client)

    def get(self, func: Callable):
        pass


class _Router(Router):
    def __init__(self, client: Client):
        super().__init__(client)

    def get(self, func: Callable):
        pass


"""
from typing import TypedDict, Generic, TypeVar

T = TypeVar('T')

class BaseProfile:
    @router.get('/browser_profiles/{id_}', error_msg="Some_text")
    def get_profile(id_: Annotated[int, Path()]) -> Args:
        return 
        
    @get_profile.postprocessing()
    def _get_profile_post(response: ProfileModel) -> Profile:
        return Profile(**response)
        
class Profile(BaseProfile):
    @BaseProfile.get_profile()
    def get(id_: int) -> Profile:
        pass
        
class AsyncProfile(BaseProfile):
    @BaseProfile.get_profile()
    async def get(id_: str) -> Profile:
        pass    
"""