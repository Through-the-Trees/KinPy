from __future__ import annotations
from dataclasses import dataclass
from typing import (
    Literal,
)

from .constants import Status

@dataclass 
class UserRef:
    code: str
    name: str

@dataclass
class AppStatus:
    app: str
    status: Status

@dataclass
class AppResponse:
    appId: str
    code: str
    name: str
    description: str
    spaceId: str
    threadId: str
    createdAt: str  # ISO 8601
    creator: UserRef
    modifiedAt: str # ISO 8601
    modifier: UserRef
    
@dataclass
class DeployResponse:
    apps: list[AppStatus]