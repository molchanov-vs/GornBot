from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):

    MAIN = State()


class Feedback(StatesGroup):

    DISCIPLINE = State()
    TASK = State()
    INPUT = State()
    OUTPUT = State()