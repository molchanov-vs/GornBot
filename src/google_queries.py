from .utils.sheets_async import SheetsAsync
from .config import Config
from .custom_types import Teacher


async def get_teachers(config: Config) -> list[Teacher]:

    sheet = SheetsAsync(
        spreadsheet_id=config.google.feedbacks_and_accesses_id,
        sa_json_path=config.google.service_account_json
    )

    read_res = await sheet.read(f"{config.google.accesses_tab}!A1:C100")

    teachers: list[Teacher] = [
        Teacher(id=i[1], name=i[0], disciplines=i[2].split(", ")) 
        for i in read_res.get("values")[1:]]

    return teachers