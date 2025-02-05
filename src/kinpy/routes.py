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
from .utils import QueryString

class Route:
    RequestType = Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']

    def __init__(self, method: RequestType, endpoint: str, handler: HTTPX_Async | HTTPX_Sync, **opts):
        self.handler = handler
        self.method = method
        self.endpoint = endpoint 
        self.opts = opts
     
    @property
    def url(self):
        return self.handler.client.base_url.join(self.endpoint)
       
    def __call__(self): ...
    
    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'

class SyncRoute(Route):
    def __call__(self) -> Response:
        if not isinstance(self.handler, HTTPX_Sync):
            raise AttributeError("Sync Routing requires a Sync Handler")
        
        if self.method == 'GET':
            return self.handler.get(self.url, **self.opts)
        
        elif self.method == 'POST':
            return self.handler.post(self.url, **self.opts)
        
        elif self.method == 'PATCH':
            return self.handler.patch(self.url, **self.opts)
        
        elif self.method == 'PUT':
            return self.handler.put(self.url, **self.opts)
        
        elif self.method == 'DELETE':
            return self.handler.delete(self.url, **self.opts)   
        return None

class AsyncRoute(Route):
    async def __call__(self) -> Coroutine[Any, Any, Response]:
        if not isinstance(self.handler, HTTPX_Async):
            raise AttributeError("Async Routing requires an Async Handler")
        
        if self.method == 'GET':
            return await self.handler.get(self.url, **self.opts)
        
        elif self.method == 'POST':
            return await self.handler.post(self.url, **self.opts)
        
        elif self.method == 'PATCH':
            return await self.handler.patch(self.url, **self.opts)
        
        elif self.method == 'PUT':
            return await self.handler.put(self.url, **self.opts)
        
        elif self.method == 'DELETE':
            return await self.handler.delete(self.url, **self.opts)   
        return None
    


class Routes:
    """Class for defining Kintone REST API endpoints"""

    def __init__(self, handler: HTTPX_Async | HTTPX_Sync) -> None:
        self.handler = handler
    
    def register_route(method: Route.RequestType, endpoint: str, *,
                       required: tuple[str] = None, 
                       optional: tuple[str] = None,
                       **opts) -> Route:
        """Wrapper that builds a Route object method from a method and endpoint
        
        Args:
            method: The route REST method (GET, POST, PATCH, PUT, DELETE)
            endpoint: The api endpoint minus the base url of the handler
            required: Required parameter keys
            optional: Optional parameter keys
            opts: Optional parameters to pass to the Handler request method
        """
        def _wrapper(route):
            @wraps(route)
            def _wrapped(self, **kwargs):
                
                # Build param sets
                kwarg_set = set(kwargs.keys())
                required_set = set(required)
                optional_set = set(optional)
                param_set = required_set.union(optional_set)
                
                # Validate required params
                if not required_set.issubset(kwarg_set):
                    raise ValueError(
                        f"Request requires these params: {required_set.difference(kwarg_set)}"
                        )
                
                # Validate passed params
                if not kwarg_set.issubset(param_set):
                    raise ValueError(
                        f"Invalid parameters: {kwarg_set.difference(param_set)}"
                        )
                
                # Build params
                params = {}
                for param, value in kwargs.items():
                    # Encode query strings
                    if isinstance(value, QueryString):
                        value = value.encode()
                    params[param] = value
                
                if isinstance(self.handler, HTTPX_Sync):
                    return SyncRoute(method, endpoint, self.handler, params=params, **opts)
                
                if isinstance(self.handler, HTTPX_Async):
                    return AsyncRoute(method, endpoint, self.handler, params=params, **opts)
                
                raise AttributeError("Invalid Handler type, must be `HTTPX_Sync` or `HTTPS_Async`")
                
            return _wrapped
        return _wrapper

    @register_route('GET', '/k/v1/app.json ', required=('id'))
    def get_app(self, id: int | str) -> SyncRoute | AsyncRoute: 
        """Get an App by ID"""
        ...

    @register_route('GET', '/k/v1/apps.json', optional=('ids', 'codes', 'name', 'spaceIds', 'limit', 'offset'))
    def get_apps(self, ids: list[int | str], codes: list[str], name: str, spaceIds: list[int | str], limit: int, offset: int) -> SyncRoute | AsyncRoute: 
        """Get Apps by conditions
        
        Args:
            ids: List of App Ids to search for
            codes: List of app codes to search for
            name: Return all apps with this name (partial search, case-insensitive)
            spaceIds: List of spaceIds to check for apps in
            limit: Limit apps returned (100 max)
            offset: Pagination offset
            
        Note:
            All array parameters have a size limit of 100, and only 100 apps can be returned at a time
        """
        ...
