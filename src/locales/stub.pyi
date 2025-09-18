from decimal import Decimal
from typing import Literal

from fluent_compiler.types import FluentType
from typing_extensions import TypeAlias

PossibleValue: TypeAlias = str | int | float | Decimal | bool | FluentType

class TranslatorRunner:
    def get(self, path: str, **kwargs: PossibleValue) -> str: ...
    service: Service
    feedback: Feedback

class Service:
    @staticmethod
    def lang() -> Literal["""ru"""]: ...
    @staticmethod
    def back_btn() -> Literal["""◀️ Назад"""]: ...
    @staticmethod
    def next_btn() -> Literal["""Далее ▶️"""]: ...
    @staticmethod
    def done_btn() -> Literal["""✅ Готово"""]: ...
    @staticmethod
    def contact_btn() -> Literal["""💬 Связаться"""]: ...
    @staticmethod
    def to_msg_btn() -> Literal["""👀 К сообщению"""]: ...
    @staticmethod
    def admin_btn() -> Literal["""🛠️ Админка"""]: ...
    @staticmethod
    def support_btn() -> Literal["""👨🏻‍💻 Поддержка"""]: ...

class Feedback:
    @staticmethod
    def discipline(*, name: PossibleValue) -> Literal["""Здравствуйте, { $name }.

Выберите дисциплину:"""]: ...
    @staticmethod
    def task(*, discipline: PossibleValue) -> Literal["""Выбрана дисциплина &lt;b&gt;{ $discipline }&lt;/b&gt;.

Выберите задачу:"""]: ...
    @staticmethod
    def input(*, task_name: PossibleValue) -> Literal["""Выбрано задание &lt;b&gt;{ $task_name }&lt;/b&gt;

Введите ваше сообщение или отправьте голосовую запись"""]: ...
    @staticmethod
    def audio() -> Literal["""Вот транскрибация:"""]: ...
    @staticmethod
    def output() -> Literal["""Вот результат:"""]: ...
