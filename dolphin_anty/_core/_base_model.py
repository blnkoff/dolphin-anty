from pydantic import ConfigDict, AliasGenerator
from sensei import APIModel, snake_case, camel_case, Json, Args
from dolphin_anty.context import Context
from dolphin_anty._utils import wrap_converter


class BaseModel(APIModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=wrap_converter(camel_case),
            validation_alias=wrap_converter(camel_case)
        ),
        populate_by_name=True
    )

    @staticmethod
    def __finalize_json__(json: Json) -> Json:
        return json['data']

    @staticmethod
    def __prepare_args__(args: Args) -> Args:
        token = Context.api_token
        if token is None:
            raise ValueError('No API token provided')

        args.headers['Authorization'] = f'Bearer {token}'

        return args

    @staticmethod
    def __response_case__(s: str) -> str:
        return snake_case(s)

    @staticmethod
    def __query_case__(s: str) -> str:
        return camel_case(s)

    @staticmethod
    def __body_case__(s: str) -> str:
        return camel_case(s)