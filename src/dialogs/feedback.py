from typing import TYPE_CHECKING

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, Select, Column
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram.fsm.storage.redis import RedisStorage

from ..utils.utils import get_middleware_data
from ..utils.sheets_async import SheetsAsync
from ..custom_types import Teacher

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
    
    _, config, user_data = get_middleware_data(dialog_manager)

    # sheet = SheetsAsync(
    #     spreadsheet_id=config.google.feedbacks_and_accesses_id,
    #     sa_json_path=config.google.service_account_json
    # )
    
    # read_res = await sheet.read(f"{config.google.accesses_tab}!A1:C6")
    # read_discs = await sheet.read(f"{config.google.accesses_tab}!E1:F4")    

    data = {
        "back_btn": i18n.service.back_btn(),
        "discipline": i18n.feedback.discipline(username=user_data.username),
        "task": i18n.feedback.task(),
        "input": i18n.feedback.input(),
        "audio": i18n.feedback.audio(),
        "output": i18n.feedback.output()
    }

    return data


async def get_disciplines(**kwargs):

    _, config, user_data = get_middleware_data(kwargs["dialog_manager"])
    
    sheet = SheetsAsync(
        spreadsheet_id=config.google.feedbacks_and_accesses_id,
        sa_json_path=config.google.service_account_json
    )

    read_res = await sheet.read(f"{config.google.accesses_tab}!A1:C6")
    read_discs = await sheet.read(f"{config.google.accesses_tab}!E1:F4")

    teachers: list[Teacher] = [
        Teacher(id=i[1], name=i[0], disciplines=i[2].split(", ")) 
        for i in read_res.get("values")[1:]]

    print("Teachers:", teachers)
    print("--------------------------------")
    
    discs = dict([(el[0], el[1]) for el in read_discs.get("values")[1:]])

    print("Discs:", discs)
    print("--------------------------------")

    teacher = next((t for t in teachers if t.id == user_data.id), None)
    disciplines = [(d, discs.get(d)) for d in (teacher.disciplines if teacher else [])]

    print("Disciplines:", disciplines)
    print("--------------------------------")

    return {"disciplines": disciplines}


async def discipline_selection(
        callback: CallbackQuery, 
        widget: Select,
        dialog_manager: DialogManager, 
        item_id: str):
    
    print(f'Выбрана категория с id={item_id}')


# Dialog with windows using Format for localization
dialog = Dialog(

    Window(
        Format("{discipline}"),
        Column(
            Select(
                Format('{item[0]}'),
                id='discip',
                item_id_getter=lambda x: x[1],
                items='disciplines',
                on_click=discipline_selection
            ),
        ),
        state=Feedback.DISCIPLINE,
        getter=get_disciplines
    ),

    getter=dialog_get_data
)