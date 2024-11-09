from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Sequence, Mapping, Optional, Union, List
from pydantic import field_validator, NonNegativeInt
from pydantic.fields import Field
from dolphin_anty.types import (Platform, WebRTC, Canvas, WebGL, WebGLInfo, ClientRect, Notes, Timezone,
                                Locale, Ports, Proxy, Access, Geolocation, CPU, Memory, Screen,
                                MediaDevices, AnyVersion, DeviceName, MacAddress, WebGPU, Useragent)
from ._base_model import BaseModel


class ProfileInfo(BaseModel):
    id: Optional[NonNegativeInt] = None
    team_id: Optional[NonNegativeInt] = None
    user_id: Optional[NonNegativeInt] = None
    name: Optional[str] = None
    platform: Optional[Platform] = None
    device_name: Optional[DeviceName] = None
    webgpu: Optional[WebGPU] = None
    mac_address: Optional[MacAddress] = None
    is_hidden_profile_name: Optional[bool] = None
    browser_type: Optional[str] = "anty"
    main_website: Optional[str] = None
    useragent: Useragent = Useragent()
    webrtc: Optional[WebRTC] = None
    canvas: Optional[Canvas] = None
    webgl: Optional[WebGL] = None
    webgl_info: Optional[WebGLInfo] = None
    client_rect: Optional[ClientRect] = None
    notes: Optional[Notes] = None
    timezone: Optional[Timezone] = None
    locale: Optional[Locale] = None
    tabs: Optional[List[str]] = None
    ports: Optional[Ports] = None
    proxy_id: Optional[NonNegativeInt] = None
    proxy: Optional[Proxy] = None
    access: Optional[Access] = None
    geolocation: Optional[Geolocation] = None
    cpu: Optional[CPU] = None
    memory: Optional[Memory] = None
    platform_name: Optional[str] = None
    cpu_architecture: Optional[str] = None
    tags: Optional[list[str]] = None
    os_version: Optional[str] = None
    screen: Optional[Screen] = None
    vendor_sub: Optional[str] = None
    vendor: Optional[str] = None
    product: Optional[str] = None
    do_not_track: Optional[bool] = None
    args: Optional[list] = None
    app_code_name: Optional[str] = None
    media_devices: Optional[MediaDevices] = None
    user_fields: Optional[str] = None
    storage_path: Optional[str] = None
    platform_version: Optional[AnyVersion] = None
    extensions_new_naming: Optional[bool] = None
    login: Optional[str] = None
    password: Optional[str] = None
    homepages: Optional[list[str]] = None
    updated_at: Optional[datetime] = Field(default=None, validation_alias='updated_at')
    created_at: Optional[datetime] = Field(default=None, validation_alias='created_at')

    @field_validator('*', mode='before')
    def _transform_empty_collections(cls, value: Any):
        if isinstance(value, (Sequence, Mapping)) and not value:
            return None
        return value

    @field_validator('webgpu', mode='before')
    def _transform_webgpu(cls, value: Any):
        if value in (None, ''):
            return None

        def from_json(value: Union[str, dict]):
            if isinstance(value, str):
                return json.loads(value)

            if not isinstance(value, dict):
                raise ValueError('Invalid webgpu value')
            else:
                return value

        value = from_json(value)

        try:
            value = from_json(value['value'])
            value = from_json(value)
        except KeyError:
            pass

        return value
