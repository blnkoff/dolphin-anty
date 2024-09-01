import sys
import re
from re import Match
from typing import Any, Annotated, get_args, Callable
from pydantic import BaseModel, Field
from .params import Body, Query, Header, Cookie
from .cases import header_case as to_header_case
from pydantic._internal._model_construction import ModelMetaclass


class Args(BaseModel):
    url: str
    params: dict[str, Any] | None = None
    json_: dict[str, Any] | None = Field(None, alias="json")
    headers: dict[str, Any] | None = None
    cookies: dict[str, Any] | None = None


_CaseConverter = Callable[[str], str] | None
_ModelArgs = dict[str, tuple[Annotated, Any] | tuple[Annotated]]


class Endpoint:
    def __init__(
            self,
            path: str,
            method: str,
            params: _ModelArgs | None = None,
            response: _ModelArgs | None = None,
            error_msg: str | None = None,
            query_case: _CaseConverter = None,
            body_case: _CaseConverter = None,
            cookie_case: _CaseConverter = None,
            header_case: _CaseConverter = to_header_case
    ):
        self._path = path
        self._method = method
        self._error_msg = error_msg

        params_model = self._make_model_type('Params', params)
        response_model = self._make_model_type('Response', response)

        self._case_converters = {
            'params': query_case,
            'json': body_case,
            'cookies': cookie_case,
            'headers': header_case
        }

        self._params_model = params_model
        self._response_model = response_model

    @property
    def path(self) -> str:
        return self._path

    @property
    def method(self) -> str:
        return self._method

    @property
    def error_msg(self) -> str | None:
        return self._error_msg

    @property
    def params_model(self) -> type[BaseModel] | None:
        return self._params_model

    @property
    def response_model(self) -> type[BaseModel] | None:
        return self._response_model

    @staticmethod
    def _path_params_names(url: str) -> list[str]:
        pattern = r'\{(\w+)\}'

        parameters = re.findall(pattern, url)

        return parameters

    @staticmethod
    def _make_model_type(model_name: str, model_args: _ModelArgs | None) -> type[BaseModel] | None:

        if model_args:
            annotations = {}
            defaults = {}
            for key, arg in model_args.items():
                if isinstance(arg, tuple | list):
                    annotations[key] = arg[0]
                    if len(arg) == 2:
                        defaults[key] = arg[1]
                else:
                    raise ValueError('Model args must be tuple/list of annotation and default or tuple/list only of annotation')

            model: type[BaseModel] = ModelMetaclass(  # type: ignore
                model_name,
                (BaseModel,),
                {
                    '__module__': sys.modules[__name__],
                    '__qualname__': model_name,
                    '__annotations__': annotations,
                    **defaults
                }
            )
            return model
        else:
            return None

    @staticmethod
    def _replace_path_params(url: str, values: dict[str, Any]) -> str:
        pattern = r'\{(\w+)\}'

        def replace_match(match: Match) -> str:
            param_name = match.group(1)
            return str(values.get(param_name, match.group(0)))

        new_url = re.sub(pattern, replace_match, url)

        return new_url

    def _split_params(self, params: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
        path_params_names = self._path_params_names(self.path)

        path_params = {}
        for path_param_name in path_params_names:
            path_params[path_param_name] = params[path_param_name]
            del params[path_param_name]

        return params, path_params

    def _convert_param_key(self, dest: str, key: str) -> str:
        case_converter = self._case_converters[dest]
        return case_converter(key) if case_converter else key

    def _map_params(self, params: dict[str, Any]) -> dict[str, Any]:
        annotations = self.params_model.__annotations__.copy()
        annotations, _ = self._split_params(annotations)

        new_params = {
            'params': {},
            'json': {},
            'headers': {},
            'cookies': {}
        }

        annotation_map = {
            Query: 'params',
            Body: 'json',
            Cookie: 'cookies',
            Header: 'headers',
        }

        for key, value in annotations.items():
            param_type = type(get_args(value)[1])
            dest = annotation_map[param_type]

            new_params[dest][self._convert_param_key(dest, key)] = params[key]

        new_params = {k: v for k, v in new_params.items() if v}
        return new_params

    def get_args(self, **kwargs) -> Args:
        params_model = self.params_model

        url = self.path
        if params_model:
            params = params_model(**kwargs)
            params = params.model_dump(mode='json')

            params, path_params = self._split_params(params)

            url = self._replace_path_params(self.path, path_params)
            params = self._map_params(params)
        else:
            params = {}

        return Args(
            url=url,
            **params
        )