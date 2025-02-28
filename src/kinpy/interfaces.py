"""Main interfaces for Kintone API endpoints, All interfaces defined here are part of the public
API for KinPy and will be moderately stable across minor versions.

Any changes made during a major version bump will be documented in the release notes. and will be marked
with a depreciation warning in the previous minor version.
"""
from __future__ import annotations

from typing import (
    Any,
    TypeVar, 
    Optional,
    Callable,
)

import functools

import json

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

    # TODO: Implement user/pass auth for portal-level functions
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

        # TODO: Reformat these to match get_records execution pattern
        # TODO: Implement user/pass auth for portal-level functions
        self.info = self._portal.routes.get_app(app_id)

    def get_record(self, id: int) -> dict[str, Any]:
        """Get record by $id"""
        route = self._portal.routes.get_record(app=self.app_id, id=id)
        response: dict = json.loads(route().content)
        if 'record' not in response:
            return None

        record: dict[str, Any] = \
        {
            key: value['value']
            for key, value in response['record'].items()
        }

        return record

    # TODO: Implement record and field data models here
    # Is there any way to make the class definition dynamic such that I can arbitrarily pass kwargs with field names?
    def get_records(self, fields: list[str], query: QueryString = QueryString(''), _last_record_id: int = None) -> list[dict[str, Any]]:
        """Runs a bulk set of requests to retrieve records (one API call per 500 records)"""
        
        chunk_size = 500
        order_and_limit = QueryString(f'order by $id asc limit {chunk_size}')

        # Recursive query appended each iteration
        bulk_query = QueryString(f'$id > {_last_record_id}') if _last_record_id else QueryString('')

        query: QueryString = query & bulk_query

        route = self._portal.routes.get_records(
            app = self.app_id,
            fields = ','.join(fields + ['$id']),
            query = str(query + order_and_limit),
            totalCount = True
        )

        response: dict = json.loads(route().content)

        if 'records' not in response:
            return None

        # Simplify record structure into simple dict
        # ['field_name': value, ...]
        records: list[ dict[str, Any] ] = \
        [
            {
                key: value['value']
                for key, value in record.items()
            }
            for record in response['records']
        ]
        
        # Total count of records matching query (only max of 500 returned)
        total_count = int(response['totalCount'])
        if total_count > chunk_size:
            last_record_id = max(int(record['$id']) for record in records)
            return records + self.get_records(fields, query, last_record_id)
        else:
            return records
    
    def update_record(self, record: dict[str, Any]):
        """Update specified record ($id needs to be specified)"""

        # Re-structure record in API-friendly format
        record_update: dict[str, dict[str, Any] ] = \
        {
            k: {'value': v}
            for k, v in record.items() if k != '$id'
        }

        route = self._portal.routes.update_record(app=self.app_id, id=record['$id'], record=record_update)
        response: dict = json.loads(route().content)

        return response

