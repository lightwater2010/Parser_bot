from aiogram.fsm.state import StatesGroup, State

class ProjectWithProperties(StatesGroup):
    name = State() 
    price = State()
    category = State()
    date = State()
    amount = State()

