"""A Python interface for the Kintone REST API"""

__version__ = '0.0.1'

# Uncomment as interfaces are defined
from interfaces import (
   Kintone,
#    KTApp,
#    KTRecord,
#    KTField,
)

# Kintone Auth is required for initialization of the Kintone interface
from handlers import KintoneAuth