import os
import re
import asyncio

from aiogram import Bot
from aiogram.types import User
from aiogram.fsm.state import State
from aiogram_dialog import DialogManager

from my_tools import DialogManagerKeys

from ..custom_types import UserData
from ..config import Config




async def send_typing_action(chat_id: int, bot: Bot, delay: float = 1.0):
    try:
        while True:
            await bot.send_chat_action(chat_id, "typing")
            await asyncio.sleep(delay)
    except asyncio.CancelledError:
        pass



def get_middleware_data(dialog_manager: DialogManager) -> tuple[Bot, Config, UserData]:

    bot: Bot = dialog_manager.middleware_data[DialogManagerKeys.BOT]
    config: Config = dialog_manager.middleware_data.get(DialogManagerKeys.CONFIG)
    event_from_user: User = dialog_manager.middleware_data.get(DialogManagerKeys.EVENT_FROM_USER)
    user_data: UserData = UserData(**event_from_user.model_dump())

    return bot, config, user_data


def get_current_state(dialog_manager: DialogManager) -> State:

    return dialog_manager.current_context().state


def remove_logs():
    
    logs = sorted(os.listdir('logs'))

    if len(logs) > 5:
        for log in logs[:-1]:
            os.remove(f"logs/{log}")