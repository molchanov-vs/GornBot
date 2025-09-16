import asyncio
import io
import logging

from aiogram.types import Message
from aiogram.fsm.storage.redis import RedisStorage

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.input import MessageInput, ManagedTextInput

from .utils import get_middleware_data, send_typing_action
from .genai import generate_transcript
from .genai import generate_feedback

from ..enums import DialogDataKeys

MAX_BYTES = 10 * 1024 * 1024


async def handle_voice(message: Message, widget: MessageInput, dialog_manager: DialogManager):

    bot, config, user_data = get_middleware_data(dialog_manager)
    # await add_action(dialog_manager)

    # date: str = get_datetime_now(DateTimeKeys.DEFAULT)
    # widget_id = widget.widget_id

    if message.voice:
        if message.voice.file_size <= MAX_BYTES:

            typing_task = asyncio.create_task(send_typing_action(user_data.id, bot))

            try:
                voice_file = io.BytesIO()
                await bot.download(message.voice.file_id, destination=voice_file)
                text = await generate_transcript(config, voice_file)
                print(text)
                await bot.send_message(user_data.id, text)
            except Exception as e:
                logging.error(f"Error generating transcript for {user_data.id} ({user_data.full_name}): {e}")
                # await bot.send_message(user_data.id, f"❌ Ошибка при генерации транскрипта: {e}")
            finally:
                typing_task.cancel()

        else:
            await message.answer("⚠️ Голосовое слишком большое (>10 МБ). Отправьте более короткую запись.")
            await asyncio.sleep(1)
            return
    else:
        await message.answer(text='❗Это должно быть голосовое сообщение')
        await asyncio.sleep(1)


# Хэндлер, который сработает, если пользователь ввел корректный возраст
async def process_feedback_text(
        message: Message, 
        widget: ManagedTextInput, 
        dialog_manager: DialogManager, 
        text: str) -> None:

    bot, config, user_data = get_middleware_data(dialog_manager)

    dialog_manager.dialog_data[DialogDataKeys.FOR_GEMINI][DialogDataKeys.TEXT_FROM_TEACHER] = text

    typing_task = asyncio.create_task(send_typing_action(user_data.id, bot))

    try:
        feedback: str = await generate_feedback(config, dialog_manager.dialog_data[DialogDataKeys.FOR_GEMINI])

        dialog_manager.dialog_data[DialogDataKeys.FOR_GEMINI][DialogDataKeys.FEEDBACK_TEXT] = feedback

        await dialog_manager.next()
    except Exception as e:
        logging.error(f"Error generating feedback for {user_data.id} ({user_data.full_name}): {e}")
        # await bot.send_message(user_data.id, f"❌ Ошибка при генерации фидбека: {e}")
    finally:
        typing_task.cancel()