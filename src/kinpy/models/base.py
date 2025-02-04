"""Module for defining Kintone REST API data models"""
from __future__ import annotations

from dataclasses import dataclass

@dataclass(eq=False)
class _Model:
    """Base class for Kintone data models"""
    pass

@dataclass(eq=False)
class App(_Model):
    """Class for Kintone Apps"""
    
    appId: int
    code: str
    name: str
    description: str
    spaceId: int
    threadId: int
    createdAt: str  # ISO 8601
    creator: str    # User code
    modifiedAt: str # ISO 8601
    modifier: str   # User code
