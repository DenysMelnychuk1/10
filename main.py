from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self,  value):
            self.__value = value
    def __str__(self):
        return str(self.value)
class Name(Field):
    pass
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
    @Field.value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 10:
            self._Field__value = value
            
        else:
            raise ValueError ('Invalid number')

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if not any(p.value == old_phone for p in self.phones):
            raise ValueError(f"Phone {old_phone} not found in the record")
        
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.now()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)

        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        days_remaining = (next_birthday - today).days
        return days_remaining

    def __str__(self):
        phone_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}{birthday_str}, phones: {phone_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, batch_size=5):
        records = list(self.data.values())
        for i in range(0, len(records), batch_size):
            yield records[i:i+batch_size]
