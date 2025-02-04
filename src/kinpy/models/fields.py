"""Models for Kintone fields."""

from dataclasses import dataclass
from .base import _Model

@dataclass(eq=False)
class Field(_Model):
    """Base class for Kintone fields."""
    pass

@dataclass(eq=False)
class Group(Field):
    """Class for Kintone Group fields."""
    _TYPE = "GROUP"
    pass

@dataclass(eq=False)
class GroupSelect(Field):
    """Class for Kintone Group Selection fields."""
    _TYPE = "GROUP_SELECT"
    pass

@dataclass(eq=False)
class Calc(Field):
    """Class for Kintone Calculation fields."""
    _TYPE = "CALC"
    pass

@dataclass(eq=False)
class Category(Field):
    """Class for Kintone Category fields."""
    _TYPE = "CATEGORY"
    pass

@dataclass(eq=False)
class CheckBox(Field):
    """Class for Kintone Check Box fields."""
    _TYPE = "CHECK_BOX"
    pass

@dataclass(eq=False)
class CreatedTime(Field):
    """Class for Kintone Created Time fields."""
    _TYPE = "CREATED_TIME"
    pass

@dataclass(eq=False)
class Creator(Field):
    """Class for Kintone Creator fields."""

    _TYPE = "CREATOR"
    pass

@dataclass(eq=False)
class Date(Field):
    """Class for Kintone Date fields."""
    _TYPE = "DATE"
    pass

@dataclass(eq=False)
class DateTime(Field):
    """Class for Kintone Date and Time fields."""
    _TYPE = "DATETIME"
    pass

@dataclass(eq=False)
class DropDown(Field):
    """Class for Kintone Drop Down fields."""
    _TYPE = "DROP_DOWN"
    pass

@dataclass(eq=False)
class File(Field):
    """Class for Kintone File fields."""
    _TYPE = "FILE"
    pass

@dataclass(eq=False)
class Link(Field):
    """Class for Kintone Link fields."""
    _TYPE = "LINK"
    pass

@dataclass(eq=False)
class Modifier(Field):
    """Class for Kintone Modifier fields."""
    _TYPE = "MODIFIER"
    pass

@dataclass(eq=False)
class MultiLineText(Field): 
    """Class for Kintone Multi-line Text fields."""
    _TYPE = "MULTI_LINE_TEXT"
    pass

@dataclass(eq=False)
class MultiSelect(Field):
    """Class for Kintone Multi-select fields."""
    _TYPE = "MULTI_SELECT"
    pass

@dataclass(eq=False)
class Number(Field):
    """Class for Kintone Number fields."""
    _TYPE = "NUMBER"
    pass

@dataclass(eq=False)
class OrganizationSelect(Field):
    """Class for Kintone Organization Selection fields."""
    _TYPE = "ORGANIZATION_SELECT"
    pass

@dataclass(eq=False)
class RadioButton(Field):
    """Class for Kintone Radio Button fields."""
    _TYPE = "RADIO_BUTTON"
    pass

@dataclass(eq=False)
class RecordNumber(Field):
    """Class for Kintone Record Number fields."""
    _TYPE = "RECORD_NUMBER"
    pass

@dataclass(eq=False)
class ReferenceTable(Field):
    """Class for Kintone Reference fields."""
    _TYPE = "REFERENCE_TABLE"
    pass

@dataclass(eq=False)
class RichText(Field):
    """Class for Kintone Rich Text fields."""
    _TYPE = "RICH_TEXT"
    pass

@dataclass(eq=False)
class SingleLineText(Field):
    """Class for Kintone Single-line Text fields."""
    _TYPE = "SINGLE_LINE_TEXT"
    pass

@dataclass(eq=False)
class Status(Field):
    """Class for Kintone Status fields."""
    _TYPE = "STATUS"
    pass

@dataclass(eq=False)
class StatusAssignee(Field):
    """Class for Kintone Status Assignee fields."""
    _TYPE = "STATUS_ASSIGNEE"
    pass

@dataclass(eq=False)
class Subtable(Field):
    """Class for Kintone Subtable fields."""
    _TYPE = "SUBTABLE"
    pass

@dataclass(eq=False)
class Time(Field):
    """Class for Kintone Time fields."""
    _TYPE = "TIME"
    pass

@dataclass(eq=False)
class UpdatedTime(Field):
    """Class for Kintone Updated Time fields."""
    _TYPE = "UPDATED_TIME"
    pass

@dataclass(eq=False)
class UserSelect(Field):
    """Class for Kintone User Selection fields."""
    _TYPE = "USER_SELECT"
    pass