"""User model for Kintone Users"""

from __future__ import annotations

from dataclasses import dataclass

from .base import _Model

@dataclass 
class CustomItemValue(_Model):
    """Class for Kintone Custom Item Values"""

    code: str
    value: str

@dataclass
class Organization(_Model):
    """Class for Kintone Organizations"""

    code: str
    description: str
    id: int
    localName: str
    localNameLocale: str
    name: str
    parentCode: str # Reference to another Organization

@dataclass
class Title(_Model):
    """Class for Kintone Titles"""

    code: str
    description: str
    id: int
    name: str

@dataclass
class Service(_Model):
    """Class for Kintone Services"""

    code: str           # User code
    services: list[str] # List of Service codes

@dataclass
class Group(_Model):
    """Class for Kintone Groups"""

    code: str
    description: str
    id: int
    name: str

@dataclass
class User(_Model):
    """Class for Kintone Users"""

    code: str
    birthDate: str # YYYY-MM-DD
    callto: str
    ctime: str # ISO 8601
    CustomItemValue: list[CustomItemValue]
    description: str
    email: str
    employeeNumber: str
    extensionNumber: str
    givenName: str
    givenNameReading: str
    id: int
    joinDate: str # YYYY-MM-DD
    localName: str
    localNameLocale: str
    locale: str
    mobilePhone: str
    mtime: str # ISO 8601
    name: str
    phone: str
    primaryOrganization: str
    sortOrder: int
    surName: str
    surNameReading: str
    timezone: str
    url: str
    valid: bool