from typing import TYPE_CHECKING

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram.types import CallbackQuery, Message
from aiogram_dialog.widgets.kbd import Back, Select, Column
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram.fsm.storage.redis import RedisStorage

from ..google_queries import put_feedback

from ..utils.utils import get_middleware_data
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
    current_discipline_name = dialog_manager.dialog_data.get("current_discipline_name", "Unknown")
    current_discipline_id = dialog_manager.dialog_data.get("current_discipline_id", "Unknown")

    current_task_name = dialog_manager.dialog_data.get("current_task_name", "Unknown")
    current_task_id = dialog_manager.dialog_data.get("current_task_id", "Unknown")

    current_task_description = dialog_manager.start_data.get(current_discipline_id, {}).get(current_task_id, {}).get("description", "Unknown")
    syllabus = dialog_manager.start_data.get(current_discipline_id, {}).get("syllabus", "Unknown")


    data = {
        "back_btn": i18n.service.back_btn(),
        "discipline_header": i18n.feedback.discipline(username=user_data.first_name),
        "task_header": i18n.feedback.task(discipline=current_discipline_name),
        "task_name": current_task_name,
        "input_header": i18n.feedback.input(
            task_name=current_task_name, 
            task_description=current_task_description, 
            syllabus=syllabus),
        "audio": i18n.feedback.audio(),
        "output": i18n.feedback.output()
    }

    return data


async def get_disciplines(
        dialog_manager: DialogManager,
        **kwargs):

    # _, config, user_data = get_middleware_data(dialog_manager)
    disciplines = [(v.get("name", "None"), k) for k, v in dialog_manager.start_data.items()]

    return {"disciplines": disciplines}


async def get_tasks(
        dialog_manager: DialogManager,
        **kwargs):

    # _, config, user_data = get_middleware_data(dialog_manager)
    current_discipline = dialog_manager.dialog_data.get("current_discipline_id", "None")

    tasks = [
        (v.get("name", "None"), k) for k, v in dialog_manager.start_data.get(current_discipline, {}).items() if "task" in k
        ]
    
    print("Tasks:\n", tasks)

    return {"tasks": tasks}


async def discipline_selection(
        callback: CallbackQuery, 
        widget: Select,
        dialog_manager: DialogManager, 
        item_id: str):
    
    # Get discipline name from start_data
    discipline_name = dialog_manager.start_data.get(item_id, {}).get("name", "Unknown")
    
    dialog_manager.dialog_data["current_discipline_id"] = item_id
    dialog_manager.dialog_data["current_discipline_name"] = discipline_name
    
    print(f'Выбрана дисциплина: {discipline_name} (id={item_id})')
    await dialog_manager.next()


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def process_feedback_text(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:

    _, config, user_data = get_middleware_data(dialog_manager)
    current_discipline_name = dialog_manager.dialog_data.get("current_discipline_name", "Unknown")
    current_task_name = dialog_manager.dialog_data.get("current_task_name", "Unknown")

    await put_feedback(config, user_data.id, current_discipline_name, current_task_name, text)
    
    await message.answer(text=f'Ваш фидбек добавлен')


async def task_selection(
        callback: CallbackQuery, 
        widget: Select,
        dialog_manager: DialogManager, 
        item_id: str):
    
    # Get task name from start_data
    current_discipline = dialog_manager.dialog_data.get("current_discipline_id", "None")
    task_name = dialog_manager.start_data.get(current_discipline, {}).get(item_id, {}).get("name", "Unknown")
    
    dialog_manager.dialog_data["current_task_id"] = item_id
    dialog_manager.dialog_data["current_task_name"] = task_name
    
    print(f'Выбрано задание: {task_name} (id={item_id})')
    await dialog_manager.next()


# Dialog with windows using Format for localization
dialog = Dialog(

    Window(
        Format("{discipline_header}"),
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

    Window(
        Format("{task_header}"),
        Column(
            Select(
                Format('{item[0]}'),
                id='tsk',
                item_id_getter=lambda x: x[1],
                items='tasks',
                on_click=task_selection
            ),
        ),
        Back(Format("{back_btn}")),
        state=Feedback.TASK,
        getter=get_tasks
    ),

    Window(
        Format("{input_header}"),
        Back(Format("{back_btn}")),
        TextInput(
            id="input_text_feedback",
            on_success=process_feedback_text,
        ),
        state=Feedback.INPUT
    ),

    getter=dialog_get_data
)