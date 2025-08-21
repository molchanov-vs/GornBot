from typing import TYPE_CHECKING

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.storage.redis import RedisStorage

from ..utils.utils import get_middleware_data

from ..states import Feedback
from ..config import Config

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from ..locales.stub import TranslatorRunner


async def dialog_get_data(
        i18n: TranslatorRunner,
        users: RedisStorage,
        dialog_manager: DialogManager,
        **kwargs):
    
    _, _, user_data = get_middleware_data(dialog_manager)
    
    data = {
        "back_btn": i18n.service.back_btn(),
        "discipline": i18n.feedback.discipline(),
        "task": i18n.feedback.task(),
        "input": i18n.feedback.input(),
        "audio": i18n.feedback.audio(),
        "output": i18n.feedback.output()
    }

    return data


# Dialog with windows using Format for localization
dialog = Dialog(

    Window(
        Format("{discipline}"),
        Button(Const("{approve_btn}"), id="approve"),
        state=Feedback.DISCIPLINE
    ),

    getter=dialog_get_data
)