from aiogram_dialog import DialogManager

from .utils.sheets_async import SheetsAsync

from .config import Config
from .utils.utils import get_middleware_data
from .custom_types import Teacher

from .enums import DialogDataKeys


# Multiple singletons for different spreadsheets
_teachers_sheets_instance: SheetsAsync | None = None
_content_sheets_instance: SheetsAsync | None = None
_prompts_sheets_instance: SheetsAsync | None = None


def get_teachers_sheets_instance(config: Config) -> SheetsAsync:
    """
    Get or create a singleton SheetsAsync instance for teachers spreadsheet.
    """
    global _teachers_sheets_instance
    if _teachers_sheets_instance is None:
        _teachers_sheets_instance = SheetsAsync(
            spreadsheet_id = config.google.feedbacks_and_accesses_id,
            sa_json_path = config.google.service_account_json
        )
    return _teachers_sheets_instance



def get_content_sheets_instance(config: Config) -> SheetsAsync:
    """
    Get or create a singleton SheetsAsync instance for content spreadsheet.
    """
    global _content_sheets_instance
    if _content_sheets_instance is None:
        _content_sheets_instance = SheetsAsync(
            spreadsheet_id = config.google.content_id,  # Different spreadsheet
            sa_json_path = config.google.service_account_json
        )
    return _content_sheets_instance


def get_prompts_sheets_instance(config: Config) -> SheetsAsync:
    """
    Get or create a singleton SheetsAsync instance for prompts spreadsheet.
    """
    global _prompts_sheets_instance
    if _prompts_sheets_instance is None:
        _prompts_sheets_instance = SheetsAsync(
            spreadsheet_id = config.google.prompt_id,
            sa_json_path = config.google.service_account_json
        )
    return _prompts_sheets_instance


# Teachers spreadsheet operations
async def get_teachers(config: Config) -> list[Teacher]:
    """
    Get list of teachers from Google Sheets.
    """
    sheet: SheetsAsync = get_teachers_sheets_instance(config)

    read_res = await sheet.read(f"{config.google.accesses_tab}!A1:C")

    teachers: list[Teacher] = [
        Teacher(id=row[1], name=row[0], disciplines=row[2].split(", ")) 
        for row in read_res.get("values")[1:] if len(row) > 2]

    return teachers


async def get_teachers_ids(config: Config) -> set[int]:
    """
    Get list of teachers from Google Sheets.
    """

    teachers = await get_teachers(config)

    return set([teacher.id for teacher in teachers])


async def get_list_of_disciplines(
        config: Config, 
        teachers: list[Teacher],
        teacher_id: int) -> list[tuple[str, str]]:
    """
    Get list of disciplines for a current teacher.
    """

    sheet: SheetsAsync = get_teachers_sheets_instance(config)

    read_discs = await sheet.read(f"{config.google.accesses_tab}!E1:F")

    discs = dict([(el[0], el[1]) for el in read_discs.get("values")[1:]])

    teacher = next((t for t in teachers if t.id == teacher_id), None)

    return [(d, discs.get(d)) for d in teacher.disciplines] # [("Матметоды", "mathmethods"), ...]


async def get_list_of_tasks(
        config: Config,
        disciplines: list[tuple[str, str]]) -> list[tuple[str, str]]:

    sheet: SheetsAsync = get_content_sheets_instance(config)

    task_data: dict[str, list[list[str]]] = {}

    spreadsheet_meta = await sheet.get_spreadsheet()
    existing_tabs = {
        sheet_info["properties"]["title"]
        for sheet_info in spreadsheet_meta.get("sheets", [])
    }

    ranges_to_fetch: list[str] = []
    for _, discipline_id in disciplines:
        if discipline_id not in existing_tabs:
            task_data[discipline_id] = []
            continue

        ranges_to_fetch.append(f"{discipline_id}!A2:C")
        task_data.setdefault(discipline_id, [])

    if ranges_to_fetch:
        batch_result = await sheet.batch_get(ranges_to_fetch)
        for value_range in batch_result.get("valueRanges", []):
            range_name = value_range.get("range", "")
            sheet_title = range_name.split("!", 1)[0].strip("'") if range_name else ""
            if sheet_title in task_data:
                task_data[sheet_title] = value_range.get("values", [])

    return task_data


async def get_syllabus(
        config: Config,
        disciplines: list[tuple[str, str]]) -> list[tuple[str, str, str]]:
    
    sheet: SheetsAsync = get_content_sheets_instance(config)
    read_syllabases = await sheet.read(f"{config.google.syllabus_tab}!A2:C")
    
    return read_syllabases.get("values")


async def get_prompts(
        config: Config) -> list[tuple[str, str]]:
    
    sheet: SheetsAsync = get_prompts_sheets_instance(config)
    read_prompts = await sheet.read(f"{config.google.prompt_tab}!K2:K")

    return read_prompts.get("values")


async def get_data_for_dialog(
        config: Config,
        teachers: list[Teacher],
        user_id: int) -> dict[str, dict[str, dict[str, str]]]:

    dialog_data: dict = {}

    disciplines: list[tuple[str, str]] = await get_list_of_disciplines(config, teachers, user_id)
    syllabus: list[tuple[str, str, str]] = await get_syllabus(config, disciplines)
    tasks: list[tuple[str, str, str]] = await get_list_of_tasks(config, disciplines)
    prompts: list[tuple[str, str]] = await get_prompts(config)

    for discipline_name, discipline_id in disciplines:
        dialog_data[discipline_id] = {
            "name": discipline_name,
            "syllabus": [el[2] for el in syllabus if el[0] == discipline_name][0]
            }

        for task_name, index, task_description in tasks[discipline_id]:
            dialog_data[discipline_id][index] = {
                "name": task_name,
                "description": task_description}

    dialog_data[DialogDataKeys.FOR_GEMINI] = {
        DialogDataKeys.TEMPERATURE: prompts[2][0],
        DialogDataKeys.PROMPT: prompts[-1][0]
    }

    return dialog_data



async def put_feedback(
        dialog_manager: DialogManager,
        like: bool):

    _, config, user_data = get_middleware_data(dialog_manager)
    
    sheet: SheetsAsync = get_teachers_sheets_instance(config)

    discipline_name = dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(
        DialogDataKeys.DISCIPLINE_NAME, DialogDataKeys.UNKNOWN)

    task_name = dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(
        DialogDataKeys.TASK_NAME, DialogDataKeys.UNKNOWN)

    text_from_teacher = dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(
        DialogDataKeys.TEXT_FROM_TEACHER, DialogDataKeys.UNKNOWN)

    feedback = dialog_manager.dialog_data.get(DialogDataKeys.FOR_GEMINI, {}).get(
        DialogDataKeys.FEEDBACK_TEXT, DialogDataKeys.UNKNOWN)

    await sheet.append(
        f"{user_data.id}!A1:E",
        [
            [discipline_name, task_name, text_from_teacher, feedback, int(like)]
        ]
    )
