import os.path
import pickle
from datetime import datetime

from task3 import AddressBook, Record, Name


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return "Value error"
        except Exception as e:
            return f"Undefined exception"

    return inner


def check_input_correctness(
        number_of_params_that_should_be_pass_to_function,
        error_message
):
    def decorator(func):
        def changed_function(*args, **kwargs):
            if len(args[0]) != number_of_params_that_should_be_pass_to_function:
                return error_message
            return func(*args, **kwargs)

        return changed_function

    return decorator


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
@check_input_correctness(
    2,
    "Please input the command in the format: add [name] [phone]"
)
def add_or_change_contact(args, contacts: AddressBook):
    name, phone = args
    try:
        record = contacts.find(name)
    except KeyError:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        response = "Record created"
    else:
        record.add_phone(phone)
        response = "add new phone to Record"

    return response


@input_error
@check_input_correctness(
    1,
    "Please input the command in the format: phone [name]"
)
def print_phone_by_name(args, contacts: AddressBook):
    if not args:
        return "Please provide a name to search for."

    name = args[0]

    try:
        record = contacts.find(name)
    except KeyError:
        return f"No contact found for {name}."
    else:
        return f"{record}"


@input_error
@check_input_correctness(
    0,
    "Please input the command in the format: all"
)
def print_all_contacts(args, contacts: AddressBook):
    if not contacts:
        return "No contacts available."

    return "\n".join(f"{records}" for records in contacts.values())


@input_error
@check_input_correctness(
    2,
    "Please input the command in the format: add-birthday [name] [birth_day]"
)
def add_birthday(args, contacts: AddressBook):
    name, birthday = args
    try:
        record = contacts.find(name)
    except KeyError:
        return "Such person was not found"

    try:
        if record.birthday is None:
            record.add_birthday(birthday)
        else:
            return "Failure. Birthday was already added to Record."
    except ValueError as e:
        return f"Birthday should be in format DD.MM.YYYY (for example 30.12.1990)"

    return "birthday successfully added"


@input_error
@check_input_correctness(
    1,
    "Please input the command in the format: show-birthday [name]"
)
def show_birthday(args, contacts: AddressBook):
    name = args[0]
    try:
        record = contacts.find(name)
    except KeyError:
        return "Such person was not found"

    if record.birthday is None:
        return "User dont add birthday"
    else:
        return f"{record.name}:{record.birthday}"


@input_error
@check_input_correctness(
    0,
    "Please input the command in the format: birthdays"
)
def birthdays(args, contacts: AddressBook):
    # defaultdict[date, list[Record]]

    birthdays_dict = contacts.get_birthdays_per_week()

    response = ""
    for day in sorted(birthdays_dict.keys()):
        response += f"{day.strftime('%A')}\n"
        for record in birthdays_dict[day]:
            response += f"\t{record}\n"

    return response


def load_dummy_contacts(contacts: AddressBook):
    data = [
        {"name": "Олексій", "birthday": datetime(1955, 12, 20)},
        {"name": "Марія", "birthday": datetime(1955, 12, 19)},
        {"name": "Анастасія", "birthday": datetime(1955, 12, 24)},
        {"name": "Іван", "birthday": datetime(1955, 12, 19)},
        {"name": "Оксана", "birthday": datetime(1955, 12, 20)},
    ]
    for user in data:
        r = Record(user['name'])
        r.add_phone("1234567890")
        r.add_birthday(user['birthday'].strftime("%d.%m.%Y"))
        contacts.add_record(r)


DATABASE_DIR = "databases"
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR, exist_ok=True)
DATABASE_FILE = DATABASE_DIR + "/saved_object.pkl"


def main():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'rb') as file:
            contacts = pickle.load(file)
    else:
        contacts = AddressBook()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add" or command == "change":
            print(add_or_change_contact(args, contacts))
        elif command == "phone":
            print(print_phone_by_name(args, contacts))
        elif command == "all":
            print(print_all_contacts(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")

    with open(DATABASE_FILE, 'wb') as file:
        pickle.dump(contacts, file)


if __name__ == "__main__":
    main()
