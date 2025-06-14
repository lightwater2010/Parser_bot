import re

async def validate_price(price:str) -> bool:
    pattern = r"от \d{2,5} до \d{2,5} (?:руб|дол|евр)"
    if re.fullmatch(pattern=pattern, string=price.lower().strip()):
        return True
    return False

async def validate_field(field, data):
    return True if field in data else False

async def generate_text_by_projects(data_list: list[dict]):
    for project in data_list:
        text = (
                        f"🔎 <b>Вакансия найдена</b>\n"
                        f"📌 <b>Заголовок:</b> {project['title'].strip()}\n"
                        f"📂 <b>Категория:</b> {project['category'].strip()}\n"
                        f"📝 <b>Описание:</b>\n{project['descr'].strip()}\n"
                        f"💰 <b>Оплата:</b> {project['price'].strip()}\n"
                        f"📅 <b>Дата публикации:</b> {project['date'].strip()}\n"
                        f"🔗 <b>Подробнее:</b> <i>{project['url'].strip()}</i>"
                    )
        yield text

        
