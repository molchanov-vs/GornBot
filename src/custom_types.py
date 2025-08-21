from datetime import datetime
from pydantic import BaseModel, field_validator, ValidationInfo
from pydantic import PositiveInt, Field

from my_tools import get_datetime_now, DateTimeKeys


class UserNotify(BaseModel):

    id: PositiveInt
    date: str = Field(default_factory=get_datetime_now)
    status: bool


class UserOnboarding(BaseModel):

    date: str = Field(default_factory=get_datetime_now, validate_default=True)
    approve: bool = Field(default=False)
    name: str | None = Field(default=None)
    age: str | None = Field(default=None)
    education: str | None = Field(default=None)
    current_status: str | None = Field(default=None)
    university: str | None = Field(default=None)
    about: str | None = Field(default=None)
    question_1: str | None = Field(default=None)
    question_2: str | None = Field(default=None)
    question_3: str | None = Field(default=None)
    question_4: str | None = Field(default=None)

    @field_validator("date")
    @classmethod
    def set_date(cls, v: datetime):
        return get_datetime_now(DateTimeKeys.DEFAULT)


class UserOffboarding(BaseModel):

    date: str = Field(default_factory=get_datetime_now, validate_default=True)
    question_1: str | None = Field(default=None)
    question_2: str | None = Field(default=None)
    question_3: str | None = Field(default=None)
    question_4: str | None = Field(default=None)
    associate: str | None = Field(default=None)
    feedback: str | None = Field(default=None)

    @field_validator("date")
    @classmethod
    def set_date(cls, v: datetime):
        return get_datetime_now(DateTimeKeys.DEFAULT)


class UserAction(BaseModel):

    date: str = Field(default_factory=get_datetime_now)
    action_id: str


class MessageForGPT(BaseModel):

    date: str = Field(default_factory=get_datetime_now)
    state: str
    text: str


class UserData(BaseModel):

    id: PositiveInt
    first_name: str | None = Field(default=None, description="User's first name")
    last_name: str | None = Field(default=None, description="User's last name")
    full_name: str | None = Field(default=None, validate_default=True, description="Computed full name from first and last name")
    username: str | None = Field(default=None, description="Telegram username with https://t.me/ prefix")
    is_premium: bool | None = Field(default=None, description="Whether user has Telegram Premium")
    language_code: str = Field(default="", description="User's language code")
    date: str = Field(default_factory=get_datetime_now, description="Record creation date")


    @field_validator("full_name", mode="before")
    @classmethod
    def set_fullname(cls, v: str | None, info: ValidationInfo) -> str | None:

        _first_name = info.data.get("first_name")
        _last_name = info.data.get("last_name")

        if _first_name or _last_name:
            _full_name = " ".join(
                [
                    _first_name if _first_name else "", 
                    _last_name if _last_name else ""
                ]).strip()
        else:
            _full_name = v
        
        return _full_name 


    @field_validator("username")
    @classmethod
    def set_username(cls, v: str | None) -> str | None:

        if v is None:
            return v
        
        if isinstance(v, str) and not v.startswith("https://t.me/"):
            return f"https://t.me/{v}"
        else:
            return v


    @field_validator("language_code", mode="before")
    @classmethod
    def set_language_code(cls, v: str):

        if not v:
            return ""
        else:
            return v

    def compare_fields(self) -> tuple:
        
        return (self.full_name, self.username, self.is_premium, self.language_code)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserData):
            return NotImplemented
        return self.compare_fields() == other.compare_fields()
    
    def __hash__(self) -> int:
        """Make UserData hashable for use in sets and as dict keys."""
        return hash((self.id, self.compare_fields()))