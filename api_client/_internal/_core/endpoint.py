from typing import Any, get_args, Callable, Annotated
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo
from api_client.params import Body, Query, Header, Cookie
from api_client.cases import header_case as to_header_case
from .._tools import ChainedMap, fill_path_params, split_params, make_model, is_safe_method, HTTPMethod, validate_method

_CaseConverter = Callable[[str], str] | None


class Args(BaseModel):
    url: str
    params: dict[str, Any] | None = None
    json_: dict[str, Any] | None = Field(None, alias="json")
    headers: dict[str, Any] | None = None
    cookies: dict[str, Any] | None = None


def _identical(s: str) -> str: return s


class Endpoint:
    def __init__(
            self,
            path: str,
            method: HTTPMethod,
            params: dict[str, Any] | None = None,
            response: dict[str, Any] | None = None,
            error_msg: str | None = None,
            query_case: _CaseConverter = _identical,
            body_case: _CaseConverter = _identical,
            cookie_case: _CaseConverter = _identical,
            header_case: _CaseConverter = to_header_case
    ):
        validate_method(method)

        self._path = path
        self._method = method
        self._error_msg = error_msg

        params_model = self._make_model('Params', params)
        response_model = self._make_model('Response', response)

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
    def method(self) -> HTTPMethod:
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
    def _make_model(model_name: str, model_args: dict[str, Any] | None) -> type[BaseModel] | None:
        if model_args:
            return make_model(model_name, model_args)
        else:
            return None

    def get_args(self, **kwargs) -> Args:
        params_model = self.params_model
        path = self.path
        if params_model:
            url, request_params = self._get_init_args(params_model, **kwargs)
        else:
            url = path
            request_params = {}

        return Args(
            url=url,
            **request_params
        )

    def _get_init_args(
            self,
            params_model: type[BaseModel],
            **kwargs
    ) -> tuple[str, dict[str, Any]]:
        path = self.path
        params_model_instance = params_model(**kwargs)
        params_all = params_model_instance.model_dump(mode='json', by_alias=True)
        params, path_params = split_params(path, params_all)

        annotations_all = params_model.__annotations__.copy()
        annotations, _ = split_params(path, annotations_all)

        request_params = self._map_params(annotations, params)
        url = fill_path_params(path, path_params)
        return url, request_params

    def _map_params(
            self,
            annotations: dict[str, Any],
            params: dict[str, Any]
    ) -> dict[str, Any]:
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

        type_to_converter = ChainedMap[type[FieldInfo], _CaseConverter](annotation_map, self._case_converters)
        type_to_params = ChainedMap[type[FieldInfo], dict[str, Any]](annotation_map, new_params)
        temp_type = type(Annotated[int, int])

        for key, value in annotations.items():
            if isinstance(value, temp_type):
                param_annotation = get_args(value)[1]

                param_type = type(param_annotation)

                converted = type_to_converter[param_type](key)

                result_key = param_annotation.alias if param_annotation.alias else converted
                type_to_params[param_type][result_key] = params[key]
            else:
                param_type = Query if is_safe_method(self.method) else Body

                converted = type_to_converter[param_type](key)
                type_to_params[param_type][converted] = params[key]

        new_params = {k: v for k, v in new_params.items() if v}
        return new_params
