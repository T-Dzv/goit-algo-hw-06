from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        # adding equality method to simplify further usage, since Field class is ment for simple types of data
        # and it will be conveniant to use "in", "==" and other comparisons similar to primitive types. 
        if isinstance(other, Field):
            return self.value == other.value
        return False

class Name(Field):
    # This class represents the name of a contact, ensures it has a value attribute. Parent class is Field
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name field cannot be empty.")
        super().__init__(value)

class Phone(Field):
    # Phone class with validation to ensure the phone number contains exactly 10 digits. Parent class is Field
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must consist of 10 digits.")
        super().__init__(value)

class Record:
    # This class holds a contact's information, including name and a list of phone numbers.
    def __init__(self, name):
        self.name = Name(name) # Name object, ensuring the name is validated.
        self.phones = [] # List to store multiple Phone objects.

    def add_phone(self, phone):
        self.phones.append(Phone(phone))  # Adds a new Phone object after validation.

    def remove_phone(self, phone):
        # Attempts to remove a phone number from the list; if not found, does nothing.
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Edits an existing phone number; if not found, raises an error.
        try:
            # This will create a temporary Phone object and use it for comparison
            index = self.phones.index(Phone(old_phone))
            self.phones[index] = Phone(new_phone)
        except ValueError:
            raise ValueError("Old phone number not found.")

    def find_phone(self, phone):
        # Finds and returns a phone object; if not found, returns None.
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, Phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    # Manages a collection of Record objects, providing methods to manipulate them.
    def add_record(self, record: Record):
        if record.name.value in self.data:
            raise ValueError("Record with this name already exists.")
        ''' !!!! питання до ментора !!!
        тут я не змогла остаточно визначитись, чи буде краще у велью запису зберігати цілком данні Рекорд,
        чи краще лише список номерів телефонів:
        self.data[record.name.value] = record.phones
        у коді реалізований перший підхід, оскільки він дає доступ до більшого обсягу даних, проте тоді 
        АдресБук буде "важити" більше. 
        Буду вдячна за пораду та розбір питання у комментах до ДЗ. 
        '''
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Record not found.")

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

# Test cases. Uncomment to check. 

# book = AddressBook()

#     # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

#     # Додавання запису John до адресної книги
# book.add_record(john_record)

#     # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

#     # Виведення всіх записів у книзі
     
# print(book)
# print("")

#     # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

#     # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

#     # Видалення запису Jane
# book.delete("Jane")
# print(book)
