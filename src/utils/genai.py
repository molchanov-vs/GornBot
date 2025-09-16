import io
from google import genai
from google.genai.types import UploadFileConfig, GenerateContentConfig

from ..config import Config

from ..enums import DialogDataKeys

from pprint import pprint


async def generate_transcript(config: Config, voice_file: io.BytesIO):

    client = genai.Client(api_key=config.gemini.api_key)

    voice_file.seek(0)

    # ✅ provide mime_type and a name
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



async def generate_feedback(config: Config, data: dict):

    pprint(data)

    client = genai.Client(api_key=config.gemini.api_key)

    response = await client.aio.models.generate_content(
        model=config.gemini.model,
        config = GenerateContentConfig(
            system_instruction=data[DialogDataKeys.PROMPT]
        ),
        contents=[
            data[DialogDataKeys.FEEDBACK_TEXT],
            data[DialogDataKeys.DISCIPLINE_NAME],
            data[DialogDataKeys.TASK_NAME],
            data[DialogDataKeys.TASK_DESCRIPTION],
            data[DialogDataKeys.SYLLABUS]
        ]
    )
    return response.text
