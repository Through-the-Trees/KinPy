from __future__ import annotations
from urllib.parse import quote
from numbers import Number

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
        'field%20like%20%27value%27%20and%20field%20not%20in%20%28%27value1%27%2C%20%27value2%27%29'
    """
    
    def __init__(self, field: str):
        self.value = field
        self.query = f"{field}"

    def __repr__(self):
        return self.query
    
    # URL encoding
    def encode(self, safe="", encoding = "utf-8", errors = "strict"):
        return quote(self.query, encoding=encoding, errors=errors)

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
    def __add__(self, other: QueryString):
        """Useful for appending order by, limit, etc."""
        if self and other:
            return QueryString(f"{self.query} {other.query}")
        return QueryString( str(self.query) + str(other.query) )
    def __and__(self, other: QueryString):
        if self and other:
            return QueryString(f"{self.query} and {other.query}")
        return self + other
    
    def __or__(self, other: QueryString):
        if self and other:
            return QueryString(f"{self.query} or {other.query}")
        return self + other
    
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