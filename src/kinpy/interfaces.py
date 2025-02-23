"""Main interfaces for Kintone API endpoints, All interfaces defined here are part of the public
API for KinPy and will be moderately stable across minor versions.

Any changes made during a major version bump will be documented in the release notes. and will be marked
with a depreciation warning in the previous minor version.
"""
from __future__ import annotations

from typing import (
    TypeVar, 
    Optional,
    Callable,
)

import functools

from httpx import Client as HTTPX_Client

from routes import Routes
from handlers import HTTPX_Async, HTTPX_Sync, KintoneAuth
from utils import QueryString

# TODO: Return type of a container property (e.g. .get_apps()) should be a bespoke container class
# That implements nice indexing and "select_by" methods. For reference see C# LINQ

class KTQueryable(list):
    """Extension of list that allows for simple querying of returned Kintone objects"""
    
    def pop_where(self, **kwargs):
        """Pop the first item that matches the key-value pair"""
        for i, item in enumerate(self):
            if all(getattr(item, key) == value for key, value in kwargs.items()):
                return self.pop(i)
        return None
    
    def select_where(self, **kwargs) -> KTQueryable:
        """Return a new KTQueryable with only items that match the key-value pair"""
        return KTQueryable(
            item 
            for item in self 
            if all(
                getattr(item, key) == value 
                for key, value in kwargs.items()
                )
            )
    
    def take(self, n: int) -> KTQueryable:
        """Return a new KTQueryable with the first n items 
        and pad with None if n > len(self).

        This allows for safe unpacking of the first n items in a list
        """
        if len(self) < n:
            return KTQueryable(self + [None] * (n - len(self)))
        return KTQueryable(self[:n])

    def query(self, func: Callable) -> KTQueryable:
        """Return a new KTQueryable with only items that match the function"""
        return KTQueryable(item for item in self if func(item))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return KTQueryable(super().__getitem__(key))
        return super().__getitem__(key)

class KintonePortal:
    def __init__(self, base_url: str, auth: KintoneAuth, sync: bool = True) -> None:
        # NOTE: Should auth be handled on a per-app basis?
        # API Keys only allow permissions within apps, to do anything to the greater Kintone portal, you need user/pass auth
        client = HTTPX_Client(base_url=base_url)
        if sync:
            self.handler = HTTPX_Sync(client, auth)
        else:
            self.handler = HTTPX_Async(client, auth)
        
        self.routes = Routes(self.handler)

    @property
    def apps(self) -> list:
        """Return a list of Apps"""
        route = self.routes.get_apps()

        return route()

class KTApp:
    def __init__(self, kintone_portal: KintonePortal, app_id: int) -> None:
        
        self._portal = kintone_portal
        self.app_id = app_id

        self.routes = Routes(self._portal.handler)
        # TODO: Implement user/pass auth for portal-level functions
        self.info = self._portal.routes.get_app(app_id)
        self.get_record = functools.partial(self._portal.routes.get_record, app=self.app_id)
        
    def get_records(self, fields: list[str], query: QueryString):
        self._portal.routes.get_records(app=self.app_id)