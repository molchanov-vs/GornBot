import io
import random
from google import genai
from google.genai.types import UploadFileConfig, GenerateContentConfig

from functools import lru_cache

from ..config import Config

from ..enums import DialogDataKeys


@lru_cache(maxsize=None)
def _get_client(api_key: str) -> genai.Client:
    return genai.Client(api_key=api_key)


async def generate_transcript(config: Config, voice_file: io.BytesIO):

    client = _get_client(config.gemini.api_key)

    voice_file.seek(0)

    uploaded = await client.aio.files.upload(
        file=voice_file,        
        config=UploadFileConfig(
            mime_type="audio/ogg",        # Telegram voice notes = OGG/Opus
            display_name="voice.ogg" # optional, for your sanity
        ),
    )

    prompt = 'Generate a transcript of the speech.'
    response = await client.aio.models.generate_content(
        model=config.gemini.model,
        contents=[prompt, uploaded]
    )
    return response.text



async def generate_feedback(config: Config, data: dict, default_config: bool = True):

    client = _get_client(config.gemini.api_key)

    if default_config:
        temperature = data[DialogDataKeys.TEMPERATURE]

    else:
        temperature = random.uniform(0.1, 1.0)

    gemini_config = GenerateContentConfig(
        system_instruction=data[DialogDataKeys.PROMPT],
        temperature=temperature
    )

    contents = [
        f"<sullabus>{data[DialogDataKeys.SYLLABUS]}</sullabus>",
        f"<discipline>{data[DialogDataKeys.DISCIPLINE_NAME]}</discipline>",
        f"<task>{data[DialogDataKeys.TASK_NAME]}</task>",
        f"<task_description>{data[DialogDataKeys.TASK_DESCRIPTION]}</task_description>",
        f"<teacher_input>{data[DialogDataKeys.TEXT_FROM_TEACHER]}</teacher_input>",
    ]

    response = await client.aio.models.generate_content(
        model=config.gemini.model,
        config=gemini_config,
        contents=contents
    )
    return response.text
