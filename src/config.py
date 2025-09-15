import yaml
from pydantic import \
    BaseModel, PositiveInt, ValidationError, HttpUrl, Field


class System(BaseModel):

    time_zone: str


class Bot(BaseModel):

    id: PositiveInt
    name: str
    link: HttpUrl
    token: str


class MessageEffect(BaseModel):

    fire: str
    thumb_up: str
    thumb_down: str
    heart: str
    greeting: str
    poo: str


class Owner(BaseModel):

    id: PositiveInt
    name: str
    link: HttpUrl


class Admins(BaseModel):
    ids: list[PositiveInt]


class Superadmins(BaseModel):
    ids: list[PositiveInt]


class Redis(BaseModel):

    host: str
    fsm: str
    users: str
    temp: str


class Google(BaseModel):

    feedbacks_and_accesses_id: str
    accesses_tab: str
    accesses_tab_length: PositiveInt
    content_id: str
    content_tab: str
    content_tab_length: PositiveInt
    disciplines_tab_length: PositiveInt
    syllabus_tab: str
    service_account_json: str


class LLM(BaseModel):

    api_key: str
    model: str
    provider: str
    embedding_model: str


class SystemPrompt(BaseModel):

    prompt: str


class Config(BaseModel):

    system: System
    bot: Bot
    bot_test: Bot
    message_effect: MessageEffect
    owner: Owner
    admins: Admins
    superadmins: Superadmins
    redis: Redis
    google: Google
    openai: LLM
    gemini: LLM
    system_prompt: SystemPrompt


# Load the YAML configuration file
def load_config() -> Config:
    import os

    with open('config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)

    # Get environment variable to determine which bot config to use
    environment = os.getenv('ENVIRONMENT', 'prod')
    
    # Select the appropriate bot configuration
    if environment == 'dev':
        # For development, swap bot and bot_test so bot points to bot_test config
        config_data['bot'] = config_data['bot_test']
        print(config_data['bot'])
        print(f"🔧 Development mode: Using test bot configuration: {config_data['bot']['name']}")
    else:
        # Use bot configuration for production (keep as is)
        print(f"🚀 Production mode: Using production bot configuration: {config_data['bot']['name']}")

    try:
        config: Config = Config(**config_data)
        return config
    except ValidationError as e:
        print("Config validation error:", e.json(indent=4))
        raise
    
    
def main():
    config: Config = load_config()
    print(config.model_dump_json(indent=4))


if __name__ == "__main__":
    main()