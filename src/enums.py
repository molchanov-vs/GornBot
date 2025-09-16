from enum import Enum


class Action(str, Enum):
    
    START = "start"
    RESTART = "restart"
    BACK = "back"
    NEXT = "next"
    CANCEL = "cancel"
    CONFIRM = "confirm"
    DELETE = "delete"
    EDIT = "edit"
    SEND = "send"
    SELECT = "select"
    SELECTED = "selected"
    UNSELECTED = "unselected"
    ADD = "add"
    REMOVE = "remove"
    ONBOARDING = "onboarding"
    OFFBOARDING = "offboarding"
    CHAT = "chat"


class Database(str, Enum):

    FSM = "fsm"
    USERS = "users"
    TEMP = "temp"


class RedisKeys(str, Enum):

    KNOWN_USERS = "known_users"
    PARSER_JOBS = "parser_jobs"
    PARSER_JOBS_RUNNING = "parser_jobs_running"


class DialogDataKeys(str, Enum):

    FOR_GEMINI = "for_gemini"
    DISCIPLINE_NAME = "discipline_name"
    DISCIPLINE_ID = "discipline_id"
    TASK_NAME = "task_name"
    TASK_ID = "task_id"
    TASK_DESCRIPTION = "task_description"
    SYLLABUS = "syllabus"
    UNKNOWN = "unknown"
    TEMPERATURE = "temperature"
    PROMPT = "prompt"
    TEXT_FROM_TEACHER = "text_from_teacher"
    FEEDBACK_TEXT = "feedback_text"
