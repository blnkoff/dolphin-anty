from sensei import Args
from .context import Context
from .._core import BaseModelMixin

router = Context.router


@router.model()
class BaseModel(BaseModelMixin):
    def __prepare_args__(self, args: Args) -> Args:
        token = Context.api_token
        if token is None:
            raise ValueError('No API token provided')

        args.headers['Authorization'] = f'Bearer {token}'

        return args