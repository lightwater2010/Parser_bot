from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from keyboards import *
from aiogram.fsm.context import FSMContext
from project_with_properties import ProjectWithProperties
from validate_fields import validate_field, validate_price, generate_text_by_projects
from parse import parsing


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.reply(
        "👋 Привет! Я твой помощник для парсинга новых заказов.\n"
        "Готов найти нужную информацию для тебя. Просто нажми на кнопку \"Получить проекты\", чтобы начать!",
        reply_markup=greeting_kb
    )

@router.message(F.text.in_(["/search", "Получить проекты"]))
async def get_projects(message: Message, state: FSMContext):
    await message.answer("🚀 Отлично! Введите ключевые слова для поиска проекта:\n"
    "Например:  дизайнер логотипов, разработка сайта на Python, копирайтер для соцсетей", reply_markup=ReplyKeyboardRemove())
    
    await state.set_state(ProjectWithProperties.name)


@router.message(ProjectWithProperties.name)
async def get_name_project(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("💰 Теперь укажите желаемый бюджет проекта:\n"
    "Например: от 5000 до 15000 руб, или от 100 до 300 дол/евр", reply_markup=skip_kb_builder_price)
    
    await state.set_state(ProjectWithProperties.price)


@router.message(ProjectWithProperties.price)
async def get_price_project(message: Message, state: FSMContext, categories: list[str]):
    
    if await validate_price(message.text):
        await state.update_data(price=message.text)
        await message.answer("🎨 Супер! Теперь выберите категорию проекта из списка ниже:", reply_markup=await get_categories(categories))
        await message.answer("Или, если категория не важна, просто нажмите \"Пропустить\" 👇", reply_markup=skip_kb_builder_cat)
        await state.set_state(ProjectWithProperties.category)
    else:
        await message.reply("🤔 Упс! Кажется, формат цены введён неверно. Попробуйте ещё раз:\nНапример:\n—от 1000 до 2000 руб\n— от 50 до 100 дол\n— от 40 до 70 евр", 
                            reply_markup=skip_kb_builder_price)
        await state.set_state(ProjectWithProperties.price)



@router.message(ProjectWithProperties.category)
async def get_category_project(message: Message, state: FSMContext, categories: list[str]):

    if await validate_field(message.text.strip(), categories):
        await state.update_data(category=message.text)
        await message.answer("📅 Отлично! Теперь выберите, насколько свежие проекты вас интересуют:", reply_markup=dates_kb)
        await message.answer("Или нажмите \"Пропустить\", если дата публикации не имеет значения 👇", reply_markup=skip_kb_builder_date)
        await state.set_state(ProjectWithProperties.date)
    else:
        await message.reply("🧐 Такой категории в списке нет. Пожалуйста, выберите одну из предложенных:\n"
        "Или пропустите этот шаг.", reply_markup=skip_kb_builder_cat)
        await state.set_state(ProjectWithProperties.category)


@router.message(ProjectWithProperties.date)
async def get_date_project(message: Message, state: FSMContext, dates: list[str]):
    if await validate_field(message.text.strip(), dates):
        await state.update_data(date=message.text)
        await message.answer("Введите сколько проектов найти:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(ProjectWithProperties.amount)
    else:
        await message.reply("🤔 Хм, такой опции для даты нет. Пожалуйста, выберите из предложенных вариантов:", reply_markup=skip_kb_builder_date)
        await state.set_state(ProjectWithProperties.date)

@router.message(ProjectWithProperties.amount)
async def get_amount_projects(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(amount=int(message.text))
        request_data = await state.get_data()
        await message.reply(
                    f"✅ Все данные собраны! Идет поиск {request_data['amount']} проектов... ⏳\n\n"
                    f"📝 Ваш запрос:\n"
                    f"✨ Название: {request_data.get('name')}\n"
                    f"💰 Цена: {request_data.get('price', 'не указана')}\n"
                    f"🎨 Категория: {request_data.get('category', 'не указана')}\n"
                    f"📅 Дата: {request_data.get('date', 'не указана')}"
                ,reply_markup=ReplyKeyboardRemove())
        await state.clear()

        projects = await parsing(request_data)
        if projects != "Ничего" and projects != None:
            async for text in generate_text_by_projects(projects):
                await message.answer(text=text, parse_mode="HTML")
        else:
            await message.answer("К сожалению по вашему запросу не найдено заказов\nПопробуйте заново ввести запрос, использовав команду\n/search")

    else:
        await message.reply("Введите число!")
        await state.set_state(ProjectWithProperties.amount)


@router.callback_query(F.data.in_(["skip_price", "skip_category", "skip_date"]))
async def skip_handler(callback: CallbackQuery, state: FSMContext, categories: list[str]):
    await callback.answer()
    
    try:
        await callback.message.delete()
    except Exception:
        pass 
    

    if callback.data == "skip_price":
        await state.update_data(price=None)
        msg = await callback.message.answer(
            "💸 Цена пропущена. Двигаемся дальше!\n🎨 Теперь выберите категорию проекта:",
            reply_markup=await get_categories(categories)
        )
        await msg.answer(
            "Или нажмите \"Пропустить\", если категория не важна 👇",
            reply_markup=skip_kb_builder_cat
        )
        await state.set_state(ProjectWithProperties.category)

    elif callback.data == "skip_category":
        await state.update_data(category=None)
        msg = await callback.message.answer(
            "🎨 Категория пропущена. Хорошо!\n📅 Теперь выберите, насколько свежие проекты вас интересуют:",
            reply_markup=dates_kb
        )
        await msg.answer(
            "Или нажмите \"Пропустить\", если дата публикации не имеет значения 👇",
            reply_markup=skip_kb_builder_date
        )
        await state.set_state(ProjectWithProperties.date)

    elif callback.data == "skip_date":
        await state.update_data(date=None)
        msg = await callback.message.answer(
            "📅Дата пропущена. Хорошо!\n Теперь введите сколько проектов найти:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(ProjectWithProperties.amount)


