from collections import defaultdict
from datetime import datetime, date, timedelta


def get_birthdays_per_week(users: list[dict]):
    today = datetime.today().date()
    next_monday = today + timedelta(days=-today.weekday(), weeks=1)
    next_sunday = next_monday + timedelta(days=6)

    users_that_have_birth_day = defaultdict(list)

    for user in users:
        user_birthday = user["birthday"].date().replace(year=today.year)
        if user_birthday < today:
            user_birthday = user_birthday.replace(year=today.year + 1)

        if next_monday <= user_birthday <= next_sunday:
            users_that_have_birth_day[user_birthday].append(user['name'])

    for weekday in [next_sunday, next_monday]:
        users_that_have_birth_day[next_monday].extend(users_that_have_birth_day[weekday])
        users_that_have_birth_day.pop(weekday, None)

    if not users_that_have_birth_day[next_monday]:
        users_that_have_birth_day.pop(next_monday, None)

    for day in sorted(users_that_have_birth_day.keys()):
        f_str = f'{day.strftime("%A").center(15)} {" ~ ".join(users_that_have_birth_day[day])}'
        print(f_str)


if __name__ == "__main__":
    users = [
        {"name": "Олексій", "birthday": datetime(1955, 12, 5)},
        {"name": "Марія", "birthday": datetime(1955, 12, 4)},
        {"name": "Анастасія", "birthday": datetime(1955, 12, 9)},
        {"name": "Іван", "birthday": datetime(1955, 12, 10)},
        {"name": "Оксана", "birthday": datetime(1955, 12, 8)},
    ]
    get_birthdays_per_week(users)
