"""Submodule for defining Kintone Fields"""

from dataclasses import dataclass

class Field:
    def __init__(self, field_info: dict[str, dict[str, str]]):
        self.code, data = field_info.popitem()

        self.type = data.pop('type')
        self.value = data.pop('value')



@dataclass
class RecordNumber(Field): ...

@dataclass
class RecordId(Field): ...

@dataclass
class Revision(Field): ...

@dataclass
class CreatedBy(Field): ...

@dataclass
class CreatedDatetime(Field): ...

@dataclass
class UpdatedBy(Field): ...

@dataclass
class UpdatedDatetime(Field): ...


# Custom Fields

@dataclass
class Text(Field): ...

@dataclass 
class TextArea(Field): ...

@dataclass
class RichText(Field): ...

@dataclass
class Number(Field): ...

@dataclass
class Calculated(Field): ...

@dataclass
class CheckBox(Field): ...

@dataclass
class RadioButton(Field): ...

@dataclass
class MultiChoice(Field): ...

@dataclass
class Dropdown(Field): ...

@dataclass
class UserSelection(Field): ...

@dataclass
class DepartmentSelection(Field): ...

@dataclass
class GroupSelection(Field): ...

@dataclass
class Date(Field): ...

@dataclass
class Time(Field): ...

@dataclass
class DateAndTime(Field): ...

@dataclass
class Link(Field): ...

@dataclass
class Attachment(Field): ...

@dataclass
class Lookup(Field): ...

@dataclass
class Table(Field): ...

@dataclass
class RelatedRecords(Field): ...

@dataclass
class Categories(Field): ...

@dataclass
class Status(Field): ...

@dataclass
class Assignee(Field): ...


# Un-retrievable

@dataclass
class Label(Field): ...

@dataclass
class BlankSpace(Field): ...

@dataclass
class Border(Field): ...

@dataclass
class FieldGroup(Field): ...