"""Module for defining Kintone REST API endpoints"""

from typing import (
    Literal, 
    TypeAlias,
    Optional,
    Coroutine,
    Any,
)
from functools import wraps
from httpx import Response

from .handlers import HTTPX_Async, HTTPX_Sync



class Route:
    RequestType = Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

    def __init__(self, method: RequestType, endpoint: str, handler: HTTPX_Async | HTTPX_Sync):
        self.handler = handler
        self.method = method
        self.endpoint = endpoint 
     
    @property
    def url(self):
        return self.handler.client.base_url.join(self.endpoint)
       
    def __call__(self, **data): ...
    
    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'

class SyncRoute(Route):
    def __call__(self, **data) -> Response:
        if not isinstance(self.handler, HTTPX_Sync):
            raise AttributeError("Sync Routing requires a Sync Handler")
        
        if self.method == 'GET':
            return self.handler.get(self.url, data)
        
        elif self.method == 'POST':
            return self.handler.post(self.url, data)
        
        elif self.method == 'PATCH':
            return self.handler.patch(self.url, data)
        
        elif self.method == 'PUT':
            return self.handler.put(self.url, data)
        
        elif self.method == 'DELETE':
            return self.handler.delete(self.url, data)   
        return None

class AsyncRoute(Route):
    async def __call__(self, **data) -> Coroutine[Any, Any, Response]:
        if not isinstance(self.handler, HTTPX_Async):
            raise AttributeError("Async Routing requires an Async Handler")
        
        if self.method == 'GET':
            return await self.handler.get(self.url, data)
        
        elif self.method == 'POST':
            return await self.handler.post(self.url, data)
        
        elif self.method == 'PATCH':
            return await self.handler.patch(self.url, data)
        
        elif self.method == 'PUT':
            return await self.handler.put(self.url, data)
        
        elif self.method == 'DELETE':
            return await self.handler.delete(self.url, data)   
        return None
    

class Routes:
    """Class for defining Kintone REST API endpoints"""

    def __init__(self, handler: HTTPX_Sync) -> None:
        self.handler = handler
        self.base_url = handler.client.base_url
    
    def register_route(method: Route.RequestType, endpoint: str, body: dict) -> Route:
        """Wrapper that builds a Route object method from a method and endpoint"""
        def _wrapper(route):
            @wraps(route)
            def _wrapped(self, *args, **kwargs):
                if args:
                    arg_map = dict(zip(route.__annotations__.keys(), args))
                    kwargs.update(arg_map)
                return Route(method, endpoint.format(**kwargs), self.handler)
            return _wrapped
        return _wrapper




