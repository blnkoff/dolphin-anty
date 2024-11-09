from typing import Callable
from functools import wraps

CaseConverter = Callable[[str], str]


def wrap_converter(converter: CaseConverter) -> CaseConverter:
    @wraps(converter)
    def wrapper(case: str) -> str:
        str_ = converter(case)

        for i in range(4):
            str_ = str_.replace(f'{i}d', f'{i}D')
        return str_

    return wrapper
