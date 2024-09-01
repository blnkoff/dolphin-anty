from abc import ABC, abstractmethod
from .types import _BaseModel


class _APIEntity(_BaseModel, ABC):
    @property
    @abstractmethod
    def id(self) -> int | str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __str__(self):
        str_ = f'{self.__class__.__name__}(id={self.id}; name={self.name})'
        return str_

    def __eq__(self, other: "_APIEntity"):
        return isinstance(other, _APIEntity) and self.model_dump() == other.model_dump()
