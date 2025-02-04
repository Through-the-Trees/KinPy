"""Module for creating HTTP handlers to be used with the rest of the package"""
from __future__ import annotations

from contextlib import contextmanager
from typing import (
    Protocol,
)
from functools import wraps
from httpx import Client, AsyncClient, Response, BasicAuth

class BaseHTTPHandler_Sync(Protocol):
    """Base class for Sync HTTP handlers"""

    def get(self, url: str) -> ... :
        """Send a GET request"""
        ...

    def post(self, url: str, data: dict) -> ... :
        """Send a POST request"""
        ...

    def put(self, url: str, data: dict) -> ... :
        """Send a PUT request"""
        ...

    def delete(self, url: str) -> ... :
        """Send a DELETE request"""
        ...

    def patch(self, url: str, data: dict) -> ... :
        """Send a PATCH request"""
        ...

    @contextmanager
    def endpoint_as(endpoint: str):
        """Context manager for setting the endpoint"""
        ...

class BaseHTTPHandler_Async(Protocol):
    """Base class for Async HTTP handlers"""

    async def get(self, url: str) -> ... :
        """Send awaitable GET request"""
        ...

    async def post(self, url: str, data: dict) -> ... :
        """Send a POST request"""
        ...

    async def put(self, url: str, data: dict) -> ... :
        """Send a PUT request"""
        ...

    async def delete(self, url: str) -> ... :
        """Send a DELETE request"""
        ...

    async def patch(self, url: str, data: dict) -> ... :
        """Send a PATCH request"""
        ...
    
    @contextmanager
    def endpoint_as(endpoint: str):
        """Context manager for setting the endpoint"""
        ...

class HTTPX_Sync:
    """HTTPX Sync handler"""

    def __init__(self, client: Client, auth: BasicAuth) -> None:
        self.client = client
        self.auth = auth

    def get(self, url: str) -> Response:
        return self.client.get(url, auth=self.auth)

    def post(self, url: str, data: dict) -> Response:
        return self.client.post(url, json=data, auth=self.auth)

    def put(self, url: str, data: dict) -> Response:
        return self.client.put(url, json=data, auth=self.auth)

    def delete(self, url: str) -> Response:
        return self.client.delete(url, auth=self.auth)

    def patch(self, url: str, data: dict) -> Response:
        return self.client.patch(url, json=data, auth=self.auth)
    
    @contextmanager
    def endpoint_as(self, endpoint: str):
        """Context manager for setting the endpoint"""
        original_endpoint = self.client.base_url
        self.client.base_url = endpoint
        try:
            yield
        finally:
            self.client.base_url = original_endpoint
    
class HTTPX_Async:
    """HTTPX Async handler"""

    def __init__(self, client: AsyncClient, auth: BasicAuth) -> None:
        self.client = client
        self.auth = auth

    @property
    def endpoint(self):
        return self.client.base_url

    async def get(self, url: str) -> Response:
        return await self.client.get(str(self.endpoint), auth=self.auth)

    async def post(self, url: str, data: dict) -> Response:
        return await self.client.post(str(self.endpoint), json=data, auth=self.auth)

    async def put(self, url: str, data: dict) -> Response:
        return await self.client.put(str(self.endpoint), json=data, auth=self.auth)

    async def delete(self, url: str) -> Response:
        return await self.client.delete(str(self.endpoint), auth=self.auth)

    async def patch(self, url: str, data: dict) -> Response:
        return await self.client.patch(str(self.endpoint), json=data, auth=self.auth)
    
    @contextmanager
    def endpoint_as(self, endpoint: str):
        """Context manager for setting the endpoint"""
        original_endpoint = self.client.base_url
        self.client.base_url = endpoint
        try:
            yield
        finally:
            self.client.base_url = original_endpoint
