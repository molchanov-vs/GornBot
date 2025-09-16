from typing import Any, TYPE_CHECKING

from aiogram import F
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram.types import CallbackQuery
from aiogram.enums import ContentType
from aiogram.fsm.storage.redis import RedisStorage

from aiogram_dialog.widgets.kbd import Back, Select, Column, Button, Row
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput

from ..enums import DialogDataKeys
from ..google_queries import put_feedback
from ..utils.utils import get_middleware_data

from ..utils.feedback_handlers import handle_voice, process_feedback_text, handle_transcription

from ..states import Feedback

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from ..locales.stub import TranslatorRunner


async def on_dialog_start(
        start_data: Any,
        dialog_manager: DialogManager):

    dialog_manager.dialog_data[DialogDataKeys.FOR_GEMINI] = start_data[DialogDataKeys.FOR_GEMINI]


async def dialog_get_data(
        i18n: TranslatorRunner,
        users: RedisStorage,
        dialog_manager: DialogManager,
        **kwargs):
    
    _, _, user_data = get_middleware_data(dialog_manager)

    discipline_name = dialog_manager.dialog_data.get(
        DialogDataKeys.DISCIPLINE_NAME, DialogDataKeys.UNKNOWN)

    discipline_id = dialog_manager.dialog_data.get(
        DialogDataKeys.DISCIPLINE_ID, DialogDataKeys.UNKNOWN)

    task_name = dialog_manager.dialog_data.get(
        DialogDataKeys.TASK_NAME, DialogDataKeys.UNKNOWN)

    task_id = dialog_manager.dialog_data.get(
        DialogDataKeys.TASK_ID, DialogDataKeys.UNKNOWN)

    task_description = dialog_manager.start_data.get(discipline_id, {}).get(task_id, {}).get(
        DialogDataKeys.TASK_DESCRIPTION, DialogDataKeys.UNKNOWN)

    syllabus = dialog_manager.start_data.get(discipline_id, {}).get(
        DialogDataKeys.SYLLABUS, DialogDataKeys.UNKNOWN)

    
    dialog_manager.dialog_data[DialogDataKeys.FOR_GEMINI].update({
        DialogDataKeys.DISCIPLINE_NAME: discipline_name,
        DialogDataKeys.TASK_NAME: task_name,
        DialogDataKeys.TASK_DESCRIPTION: task_description,
        DialogDataKeys.SYLLABUS: syllabus
    })


    data = {
        "back_btn": i18n.service.back_btn(),
        "discipline_header": i18n.feedback.discipline(username=user_data.first_name),
        "task_header": i18n.feedback.task(discipline=discipline_name),
        "task_name": task_name,
        "input_header": i18n.feedback.input(
            task_name=task_name, 
            task_description=f"{task_description[:50]}...", 
            syllabus=f"{syllabus[:50]}..."),
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
    current_discipline = dialog_manager.dialog_data.get(
        DialogDataKeys.DISCIPLINE_ID, DialogDataKeys.UNKNOWN)

    tasks = [
        (v.get("name", "None"), k) for k, v in dialog_manager.start_data.get(current_discipline, {}).items() if "task" in k
        ]

    return {"tasks": tasks}


async def discipline_selection(
        callback: CallbackQuery, 
        widget: Select,
        dialog_manager: DialogManager, 
        item_id: str):
    
    # Get discipline name from start_data
    discipline_name = dialog_manager.start_data.get(item_id, {}).get("name", DialogDataKeys.UNKNOWN)
    
    dialog_manager.dialog_data[DialogDataKeys.DISCIPLINE_ID] = item_id
    dialog_manager.dialog_data[DialogDataKeys.DISCIPLINE_NAME] = discipline_name
    
    print(f'Выбрана дисциплина: {discipline_name} (id={item_id})')
    await dialog_manager.next()


async def task_selection(
        callback: CallbackQuery, 
        widget: Select,
        dialog_manager: DialogManager, 
        item_id: str):

    # Get task name from start_data
    discipline_id = dialog_manager.dialog_data.get(
        DialogDataKeys.DISCIPLINE_ID, DialogDataKeys.UNKNOWN)

    task_name = dialog_manager.start_data.get(discipline_id, {}).get(item_id, {}).get("name", DialogDataKeys.UNKNOWN)
    
    dialog_manager.dialog_data[DialogDataKeys.TASK_ID] = item_id
    dialog_manager.dialog_data[DialogDataKeys.TASK_NAME] = task_name
    
    await dialog_manager.next()


async def get_data_for_output(
        dialog_manager: DialogManager,
        **kwargs):

    return {"feedback_text": dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(DialogDataKeys.FEEDBACK_TEXT, DialogDataKeys.UNKNOWN)}


async def new_feedback(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    await dialog_manager.switch_to(Feedback.INPUT)


async def handle_feedback(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    if callback.data == "like_id":
        like = True
    else:
        like = False

    await put_feedback(dialog_manager, like)

    await dialog_manager.switch_to(Feedback.INPUT)


async def redo_feedback(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    pass


async def get_data_for_input(
        dialog_manager: DialogManager,
        **kwargs):

    data = {}
    transcription_from_audio = dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(DialogDataKeys.TRANSCRIPTION_FROM_AUDIO)
    if transcription_from_audio:
        data.update({"transcription_from_audio": transcription_from_audio})

    return data
    


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
        Format("{input_header}", when=~F["transcription_from_audio"]),
        Format("{transcription_from_audio}", when=F["transcription_from_audio"]),
        Row(
            Back(Format("{back_btn}")),
            Button(Const("⌯⌲ Отправить"), id="send_btn_id", on_click=handle_transcription, when=~F["transcription_from_audio"]),
        ),
        TextInput(
            id="input_text_feedback",
            on_success=process_feedback_text,
        ),
        MessageInput(
            func=handle_voice,
            content_types= ContentType.VOICE,
            id="voice_feedback_id"
        ),
        getter=get_data_for_input,
        state=Feedback.INPUT
    ),

    Window(
        Format("{feedback_text}"),
        Row(
            Button(Const("👎"), id="dislike_id", on_click=handle_feedback),
            Button(Const("👍"), id="like_id", on_click=handle_feedback),
        ),
        Button(Const("🔄 Перегенерировать"), id="redo_btn_id", on_click=redo_feedback),
        Button(Const("🚀 Начать новый фидбек"), id="new_feedback_btn_id", on_click=new_feedback),
        getter=get_data_for_output,
        state=Feedback.OUTPUT
    ),

    on_start=on_dialog_start,
    getter=dialog_get_data
)