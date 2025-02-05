"""Module for creating HTTP handlers to be used with the rest of the package"""
from __future__ import annotations

from contextlib import contextmanager
from typing import (
    Protocol,
)
from functools import wraps
from httpx import Client, AsyncClient, Response, Auth, URL, Headers

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

class KintoneAuth(Auth):
    def __init__(self, token: str):
        self._token = token
        self._build_auth_header(token)

    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, new_token):
        self._token = new_token
        self._build_auth_header()
        
    def auth_flow(self, request):
       request.headers.update(self._auth_headers)
       yield request

    def _build_auth_header(self, token):
        self._auth_headers = Headers({
            "X-Cybozu-API-Token" : str(token)
        })
        
class HTTPX_Sync:
    """HTTPX Sync handler"""
    
    def __init__(self, client: Client, auth: KintoneAuth, **opts) -> None:
        client.auth = auth # Auth is required
        
        # Passthrough options to the handler
        for attr, val in opts.items():
            if hasattr(client, attr):
               setattr(client, attr, val)

        self.client = client
               
    def get(self, url: URL, **data) -> Response:
        return self.client.get(url, **data)

    def post(self, url: URL, **data) -> Response:
        return self.client.post(url, **data)

    def put(self, url: URL, **data) -> Response:
        return self.client.put(url, **data)

    def delete(self, url: URL, **data) -> Response:
        return self.client.delete(url, **data)

    def patch(self, url: URL, **data) -> Response:
        return self.client.patch(url, **data)
    
class HTTPX_Async:
    """HTTPX Async handler"""

    def __init__(self, client: AsyncClient, auth: KintoneAuth, **opts) -> None:
        client.auth = auth # Auth is required
        
        # Passthrough options to the handler
        for attr, val in opts.items():
            if hasattr(client, attr):
               setattr(client, attr, val) 
        
        self.client = client

    async def get(self, url: URL, **data) -> Response:
        return await self.client.get(url, **data)

    async def post(self, url: URL, **data) -> Response:
        return await self.client.post(url, **data)

    async def put(self, url: URL, **data) -> Response:
        return await self.client.put(url, **data)

    async def delete(self, url: URL, **data) -> Response:
        return await self.client.delete(url, **data)

    async def patch(self, url: URL, **data) -> Response:
        return await self.client.patch(url, **data)
