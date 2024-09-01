import json
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Self
from dolphin_anty.types import (Platform, WebRTC, Canvas, WebGL, WebGLInfo, ClientRect, Notes, Timezone,
                                Locale, Ports, Proxy, Access, Geolocation, CPU, Memory, Screen, Connection,
                                MediaDevices, AnyVersion, Extension,
                                _BaseModel, Status, DeviceName, MacAddress, WebGPU, HandlingTuple)
from datetime import datetime
from pydantic import field_validator


class _BaseProfileAPI(_BaseModel, ABC):
    id: int
    team_id: int
    user_id: int
    name: str
    platform: Platform
    device_name: DeviceName
    webgpu: WebGPU
    mac_address: MacAddress
    is_hidden_profile_name: bool
    browser_type: str
    main_website: str
    useragent: str
    webrtc: WebRTC
    canvas: Canvas
    webgl: WebGL
    webgl_info: WebGLInfo
    client_rect: ClientRect
    notes: Notes
    timezone: Timezone
    locale: Locale
    tabs: list[str] | None = None
    ports: Ports
    proxy_id: int
    proxy: Proxy | None = None
    access: Access
    geolocation: Geolocation
    cpu: CPU
    memory: Memory
    platform_name: str
    cpu_architecture: str
    tags: list[str] | None = None
    os_version: str
    screen: Screen
    connection: Connection
    vendor_sub: str
    product_sub: str
    vendor: str
    product: str
    do_not_track: bool
    args: list
    app_code_name: str
    created_at: datetime
    updated_at: datetime
    media_devices: MediaDevices
    user_fields: str | None = None
    status: Status | None = None
    storage_path: str
    last_running_time: str | None = None
    last_runned_by_user_id: int | None
    last_run_uuid: UUID | None = None
    running: bool
    platform_version: AnyVersion
    ua_full_version: AnyVersion
    extensions_new_naming: bool
    login: str
    password: str
    bookmarks: list[str]
    extensions: list[Extension]
    homepages: list[str]

    def __str__(self):
        str_ = f'{self.__class__.__name__}(id={self.id}; name="{self.name}")'
        return str_

    @field_validator('webgpu')
    def _translate_json(cls, value: dict):
        value['value'] = json.loads(value['value'])
        return value

    @classmethod
    @abstractmethod
    def get(
            cls,
            id_: int
    ) -> Self:
        pass

    @classmethod
    def _get(cls, id_: int) -> HandlingTuple:
        path = f'/browser_profiles/{id_}'


