from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
from typing import (
    Optional,
    Literal,
)

from .fields import Field

# Main datamodels for KinPy
# Interfaces inherit the attributes defined here and implement methods for the API

# Sentinel to allow passing None/null values to the API to delete data using PATCH

Unset = object()

# NOTE: As far as I know, Kintone only uses PUT requests though, so it's important to always
# Send the full object data back when updating a record



class Model:
    """Base of the datamodel, implements filtered access and defines methods used in interface implementation"""
    def __getitem__(self, key):
        """Override getitem so only set values are returned"""
        val = super().__getattribute__(key)
        if val is not Unset:
            return val
    
    def __getattribute__(self, name):
        if name not in self and name in self.__dict__.keys():
            # Value is Unset, return None/Falsy value
            return None
        
        # Allow super to handle all other cases
        return super().__getattribute__(name)

    def __iter__(self):
        """Override iter so only set values are returned"""
        return iter(
            key
            for key, val in self.__dict__.items()
            if val is not Unset
        )
    
    def __len__(self):
        """Override len so only set values are returned"""
        return sum(1 for _ in self.__iter__())
    
    def __contains__(self, key):
        """Override contains so only set values are returned"""
        return key in self.__dict__ and self.__dict__[key] is not Unset

    # Abstracts to be implemented with proper routing in interfaces
    def update(self) -> None: ...

    def refresh(self) -> None: ...

    @contextmanager
    def editor(self):
        """Context manager to allow updating a record.
        Refreshes the record before entering the context and updates it after exiting
        """
        self.refresh()
        yield self
        self.update()

# NOTE: When implementing a datamodel, use the Optional type hint to specify
# that the field is not required. Make sure you set the default value to `Unset`
# so that None/Null can be passes as a value to delete a value.

# Remember: Kintone only uses PUT requests, so always send the full object data back
# To do this, you take a record that was returned and update it with a partial record

# e.g. 
# new_record_info = Record(id=1, name="John Doe", age=30)
# old_record = kintone.get_record(1)
# with old_record.editor():
#   old_record.update(new_record_info)

@dataclass(eq=False)
class App(Model):
    appId: str = Unset
    code: str = Unset
    name: str = Unset
    spaceId: str = Unset
    threadId: str = Unset
    createdAt: str = Unset #  ISO 8601
    creator: UserId = Unset
    modifiedAt: str = Unset # ISO 8601
    modifier: UserId = Unset

@dataclass
class RecordItem(Model):
    name: str

@dataclass(eq=False)
class Record(Model):
    record: dict[str, Field]

@dataclass(eq=False)
class UserId(Model):
    code: str = Unset
    name: str = Unset

@dataclass(eq=False)
class ItemValue:
    code: str = Unset
    value: str = Unset

# This is the full gambit of responses, comment out the ones you don't need
@dataclass(eq=False)
class User(Model):
    birthDate: str = Unset # ISO 8601
    callto: str = Unset
    code: str = Unset
    ctime: str = Unset # ISO 8601
    customItemValues: list[ItemValue] = Unset
    description: str = Unset
    email: str = Unset
    employeeNumber: str = Unset
    extensionNumber: str = Unset
    givenName: str = Unset
    givenNameReading:str = Unset
    id: str = Unset
    joinDate: str = Unset # YYYY-MM-DD
    localName: str = Unset
    localNameLocale: str = Unset
    locale: str = Unset
    mobilePhone: str = Unset
    mtime: str = Unset # ISO 8601
    name: str = Unset
    phone: str = Unset
    primaryOrganization: Optional[str] = Unset
    sortOrder: int = Unset
    surName: str = Unset
    surNameReading: str = Unset
    timezone: str = Unset
    url: str = Unset
    valid: bool = Unset

@dataclass(eq=False)
class Group(Model):
    id: str = Unset
    code: str = Unset
    name:str = Unset
    description: str = Unset

@dataclass(eq=False)
class View(Model):
    type: Literal['LIST', 'CALENDAR', 'CUSTOM'] = Unset
    name: str = Unset
    id: str = Unset
    filterCond: str = Unset# A Query String
    sort: str = Unset # <FILED> asc/desc
    index: str = Unset
    fields: list[str] = Unset

@dataclass(eq=False)
class SpacePermissions(Model):
    createApp: Literal['EVERYONE', 'ADMIN'] = Unset

@dataclass(eq=False)
class Space(Model):
    id: str = Unset
    name: str = Unset
    defaultThread: str = Unset
    isPrivate: bool = Unset
    creator: UserId = Unset
    modifier: UserId = Unset
    memberCount: int = Unset
    coverType: Literal['BLOB', 'PRESET'] = Unset
    coverKey: str = Unset
    coverUrl: str = Unset
    body: str = Unset # HTML
    useMultiThread: bool = Unset
    isGuest: bool = Unset
    attachedApps: list[App] = Unset
    fixedMember: bool = Unset
    showAnnouncement: bool = Unset
    showThreadList: bool = Unset
    showAppList: bool = Unset
    showMemberList: bool = Unset
    showRelatedLinkList: bool = Unset
    permissions: SpacePermissions

@dataclass(eq=False)
class Thread(Model):
    id: str = Unset
    name: str = Unset
    body: str = Unset # HTML

@dataclass(eq=False)
class Form(Model):
    properties: list[Field]

@dataclass(eq=False)
class Layout(Model):
    type: str
    code: str
    fields: list[Field]

# API Info
@dataclass(eq=False)
class Info(Model):
    baseUrl: str
    apis: dict # JSON