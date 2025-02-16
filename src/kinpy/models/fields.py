"""Submodule for defining Kintone Fields"""

from __future__ import annotations
from dataclasses import dataclass

from typing import (
    Literal,
)

Unset = object()

FieldType = Literal[
        'CALC',
        'CATEGORY',
        'CHECK_BOX',
        'CREATED_TIME',
        'CREATOR',
        'DATE',
        'DATETIME',
        'DROP_DOWN',
        'FILE',
        'HR',
        'LABEL',
        'LINK',
        'MODIFIER',
        'MULTI_LINE_TEXT',
        'MULTI_SELECT',
        'NUMBER',
        'RADIO_BUTTON',
        'RECORD_NUMBER',
        'REFERENCE_TABLE',
        'RICH_TEXT',
        'SINGLE_LINE_TEXT',
        'SPACER',
        'STATUS',
        'STATUS_ASSIGNEE',
        'SUBTABLE',
        'TIME',
        'UPDATED_TIME',
        'USER_SELECT',
        'ORGANIZATION_SELECT',
        'GROUP_SELECT',
        '__ID__',
        '__REVISION__',
        'GROUP',
        'HR',
        '_LOOKUP',    # Added for internal use, all lookups are either Single Line Text or Number fields
    ]

FieldTypes: list[str] = FieldType.__args__

@dataclass
class Field[T]:
    """Base class for all field types
    using Field[T] allows for type hinting of the value attribute

    Example:
    ```python
    @dataclass
    class StringField(Field[str]): ...

    @dataclass
    class IntegerField(Field[int]): ...

    str_field = StringField()
    int_field = IntegerField()

    int_field.value  # hinted as a int
    str_field.value  # hinted as a str
    ```
    """
    type: FieldType = Unset
    value: T = Unset

@dataclass
class RecordNumber(Field):
    name: str = Unset
    code: str = Unset
    noLabel: bool = Unset

@dataclass
class RecordId(Field): # Partially Documented
    label: str = Unset 

@dataclass
class Revision(Field): ... # Undocumented

@dataclass
class CreatedBy(Field):
    name: str = Unset
    code: str = Unset
    noLabel: bool = Unset

@dataclass
class CreatedDatetime(Field):
    name: str = Unset
    code: str = Unset
    noLabel: bool = Unset

@dataclass
class UpdatedBy(CreatedBy): ...

@dataclass
class UpdatedDatetime(CreatedDatetime): ...


# Custom Fields

@dataclass
class Text(Field):
    label: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    unique: bool = Unset
    maxLength: int = Unset
    minLength: int = Unset
    defaultValue: str = Unset
    expression: str = Unset
    hideExpression: bool = Unset


@dataclass 
class TextArea(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    defaultValue: str = Unset

@dataclass
class RichText(TextArea): ...
    
@dataclass
class Number(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    unique: bool = Unset
    maxValue: int = Unset
    minValue: int = Unset
    defaultValue: int = Unset
    digit: int = Unset
    displayScale: int = Unset

@dataclass
class Calculated(Field):
    name: str = Unset
    code: str = Unset
    required: bool = False
    noLabel: bool = Unset
    expression: str = Unset
    format: str = Unset
    displayScale: int = Unset
    hideExpression: bool = Unset


@dataclass
class CheckBox(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    defaultValue: bool = Unset
    options: list[str] = Unset

@dataclass
class RadioButton(CheckBox):
    required: bool = True

@dataclass
class MultiChoice(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    defaultValue: list[str] = Unset
    options: list[str] = Unset

@dataclass
class Dropdown(MultiChoice): ...

@dataclass
class UserSelection(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset

@dataclass
class DepartmentSelection(UserSelection): ...

@dataclass
class GroupSelection(UserSelection): ...

@dataclass
class Date(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    unique: bool = Unset
    defaultValue: str = Unset
    defaultExpression: str = Unset

@dataclass
class Time(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    defaultValue: str = Unset
    defaultExpression: str = Unset

@dataclass
class DateAndTime(Date): ...

@dataclass
class Link(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    unique: bool = Unset
    protocol: Literal['WEB', 'CALL', 'MAIL'] = Unset
    maxLength: int = Unset
    minLength: int = Unset
    defaultValue: str = Unset

@dataclass
class Attachment(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset

# NOTE: Lookup fields are determined by their field code and
#       can be either a Single Line Text or Number field
#       Also, there is a Field Type of Key Field attribute
#       that has an undocumented key
@dataclass
class Lookup(Field):
    name: str = Unset
    code: str = Unset
    required: bool = Unset
    noLabel: bool = Unset
    relatedApp: str = Unset
    _keyFieldType: str = Unset # Find out what this actually is

@dataclass
class Table(Field):
    code: str = Unset
    fields: list[Field] = Unset

@dataclass
class RelatedRecords(Field):
    name: str = Unset
    code: str = Unset
    noLabel: bool = Unset

@dataclass
class Categories(Field): ... # Undocumented

@dataclass
class Status(Field): ... # Undocumented

@dataclass
class Assignee(Field): ... # Undocumented


# Un-retrievable / Aesthetic Fields

@dataclass
class Label(Field):
    name: str = Unset

@dataclass
class BlankSpace(Field):
    elementId: str = Unset

@dataclass
class Border(Field): ...

@dataclass
class FieldGroup(Field): ... # Undocumented


# Type map used to initialize the correct field object on request
FieldTypeMap: dict[str, type[Field]] = {
"RECORD_NUMBER": RecordNumber,
"__ID__": RecordId,
"__REVISION__": Revision,
"CREATOR": CreatedBy,
"CREATED_TIME": CreatedDatetime,
"MODIFIER": UpdatedBy,
"UPDATED_TIME": UpdatedDatetime,
"SINGLE_LINE_TEXT": Text,
"MULTI_LINE_TEXT": TextArea,
"RICH_TEXT": RichText,
"NUMBER": Number,
"CALC": Calculated,
"CHECK_BOX": CheckBox,
"RADIO_BUTTON": RadioButton,
"MULTI_SELECT": MultiChoice,
"DROP_DOWN": Dropdown,
"USER_SELECT": UserSelection,
"ORGANIZATION_SELECT": DepartmentSelection,
"GROUP_SELECT": GroupSelection,
"DATE": Date,
"TIME": Time,
"DATETIME": DateAndTime,
"LINK": Link,
"FILE": Attachment,
"_LOOKUP": Lookup,  # _LOOKUP needs to be set manually during creation
"SUBTABLE": Table,
"REFERENCE_TABLE": RelatedRecords,
"CATEGORY": Categories,
"STATUS": Status,
"STATUS_ASSIGNEE": Assignee,
"LABEL": Label,
"SPACER": BlankSpace,
"HR": Border,
"GROUP": FieldGroup,
}
