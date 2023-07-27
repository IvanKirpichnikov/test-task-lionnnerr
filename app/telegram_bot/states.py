from aiogram.fsm.state import State, StatesGroup


class Order(StatesGroup):
    text = State()

class MyProfile(StatesGroup):
    email = State()
    phone_number = State()
