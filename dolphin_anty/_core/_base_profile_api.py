from __future__ import annotations

import json
from datetime import datetime
from typing import Annotated, Any, Sequence, Mapping, Optional, Union
from pydantic import ConfigDict, AliasGenerator, BeforeValidator, field_validator, NonNegativeInt
from pydantic.fields import Field
from dolphin_anty.types import (Platform, WebRTC, Canvas, WebGL, WebGLInfo, ClientRect, Notes, Timezone,
                                Locale, Ports, Proxy, Access, Geolocation, CPU, Memory, Screen,
                                MediaDevices, AnyVersion, DeviceName, MacAddress, WebGPU)
from sensei import APIModel, camel_case


class BaseProfileAPI(APIModel):
    model_config = ConfigDict(alias_generator=AliasGenerator(validation_alias=camel_case))

    id: NonNegativeInt
    team_id: NonNegativeInt
    user_id: NonNegativeInt
    name: str
    platform: Platform
    device_name: DeviceName
    webgpu: WebGPU
    mac_address: MacAddress
    is_hidden_profile_name: bool
    browser_type: str
    main_website: Optional[str]
    useragent: Annotated[str, BeforeValidator(lambda x: x['value'])]
    webrtc: WebRTC
    canvas: Canvas
    webgl: WebGL
    webgl_info: WebGLInfo
    client_rect: ClientRect
    notes: Notes
    timezone: Timezone
    locale: Locale
    tabs: Optional[list[str]]
    ports: Ports
    proxy_id: NonNegativeInt
    proxy: Optional[Proxy]
    access: Access
    geolocation: Geolocation
    cpu: CPU
    memory: Memory
    platform_name: str
    cpu_architecture: str
    tags: Optional[list[str]]
    os_version: str
    screen: Screen
    vendor_sub: Optional[str]
    product_sub: int
    vendor: str
    product: str
    do_not_track: bool
    args: Optional[list]
    app_code_name: str
    media_devices: MediaDevices
    user_fields: Optional[str]
    storage_path: Optional[str]
    platform_version: AnyVersion
    extensions_new_naming: bool
    login: Optional[str]
    password: Optional[str]
    homepages: Optional[list[str]]
    created_at: datetime = Field(validation_alias='created_at')
    deleted_at: Optional[datetime] = Field(validation_alias='deleted_at')
    updated_at: datetime = Field(validation_alias='updated_at')
    total_session_duration: NonNegativeInt
    screen_width: Optional[NonNegativeInt]
    screen_height: Optional[NonNegativeInt]
    connection_downlink: NonNegativeInt
    connection_effective_type: str
    connection_rtt: NonNegativeInt
    connection_save_data: int
    datadir_hash: Optional[str]
    cookies_hash: Optional[str]
    archived: int
    webgl2_maximum: Optional[str]
    sorting_name: str
    added_sorting_name: bool
    transfer: int
    recover_count: Optional[str]
    last_start_time: Optional[str]
    tags_with_separator: Optional[list[str]] = Field(alias='tags_with_separator')
    pinned: bool
    folder: Optional[str]

    @field_validator('*', mode='before')
    def _transform_empty_collections(cls, value: Any):
        if isinstance(value, (Sequence, Mapping)) and not value:
            return None
        return value

    @field_validator('webgpu', mode='before')
    def _transform_webgpu(cls, value: Any):
        def from_json(value: Union[str, dict]):
            if isinstance(value, str):
                return json.loads(value)

            if not isinstance(value, dict):
                raise ValueError('Invalid webgpu value')
            else:
                return value

        value = from_json(value)
        value = from_json(value['value'])
        value = from_json(value)

        return value
