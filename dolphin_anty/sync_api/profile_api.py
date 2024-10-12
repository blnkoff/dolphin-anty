from typing import Union, Annotated
from pydantic import NonNegativeInt
from typing_extensions import Self
from sensei import Query, Router
from .._core import BaseProfileAPI
from .context import Context
from ._base_model import BaseModel

router: Router = Context.router


class ProfileAPI(BaseProfileAPI, BaseModel):
    @classmethod
    @router.get('/browser_profiles')
    def list(
            cls,
            limit: Annotated[NonNegativeInt, Query(50, le=50)] = 50,
            query: Union[str, None] = None,
            tags: Union[list[str], None] = None,
            statuses: Union[list[int], None] = None,
            main_websites: Union[list[str], None] = None,
            users: Union[list[int], None] = None,
            page: NonNegativeInt = 0
    ) -> list[Self]:
        ...

    @classmethod
    @router.get('/browser_profiles/{id_}')
    def get(cls, id_: NonNegativeInt) -> Self: ...
