from datetime import datetime

async def get_object_id_from_date(date_str: str) -> str:
        start_date = datetime.strptime("02.09.2024", "%d.%m.%Y")
        current_date = datetime.strptime(date_str, "%d.%m.%Y")

        delta_days = (current_date - start_date).days
        if delta_days < 0:
            raise ValueError("Дата раньше начала первой недели")

        week_number = delta_days // 7 + 1
        object_id = 91 + week_number
        return f'object:{object_id}'