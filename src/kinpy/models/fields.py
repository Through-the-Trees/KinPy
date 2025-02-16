"""Submodule for defining Kintone Fields"""

from __future__ import annotations
from dataclasses import dataclass

from typing import (
    Literal,
)

Unset = object()

FieldType = Literal[
        'CALC',
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
        'SUBTABLE'
        'TIME',
        'UPDATED_TIME',
        'USER_SELECT',
        'ORGANIZATION_SELECT',
        'GROUP_SELECT',
        '__ID__',
        '__REVISION__',
        '_LOOKUP',    # Added for internal use, all lookups are either Single Line Text or Number fields
    ]
FieldTypes: list[str] = FieldType.__args__

class Field:
    _type: FieldType = None

    def __init__(self, field_info: dict[str, dict[str, str]]):
        
        # Some field responses embed the code in the object
        if 'code' in field_info:
            data: dict[str, str] = field_info
            self.code = data.pop('code')

        # Other responses use the code as the key
        else:
            self.code, data = field_info.popitem()

        # type is always set   
        self.type: FieldType = data.pop('type', None)
        
        # value is set when accessing a record
        self.value: dict = data.pop('value', None)

        # Below values are set when accessing a Layout
        self.label:str = data.pop('label',None)
        self.elementId = data.pop('elementId', None)
        
        # Flatten size into Field attributes
        size: dict = data.pop('size', None)
        if size:
            self.width: float = size.pop('width', None)
            self.height: float = size.pop('height', None)
            self.innerHeight: float = size.pop('innerHeight', None)
        
        # Store remaining response values in a private attribute
        self._data = data

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.code} ({self.type})>'

@dataclass
class RecordNumber(Field):
    _type = 'RECORD_NUMBER'

@dataclass
class RecordId(Field):
    _type = '__ID__'

@dataclass
class Revision(Field):
    _type = '__REVISION__'

@dataclass
class CreatedBy(Field):
    _type = 'CREATED_BY'

@dataclass
class CreatedDatetime(Field):
    _type = 'CREATED_TIME'

@dataclass
class UpdatedBy(Field):
    _type = 'MODIFIER'

@dataclass
class UpdatedDatetime(Field):
    _type = 'UPDATED_TIME'


# Custom Fields

@dataclass
class Text(Field):
    _type = 'SINGLE_LINE_TEXT'

@dataclass 
class TextArea(Field):
    _type = 'MULTI_LINE_TEXT'

@dataclass
class RichText(Field):
    _type = 'RICH_TEXT'

@dataclass
class Number(Field):
    _type = 'NUMBER'

@dataclass
class Calculated(Field):
    _type = 'CALC'

@dataclass
class CheckBox(Field):
    _type = 'CHECK_BOX'

@dataclass
class RadioButton(Field):
    _type = 'RADIO_BUTTON'

@dataclass
class MultiChoice(Field):
    _type = 'MULTI_SELECT'

@dataclass
class Dropdown(Field):
    _type = 'DROP_DOWN'

@dataclass
class UserSelection(Field):
    _type = 'USER_SELECT'

@dataclass
class DepartmentSelection(Field):
    _type = 'ORGANIZATION_SELECT'

@dataclass
class GroupSelection(Field):
    _type = 'GROUP_SELECT'

@dataclass
class Date(Field):
    _type = 'DATE'

@dataclass
class Time(Field):
    _type = 'TIME'

@dataclass
class DateAndTime(Field):
    _type = 'DATETIME'

@dataclass
class Link(Field):
    _type = 'LINK'

@dataclass
class Attachment(Field):
    _type = 'FILE'

# NOTE: Lookup fields are determined by their field code and
#       can be either a Single Line Text or Number field
@dataclass
class Lookup(Field):
    _type = '_LOOKUP' #('SINGLE_LINE_TEXT', 'NUMBER')

@dataclass
class Table(Field):
    _type = 'SUBTABLE'

@dataclass
class RelatedRecords(Field):
    _type = 'REFERENCE_TABLE'

@dataclass
class Categories(Field):
    _type = 'CATEGORY'

@dataclass
class Status(Field):
    _type = 'STATUS'

@dataclass
class Assignee(Field):
    _type = 'STATUS_ASSIGNEE'


# Un-retrievable / Aesthetic Fields

@dataclass
class Label(Field): 
    _type = 'LABEL'

@dataclass
class BlankSpace(Field):
    _type = 'SPACER'

@dataclass
class Border(Field):
    _type = 'HR'

@dataclass
class FieldGroup(Field):
    _type = 'GROUP'

# Map the response type to the Field Subclass
FieldTypeMap: dict[str, type[Field]] = {
    field_type._type: field_type
    for field_type in Field.__subclasses__()
}

if __name__ == '__main__':
    for name, type_ in FieldTypeMap.items():
        print(f'{name}: {type_}')
