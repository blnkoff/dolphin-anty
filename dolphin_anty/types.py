from __future__ import annotations

import json
from typing import Literal, Any, Sequence, Mapping, Union
from pydantic import constr, PositiveInt, conint, field_validator, NonNegativeInt, \
    ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel
from sensei import APIModel

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

_NNT = NonNegativeInt


class BaseModel(APIModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=to_camel))

    @field_validator('*')
    def _transform_empty_collections(cls, value: Any):
        if isinstance(value, (Sequence, Mapping)) and not value:
            return None
        return value


class _ModeMixin(BaseModel):
    mode: str


class UserAgent:
    mode: AutoManual
    value: str


class WebRTC(BaseModel):
    mode: WebRTCMode
    ip_address: Union[IP, None] = None


class Canvas(BaseModel):
    mode: CanvasMode


class WebGL(BaseModel):
    mode: CanvasMode


class WebGLMaximum(BaseModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=lambda x: x))

    UNIFORM_BUFFER_OFFSET_ALIGNMENT: _NNT
    MAX_TEXTURE_SIZE: _NNT
    MAX_VIEWPORT_DIMS: list[_NNT]
    MAX_VERTEX_ATTRIBS: _NNT
    MAX_VERTEX_UNIFORM_VECTORS: _NNT
    MAX_VARYING_VECTORS: _NNT
    MAX_COMBINED_TEXTURE_IMAGE_UNITS: _NNT
    MAX_VERTEX_TEXTURE_IMAGE_UNITS: _NNT
    MAX_TEXTURE_IMAGE_UNITS: _NNT
    MAX_FRAGMENT_UNIFORM_VECTORS: _NNT
    MAX_CUBE_MAP_TEXTURE_SIZE: _NNT
    MAX_RENDERBUFFER_SIZE: _NNT
    MAX_3D_TEXTURE_SIZE: _NNT
    MAX_ELEMENTS_VERTICES: _NNT
    MAX_ELEMENTS_INDICES: _NNT
    MAX_TEXTURE_LOD_BIAS: _NNT
    MAX_DRAW_BUFFERS: _NNT
    MAX_FRAGMENT_UNIFORM_COMPONENTS: _NNT
    MAX_VERTEX_UNIFORM_COMPONENTS: _NNT
    MAX_ARRAY_TEXTURE_LAYERS: _NNT
    MIN_PROGRAM_TEXEL_OFFSET: int
    MAX_PROGRAM_TEXEL_OFFSET: int
    MAX_VARYING_COMPONENTS: _NNT
    MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS: _NNT
    MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS: _NNT
    MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS: _NNT
    MAX_COLOR_ATTACHMENTS: _NNT
    MAX_SAMPLES: _NNT
    MAX_VERTEX_UNIFORM_BLOCKS: _NNT
    MAX_FRAGMENT_UNIFORM_BLOCKS: _NNT
    MAX_COMBINED_UNIFORM_BLOCKS: _NNT
    MAX_UNIFORM_BUFFER_BINDINGS: _NNT
    MAX_UNIFORM_BLOCK_SIZE: _NNT
    MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS: _NNT
    MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS: _NNT
    MAX_VERTEX_OUTPUT_COMPONENTS: _NNT
    MAX_FRAGMENT_INPUT_COMPONENTS: _NNT
    MAX_ELEMENT_INDEX: _NNT


class WebGLInfo(BaseModel):
    mode: WebGLMode
    vendor: str
    renderer: str
    webgl2_maximum: WebGLMaximum

    @field_validator('webgl2_maximum', mode='before')
    def _validate_webgl2_maximum(cls, value):
        return json.loads(value)


class ClientRect(_ModeMixin):
    pass


class Notes(BaseModel):
    content: Union[str, None]
    color: str
    style:  str
    icon: Union[str, None]


class Timezone(BaseModel):
    mode: AutoManual
    value: Union[str, None] = None


class Locale(BaseModel):
    mode: AutoManual
    value: Union[str, None]


class Ports(BaseModel):
    mode: str
    blacklist: list[int]

    @field_validator('blacklist', mode='before')
    def _validate_blacklist(cls, value: str):
        return [int(value) for value in value.split(',')]


class Proxy(BaseModel):
    id: _NNT
    name: Union[str, None] = None
    type: Union[Literal['http', 'socks5', 'socks4'], None] = None
    host: Union[IP, None] = None
    saved_by_user: Union[bool, None] = None
    crypto_key_id: Union[PositiveInt, None] = None
    login: Union[str, None] = None
    password: Union[str, None] = None
    change_ip_url: Union[IP, None] = None


class Access(BaseModel):
    view: bool
    update: bool
    delete: bool
    share: bool
    usage: bool


class Geolocation(BaseModel):
    mode: AutoManual
    latitude: Union[str, None]
    longitude: Union[str, None]
    accuracy: Union[str, None]


class CPU(BaseModel):
    mode: RealManual
    value: int


class Memory(BaseModel):
    mode: AutoManual
    value: int


class Screen(BaseModel):
    mode: RealManual
    resolution: Union[Resolution, None]


class Connection(BaseModel):
    downlink: float
    effective_type: Literal['slow-2g', '2g', '3g', '4g', '5g']
    rtt: int
    saveData: bool


class MediaDevices(BaseModel):
    mode: RealManual
    audio_inputs: Union[list[str], None]
    video_inputs: Union[list[str], None]
    audioOutputs: Union[list[str], None]


class Extension(BaseModel):
    url: str
    type: str
    hash: str


class MacAddress(_ModeMixin):
    mode: str
    value: Union[str, None]


class DeviceName(_ModeMixin):
    value: Union[str, None] = None


class _Limits(BaseModel):
    max_bind_groups: int
    max_bindings_per_bind_group: int
    max_buffer_size: int
    max_color_attachment_bytes_per_sample: int
    max_color_attachments: int
    max_compute_invocations_per_workgroup: int
    max_compute_workgroup_size_x: int
    max_compute_workgroup_size_y: int
    max_compute_workgroup_size_z: int
    max_compute_workgroup_storage_size: int
    max_compute_workgroups_per_dimension: int
    max_dynamic_storage_buffers_per_pipeline_layout: int
    max_dynamic_uniform_buffers_per_pipeline_layout: int
    max_inter_stage_shader_components: int
    max_inter_stage_shader_variables: int
    max_sampled_textures_per_shader_stage: int
    max_samplers_per_shader_stage: int
    max_storage_buffer_binding_size: int
    max_storage_buffers_per_shader_stage: int
    max_storage_textures_per_shader_stage: int
    max_texture_array_layers: int
    max_texture_dimension_1d: int
    max_texture_dimension_2d: int
    max_texture_dimension_3d: int
    max_uniform_buffer_binding_size: int
    max_uniform_buffers_per_shader_stage: int
    max_vertex_attributes: int
    max_vertex_buffer_array_stride: int
    max_vertex_buffers: int
    min_storage_buffer_offset_alignment: int
    min_uniform_buffer_offset_alignment: int


class _Info(BaseModel):
    architecture: str
    description: str
    device: str
    vendor: str


class WebGPU(BaseModel):
    get_preferred_canvas_format: str
    limits: _Limits
    info: _Info
