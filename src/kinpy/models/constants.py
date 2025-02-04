"""Module for storing Kintone Constants"""

from typing import (
    Literal,
)

FieldType = Literal[
    "SINGLE_LINE_TEXT",
    "MULTI_LINE_TEXT",
    "RICH_TEXT",
    "NUMBER",
    "CALC",
    "RADIO_BUTTON",
    "CHECK_BOX",
    "MULTI_SELECT",
    "DROP_DOWN",
    "DATE",
    "TIME",
    "DATETIME",
    "FILE",
    "LINK",
    "USER_SELECT",
    "ORGANIZATION_SELECT",
    "GROUP_SELECT",
    "REFERENCE_TABLE",
    "SPACER",
    "GROUP",
    "SUBTABLE",
    "RECORD_NUMBER",
    "CREATOR",
    "CREATED_TIME",
    "MODIFIER",
    "UPDATED_TIME",
    "__ID__",         # Special field for record ID
    "__REVISION__",   # Special field for record revision
]

FieldTypes: tuple[str] = FieldType.__args__

LanguageCode = Literal[
    "default",
    "en",
    "ja",
    "zh",
    "user",
    ]

LanguageCodes: tuple[str] = LanguageCode.__args__

QueryFunction = Literal[
    "LOGINUSER()",
    "PRIMARY_ORGANIZATION()",
    "NOW()",
    "TODAY()",
    "YESTERDAY()",
    "TOMORROW()",
    "FROM_TODAY({number},{period})",
    "THIS_WEEK()",
    "LAST_WEEK()",
    "NEXT_WEEK()",
    "THIS_MONTH({day})",
    "LAST_MONTH({day})",
    "NEXT_MONTH({day})",
    "THIS_YEAR()",
    "LAST_YEAR()",
    "NEXT_YEAR()",
]

QueryFunctions: tuple[str] = QueryFunction.__args__
