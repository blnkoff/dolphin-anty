from typing import Literal, Any, Sequence, Mapping, Callable
from pydantic import BaseModel, constr, PositiveInt, conint, field_validator, Json
from pydantic.alias_generators import to_camel
from typing_extensions import TypedDict

HandlingTuple = tuple[dict[str, dict | str], Callable[[dict[str, Any]], Any] | Callable[[], Any]]

IP = constr(pattern=r"^(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})(\.(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})){3}$")
Port = conint(ge=1, le=65535)
AnyVersion = constr(pattern=r"^(\d+)(\.\d+)*$")
Resolution = constr(pattern=r"^\d{3,4}x\d{3,4}$")

WebRTCMode = Literal['off', 'real', 'altered', 'manual']
CanvasMode = Literal['off', 'real', 'noise']
WebGLMode = Literal['real', 'software', 'manual']
AutoManual = Literal['auto', 'manual']
RealManual = Literal['real', 'manual']
Platform = Literal['windows', 'linux', 'macos']
MainWebsite = Literal['google', 'tiktok', 'crypto', 'facebook']
Status = Literal['ban', 'ready', 'new']


class _BaseModel(BaseModel):
    def __str__(self):
        return f'{self.__class__.__name__}({super().__str__()})'

    @field_validator('*')
    def _transform_empty_collections(cls, value: Any):
        if isinstance(value, (Sequence, Mapping)) and not value:
            return None
        return value

    class Config:
        alias_generator = to_camel


class _ModeMixin(_BaseModel):
    mode: str


class UserAgent:
    mode: AutoManual
    value: str


class WebRTC(_BaseModel):
    mode: WebRTCMode
    ip_address: IP | None = None


class Canvas(_BaseModel):
    mode: CanvasMode


class WebGL(_BaseModel):
    mode: CanvasMode


class WebGLInfo(_BaseModel):
    mode: WebGLMode
    vendor: str
    renderer: str
    webgl2_maximum: str


class ClientRect(_ModeMixin):
    pass


class Notes(_BaseModel):
    content: str | None
    color: str
    style:  str
    icon: str | None


class Timezone(_BaseModel):
    mode: AutoManual
    value: str | None = None


class Locale(_BaseModel):
    mode: AutoManual
    value: str | None


class Ports(_BaseModel):
    mode: str
    blacklist: constr(pattern=r"^(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|\d{1,4})(,(6553[0-5]|655[0-2]\d|65[0-4]\d{2}|6[0-4]\d{3}|[1-5]\d{4}|\d{1,4}))*$") | None


class Proxy(_BaseModel):
    id: PositiveInt
    name: str
    type: Literal['http', 'socks5', 'socks4']
    host: IP
    saved_by_user: bool
    crypto_key_id: PositiveInt
    login: str
    password: str
    change_ip_url: IP | None


class Access(_BaseModel):
    view: bool
    update: bool
    delete: bool
    share: bool
    usage: bool


class Geolocation(_BaseModel):
    mode: AutoManual
    latitude: str | None
    longitude: str | None
    accuracy: str | None


class CPU(_BaseModel):
    mode: RealManual
    value: int


class Memory(_BaseModel):
    mode: AutoManual
    value: int


class Screen(_BaseModel):
    mode: RealManual
    width: int | None
    height: int | None
    resolution: Resolution | None


class Connection(_BaseModel):
    downlink: float
    effective_type: Literal['slow-2g', '2g', '3g', '4g', '5g']
    rtt: int
    saveData: bool


class MediaDevices(_BaseModel):
    mode: RealManual
    audio_inputs: list[str] | None
    video_inputs: list[str] | None
    audioOutputs: list[str] | None


class Extension(_BaseModel):
    url: str
    type: str
    hash: str


class MacAddress(_ModeMixin):
    mode: str
    value: str | None


class DeviceName(_ModeMixin):
    value: str | None = None


class _WebGPU(TypedDict):
    mode: AutoManual
    value: Json


WebGPU = Json[_WebGPU]
