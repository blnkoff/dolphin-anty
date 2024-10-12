from sensei import APIModel, snake_case, camel_case, Json


class BaseModelMixin(APIModel):
    def __finalize_json__(self, json: Json) -> Json:
        return json['data']

    def __response_case__(self, s: str) -> str:
        return snake_case(s)

    def __query_case__(self, s: str) -> str:
        return camel_case(s)