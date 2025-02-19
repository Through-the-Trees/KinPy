"""Module for defining Kintone REST API endpoints"""

from typing import (
    Literal, 
    Coroutine,
    Any,
)
from functools import wraps
from httpx import Response

from handlers import HTTPX_Async, HTTPX_Sync
from utils import QueryString

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
       
    def __call__(self) -> Response | Coroutine[Any, Any, Response]:
        raise NotImplementedError("Route must be subclassed as SyncRoute or AsyncRoute")
    
    def __repr__(self):
        return f'<Route {self.method} {self.endpoint} for {self.handler}>'

class SyncRoute(Route):
    """Sync Route
    
    This class is used to define a synchronous route for making requests to the Kintone REST API
    
    Args:
        method: The route REST method (GET, POST, PATCH, PUT, DELETE)
        endpoint: The api endpoint minus the base url of the handler
        handler: The handler to use for the request
        opts: Optional parameters to pass to the Handler request method
        
    Returns:
        Route: A Route object for the defined endpoint that can be called to make a request
        
    Example:
        >>> route = SyncRoute('GET', '/k/v1/app.json', handler, params={'id': 1})
        >>> route()
        <Response [200 OK]>
    
    Example:
        >>> routes = [SyncRoute('GET', '/k/v1/app.json', handler, params={'id': i}) for i in range(1, 11)]
        >>> responses = [route() for route in routes] # Run requests synchronously
    """
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
    """Async Route
    
    This class is used to define an asynchronous route for making requests to the Kintone REST API
    
    Args:
        method: The route REST method (GET, POST, PATCH, PUT, DELETE)
        endpoint: The api endpoint minus the base url of the handler
        handler: The handler to use for the request
        opts: Optional parameters to pass to the Handler request method
        
    Returns:
        Route: A Route object for the defined endpoint that can be called to make a request
        
    Example:
        >>> route = AsyncRoute('GET', '/k/v1/app.json', handler, params={'id': 1})
        >>> await route()
        <Response [200 OK]>
        
    Example:
        >>> routes = [AsyncRoute('GET', '/k/v1/app.json', handler, params={'id': i}) for i in range(1, 11)]
        >>> responses = [await route() for route in routes] # Run requests concurrently
    """
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
    """Class for defining Kintone REST API endpoints
    
    Args:
        handler: The handler to use for the request
        
    Example:
        >>> handler = HTTPX_Sync('https://example.com', auth=KintoneAuth('<token>'))
        >>> routes = Routes(handler)
        >>> app_one = routes.get_app(1)
        >>> app_one()
        <Response [200 OK]>
    
    Example:
        >>> handler = HTTPX_Async('https://example.com', auth=KintoneAuth('<token>'))
        >>> routes = Routes(handler)
        >>> app_one = routes.get_app(1)
        >>> await app_one()
        <Response [200 OK]>
    """

    def __init__(self, handler: HTTPX_Async | HTTPX_Sync) -> None:
        self.handler = handler
    
    def register_route(method: Route.RequestType, endpoint: str, *,
                       required: tuple[str] = None, 
                       optional: tuple[str] = None,
                       **opts) -> Route:
        """Define a route using a function header and type hints
        
        Args:
            method: The route REST method (GET, POST, PATCH, PUT, DELETE)
            endpoint: The api endpoint minus the base url of the handler
            required: Required parameter keys
            optional: Optional parameter keys
            opts: Optional parameters to pass to the Handler request method
        
        Raises:
            ValueError: If required parameters are not passed
            ValueError: If invalid parameters are passed
            TypeError: If parameters do not match type hints
        
        Returns:
            Route: A Route object for the defined endpoint that can be called to make a request
        
        Danger:
            This decorator allows for both positional and keyword arguments to be passed to the method. 
            However, it is recommended to use keyword arguments for clarity, because a ValueError will be raised 
            if a parameter is specified both positionally and as a keyword.
            
        Example:
            >>> @register_route('GET', '/k/v1/app.json ', required=('id'))
            ... def get_app(self, id: int | str) -> SyncRoute | AsyncRoute: 
            ...    '''Get an App by ID'''
            ...    ...
            
            >>> get_app_one = get_app(1)
            >>> get_app_one
            <Route GET /k/v1/app.json for <HTTPX_Sync https://example.com>>
            >>> get_app_one()
            <Response [200 OK]>
        """
        def _wrapper(route):
            @wraps(route)
            def _wrapped(self, *args, **kwargs):
                
                # Convert positional to keyword
                if args:
                    # Zip up the positionals with the annotation keys (dict keys are ordered)
                    #
                    # NOTE: This will fail if the method has no annotations, so make sure you type hint
                    # Your method parameters
                    arg_map = dict(zip(_wrapped.__annotations__.keys(), args))
                    # Update kwargs with mapped args
                    # Raise a ValueError if a parameter is specified in both args and kwargs
                    for k, v in arg_map:
                        if k in kwargs:
                            raise ValueError(f"{k} is specified both positionally and as a keyword")
                        kwargs[k] = v
                
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
                
                # Validate param types against annotation hints
                for param, value in params.items():
                    if not isinstance(value, _wrapped.__annotations__[param]):
                        raise TypeError(
                            f"Expected {param} to be of type {_wrapped.__annotations__[param]}"
                            )
                
                if isinstance(self.handler, HTTPX_Sync):
                    return SyncRoute(method, endpoint, self.handler, params=params, **opts)
                
                if isinstance(self.handler, HTTPX_Async):
                    return AsyncRoute(method, endpoint, self.handler, params=params, **opts)
                
                raise AttributeError("Invalid Handler type, must be `HTTPX_Sync` or `HTTPS_Async`")
                
            return _wrapped
        return _wrapper

    @register_route('GET', '/k/v1/app.json ', required=('id'))
    def get_app(self, id: int | str) -> Route: 
        """Get an App by ID
        
        Args:
            id: The App ID to get (required)
        """
        ...

    @register_route('GET', '/k/v1/apps.json', optional=('ids', 'codes', 'name', 'spaceIds', 'limit', 'offset'))
    def get_apps(self, ids: list[int | str], codes: list[str], name: str, spaceIds: list[int | str], limit: int, offset: int) -> Route: 
        """Get Apps that match the specified criteria
        
        Args:
            ids: Sequence of App IDs to get (up to 100) (optional)
            codes: Sequence of App codes to get (up to 100) (optional)
            name: App name to get (partial match, case insensitive) (optional)
            spaceIds: Sequence of Space IDs to get (up to 100) (optional)
            limit: The number of apps to get (default: 100, max: 100) (optional)
            offset: The offset of the apps to get (default: 0, max: 2147483647) (optional)
        
        Note:
            All parameters are optional, but at least one must be specified for the request to be valid
        """
        ...
        # TODO: Implement all routes from here: https://kintone.dev/en/docs/kintone/rest-api/

