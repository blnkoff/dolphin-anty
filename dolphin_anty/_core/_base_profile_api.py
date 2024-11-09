from abc import ABC, abstractmethod
from typing import Annotated, Optional
from typing_extensions import Self
from pydantic import NonNegativeInt
from sensei import Query, Body

from ._profile_info import ProfileInfo


class BaseProfileAPI(ABC, ProfileInfo):
    product_sub: Optional[int] = None

    @classmethod
    @abstractmethod
    def list(
            cls,
            limit: Annotated[NonNegativeInt, Query(50, le=50)] = 50,
            query: Optional[str] = None,
            tags: Optional[list[str]] = None,
            statuses: Optional[list[int]] = None,
            main_websites: Optional[list[str]] = None,
            users: Optional[list[int]] = None,
            page: NonNegativeInt = 0
    ) -> list[Self]:
        pass

    @classmethod
    @abstractmethod
    def get(cls, id_: NonNegativeInt) -> Self:
        pass

    @classmethod
    @abstractmethod
    def create(cls, profile: Annotated[ProfileInfo, Body(embed=False)]) -> Self:
        pass
