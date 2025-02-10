from dataclasses import dataclass
from contextlib import contextmanager

# Main datamodels for KinPy
# Interfaces inherit the attributes defined here and implement methods for the API

# Sentinal to allow passing None/null values to the API to delete data using PATCH

Unset = object()

# NOTE: As far as I know, Kintone only uses PUT requests though, so it's important to always
# Send the full object data back when updating a record



class KTModel:
    def __getitem__(self, key):
        """Override getitem so only set values are returned"""
        val = getattr(self, key)
        if val is not Unset:
            return val
    
    def __iter__(self):
        """Override iter so only set values are returned"""
        return iter(
            (key, val)
            for key, val in self.__dict__.items()
            if val is not Unset
        )
    
    def __len__(self):
        """Override len so only set values are returned"""
        return len(self.__iter__())
    
    def __contains__(self, key):
        """Override contains so only set values are returned"""
        return key in self.__dict__ and self.__dict__[key] is not Unset

    def update(self) -> None: ...

    def refresh(self) -> None: ...

    @contextmanager
    def editor(self):
        """Context manager to allow updating a record.
        Refreshes the record before entering the context and updates it after exiting
        """
        self.refresh()
        yield self
        self.update()

# NOTE: When implementing a datamodel, use the Optional type hint to specify
# that the field is not required. Make sure you set the default value to `Unset`
# so that None/Null can be passes as a value to delete a value.

# Remember: Kintone only uses PUT requests, so always send the full object data back
# To do this, you take a record that was returned and update it with a partial record

# e.g. 
# new_record_info = KTRecord(id=1, name="John Doe", age=30)
# old_record = kintone.get_record(1)
# with old_record.editor():
#   old_record.update(new_record_info)

@dataclass(eq=False)
class KTApp(KTModel):
    pass

@dataclass(eq=False)
class KTRecord(KTModel):
    pass

@dataclass(eq=False)
class KTField(KTModel):
    pass

@dataclass(eq=False)
class KTUser(KTModel):
    pass

@dataclass(eq=False)
class KTGroup(KTModel):
    pass

@dataclass(eq=False)
class KTView(KTModel):
    pass

@dataclass(eq=False)
class KTSpace(KTModel):
    pass

@dataclass(eq=False)
class KTForm(KTModel):
    pass

@dataclass(eq=False)
class KTLayout(KTModel):
    pass

@dataclass(eq=False)
class KTRow(KTModel):
    pass