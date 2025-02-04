"""Module for defining query parameters for the Kintone API."""
from __future__ import annotations

from dataclasses import dataclass

from urllib.parse import quote_plus

from typing import (
    Required,
    Optional,
    MutableMapping,
    TypeAlias,
)

from .constants import (
    LanguageCode,
    QueryFunctions,
    QueryFunction,
)

from numbers import Number

class _Unset:
    """Class for unset query parameters.
    
    Note:
        The `__bool__` method is overridden to always return `False`
        This is to allow for the use of the `or` operator
        when setting default values for query parameters
    """
    
    def __bool__(self):
        return False
    
    def __repr__(self):
        return "<unset>"

Unset = _Unset()

class QueryString(str):
    """Class for building a query string.

    Note:
        This class is designed to be used with the `__and__` and `__or__` operators
        to allow for chaining of query strings.

    Example:
        >>> query = QueryString("field")
        >>> query = query.like("value") & query.not_in(["value1", "value2"])
        >>> print(query)
        field like 'value' and field not in ('value1', 'value2')

        >>> query.encode()
        'field+like+%27value%27+and+field+not+in+%28%27value1%27%2C+%27value2%27%29'
    """
    
    def __init__(self, field: str):
        self.value = field
        self.query = f"{field}"

    def __repr__(self):
        return self.query
    
    # URL encoding
    def encode(self, safe="", encoding = "utf-8", errors = "strict"):
        return quote_plus(self.query, encoding=encoding, errors=errors)

    # String comparisons
    def like(self, value: str):
        self.query = f"{self.value} like '{value}'"
        return self
    
    def not_like(self, value: str):
        self.query = f"{self.value} not like '{value}'"
        return self

    # Inclusion comparisons
    def in_(self, *values: str):
        self.query = f"{self.value} in ('{', '.join(str(v) for v in values)}')"
        return self
    
    def not_in(self, *values: str):
        self.query = f"{self.value} not in ('{', '.join(str(v) for v in values)}')"
        return self

    # Query Joins (These create new QueryString objects)
    def __and__(self, other: QueryString):
        return QueryString(f"{self.query} and {other}")
    
    def __or__(self, other: QueryString):
        return QueryString(f"{self.query} or {other}")
    
    # String/Number comparisons
    def __eq__(self, other: str):
        self.query = f"{self.value} = '{other}'"
        return self
    
    def __ne__(self, other: str):
        self.query = f"{self.value} != '{other}'"
        return self
    
    # Numeric comparisons
    def __lt__(self, val: Number):
        self.query = f"{self.value} < '{val}'"
        return self
    
    def __le__(self, val: Number):
        self.query = f"{self.value} <= '{val}'"
        return self
    
    def __gt__(self, val: Number):
        self.query = f"{self.value} > '{val}'"
        return self
    
    def __ge__(self, val: Number):
        self.query = f"{self.value} >= '{val}'"
        return self
    
@dataclass(eq=False)
class _Query:
    """Base class for query parameters.self.query = 
    
    Note:
        Implements the `__iter__` and `__getitem__` methods.
        To allow for unpacking
    
    Warning:
        The `__iter__` method will only yield key-value pairs
        where the value is not `Unset` sentinel
    """
    
    def __iter__(self):
        for key, value in self.__dict__.items():
            if value is not Unset:
                yield key, value
    
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def __len__(self):
        return sum(1 for _ in iter(self))

    def __str__(self):
        return str(dict(self))

@dataclass(eq=False)
class GetApp(_Query):
    """Query parameters for the App API.
    
    Args:
        id: The App ID. (Required)
    """
    id: Required[int | str]=Unset

@dataclass(eq=False)
class GetApps(_Query):
    """Query parameters for the App Multiple API.
    
    Note:
        When maximum number of retrievals is 100 per request
    
    Args:
        ids: The App IDs. (max 100)
        codes: List of App Codes. (max 100)
        name: App Name (Partial match, localized, case-insensitive)
        spaceIds: List of Space IDs. (max 100)
        limit: Maximum number of Apps to retrieve (1-100)
        offset: The number of retrievals that will be skipped. (o <= offset < 2147483647) (Default: 0)
    """
    ids: Optional[list[int]]=Unset
    codes: Optional[list[str]]=Unset
    name: Optional[str]=Unset
    spaceIds: Optional[list[int]]=Unset
    limit: Optional[int]=Unset
    offset: Optional[int]=Unset

@dataclass(eq=False)
class GetAppsStatus(_Query):
    """Query parameters for the App Status API.
    
    Args:
        apps: The App IDs. (Required)
    """
    apps: Required[list[int | str]]=Unset

@dataclass(eq=False)
class GetFields(_Query):
    """Query parameters for the Field API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetFormLayout(_Query):
    """Query parameters for the Form Layout API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetViews(_Query):
    """Query parameters for the Views API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetSettings(_Query):
    """Query parameters for the Settings API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetProcessManagement(_Query):
    """Query parameters for the Process Management API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetCustomization(_Query):
    """Query parameters for the Customization API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetPermissions(_Query):
    """Query parameters for the Permissions API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetFieldPermissions(_Query):
    """Query parameters for the Field Permissions API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetRecordPermissions(_Query):
    """Query parameters for the Record API.
    
    Args:
        app: The App ID. (Required)
        ids: The Record IDs. (Required) (max 100)
    """
    app: Required[int | str]=Unset
    ids: Required[list[int | str]]=Unset

@dataclass(eq=False)
class GetEvaluateRecordPermissions(_Query):
    """Query parameters for the Record API.
    
    Args:
        app: The App ID. (Required)
        ids: The Record IDs. (Required) (max 100)
    """
    app: Required[int | str]=Unset
    ids: Required[int | str]=Unset

@dataclass(eq=False)
class GetNotifications(_Query):
    """Query parameters for the Notifications API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetPerRecordNotifications(_Query):
    """Query parameters for the Notifications API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetReminderNotifications(_Query):
    """Query parameters for the Notifications API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetGraphSettings(_Query):
    """Query parameters for the Graph Settings API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetActionSettings(_Query):
    """Query parameters for the Action Settings API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetForm(_Query):
    """Query parameters for the Form API.

    Warning:
        This API is read-only. Use `GetFormLayout` or `GetFormFields` instead.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetAppPlugins(_Query):
    """Query parameters for the App Plugins API.
    
    Args:
        app: The App ID. (Required)
        lang: The language code. (Optional)
    """
    app: Required[int | str]=Unset
    lang: Optional[LanguageCode]=Unset

@dataclass(eq=False)
class GetAppAdminNotes(_Query):
    """Query parameters for the App Admin Notes API.
    
    Args:
        app: The App ID. (Required)
    """
    app: Required[int | str]=Unset

@dataclass(eq=False)
class GetRecord(_Query):
    """Query parameters for the Record API.
    
    Args:
        app: The App ID. (Required)
        id: The Record ID. (Required)
    """
    app: Required[int | str]=Unset
    id: Required[int | str]=Unset

@dataclass(eq=False)
class GetRecords(_Query):
    """Query parameters for the Record API.
    
    Args:
        app: The App ID. (Required)
        fields: The fields to retrieve. (Optional)
        ids: The Record IDs. (Required) (max 100)
    """
    app: Required[int | str]=Unset
    fields: Optional[list[str]]=Unset
    query: QueryString=Unset
    ids: Required[list[int | str]]=Unset
