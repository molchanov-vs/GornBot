import io
import random
from google import genai
from google.genai.types import UploadFileConfig, GenerateContentConfig

from ..config import Config

from ..enums import DialogDataKeys


async def generate_transcript(config: Config, voice_file: io.BytesIO):

    client = genai.Client(api_key=config.gemini.api_key)

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

    client = genai.Client(api_key=config.gemini.api_key)

    if default_config:
        temperature = data[DialogDataKeys.TEMPERATURE]

    else:
        temperature = random.uniform(0.1, 1.0)

    gemini_config = GenerateContentConfig(
        system_instruction=data[DialogDataKeys.PROMPT],
        temperature=temperature
    )

    contents = [
        data[DialogDataKeys.SYLLABUS],
        data[DialogDataKeys.DISCIPLINE_NAME],
        data[DialogDataKeys.TASK_NAME],
        data[DialogDataKeys.TASK_DESCRIPTION],
        data[DialogDataKeys.TEXT_FROM_TEACHER],
    ]

    response = await client.aio.models.generate_content(
        model=config.gemini.model,
        config=gemini_config,
        contents=contents
    )
    return response.text
