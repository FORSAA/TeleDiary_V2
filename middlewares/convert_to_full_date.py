from datetime import datetime

ANCHOR_DATE = datetime(2024, 9, 2) 

async def convert_to_full_date(date: str) -> str:
    MONTHS_RU = {
        "января": "01",
        "февраля": "02",
        "марта": "03",
        "апреля": "04",
        "мая": "05",
        "июня": "06",
        "июля": "07",
        "августа": "08",
        "сентября": "09",
        "октября": "10",
        "ноября": "11",
        "декабря": "12"
    }

    parts = date.strip().lower().split()
    if len(parts) != 2:
        raise ValueError("Неверный формат. Ожидается '<день> <месяц>'")

    day, month_str = parts
    if month_str not in MONTHS_RU:
        raise ValueError(f"Неизвестный месяц: {month_str}")

    day = int(day)
    month = int(MONTHS_RU[month_str])

    year = ANCHOR_DATE.year
    result_date = datetime(year, month, day)

    if result_date < ANCHOR_DATE:
        result_date = datetime(year + 1, month, day)

    return result_date.strftime("%d.%m.%Y")
