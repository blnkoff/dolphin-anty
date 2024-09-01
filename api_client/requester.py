from abc import ABC, abstractmethod
from typing import Callable, Any, Generic, TypeVar, Mapping
from pydantic import BaseModel
from ._base_client import _BaseClient
from .client import Client, AsyncClient
from .endpoint import Endpoint, Args
from .types import IResponse

T = TypeVar('T', Mapping[str, Any], BaseModel, IResponse)


class Requester(ABC, Generic[T]):
    def __new__(
            cls,
            client: _BaseClient,
            endpoint: Endpoint,
            pre: Callable[..., Args] | None = None,
            post: Callable[[IResponse], T] | None = None
    ):
        if isinstance(client, AsyncClient):
            return super().__new__(_AsyncRequester)
        elif isinstance(client, Client):
            return super().__new__(_Requester)
        else:
            raise ValueError("Client must be an instance of AsyncClient or Client")

    def __init__(
            self,
            client: _BaseClient,
            endpoint: Endpoint,
            pre: Callable[..., Args] | None = None,
            post: Callable[[IResponse], T] | None = None
    ):
        self._client = client
        self._pre = pre or self._preprocessing
        self._post = post or self._postprocessing
        self._endpoint = endpoint

    @property
    def client(self) -> _BaseClient:
        return self._client

    @property
    def endpoint(self) -> Endpoint:
        return self._endpoint

    def _preprocessing(self, **kwargs) -> dict[str, Any]:
        endpoint = self._endpoint
        return endpoint.get_args(**kwargs).model_dump(mode="json", exclude_none=True, by_alias=True)

    def _postprocessing(self, response: IResponse) -> T:
        endpoint = self._endpoint

        response_model = endpoint.response_model
        if response_model:
            json = response.json()
            return response_model(**json)
        else:
            return response

    @abstractmethod
    def request(self, **kwargs) -> T:
        pass


class _AsyncRequester(Requester):
    def __init__(
            self,
            client: _BaseClient,
            endpoint: Endpoint,
            pre: Callable[..., Args] | None = None,
            post: Callable[[IResponse], T] | None = None
    ):
        super().__init__(client, endpoint, pre, post)

    async def request(self, **kwargs) -> T:
        client = self._client
        endpoint = self._endpoint

        args = self._pre(**kwargs)
        response = await client.request(endpoint.method, **args)
        return self._post(response)


class _Requester(Requester):
    def __init__(
            self,
            client: _BaseClient,
            endpoint: Endpoint,
            pre: Callable[..., Args] | None = None,
            post: Callable[[IResponse], T] | None = None
    ):
        super().__init__(client, endpoint, pre, post)

    def request(self, **kwargs) -> T:
        client = self._client
        endpoint = self._endpoint

        args = self._pre(**kwargs)
        print(args)
        response = client.request(endpoint.method, **args)
        return self._post(response)
