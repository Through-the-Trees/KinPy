"""Module for defining Kintone REST API endpoints"""

from typing import (
    Literal, 
    TypeAlias,
    Optional,
)
from functools import wraps
from httpx import Response

from .handlers import HTTPX_Async, HTTPX_Sync



class Route:  
    RequestType: TypeAlias = Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
    
    def __init__(self, method: RequestType, endpoint: str, handler: HTTPX_Sync) -> None:
        self.handler = handler
        self.method = method
        self.endpoint = endpoint

    @property
    def url(self):
        return self.handler.client.base_url.join(self.endpoint)
    
    def __call__(self, **data) -> Response:
        with self.handler.endpoint_as(self.endpoint):
            if self.method == 'GET':
                return self.handler.get(data)
            
            elif self.method == 'POST':
                return self.handler.post(data)
            
            elif self.method == 'PATCH':
                return self.handler.patch(data)
            
            elif self.method == 'PUT':
                return self.handler.put(data)
            
            elif self.method == 'DELETE':
                return self.handler.delete(data)
                
        return None

    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'

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




