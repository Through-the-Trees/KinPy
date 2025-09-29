"""A Python interface for the Kintone REST API"""

__version__ = '0.0.1'

from .utils import QueryString

# Kintone Auth is required for initialization of the Kintone interface
from .handlers import KintoneAuth

# Uncomment as interfaces are defined
from .interfaces import (
   KintonePortal,
   KTApp,
#    KTRecord,
#    KTField,
)