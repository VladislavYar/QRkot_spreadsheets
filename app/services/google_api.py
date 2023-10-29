from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (DRIVE, DRIVE_VERSION, FORMAT_DATETIME,
                                FREE_ROW_TABLE_PROJECTS, LOCALE,
                                RANGE_TABLE_PROJECTS, SHEETS, SHEETS_VERSION,
                                SPREADSHEETS_BODY_SHEETS,
                                TEXT_ONE_ROW_TABLE_PROJECTS,
                                TWO_ROW_TABLE_PROJECTS)


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Создаёт таблицу."""
    now_date_time = datetime.now().strftime(FORMAT_DATETIME)
    service = await wrapper_services.discover(
        SHEETS,
        SHEETS_VERSION
    )
    spreadsheet_body = {
        'properties': {'title': f'{TEXT_ONE_ROW_TABLE_PROJECTS} {now_date_time}',
                       'locale': LOCALE},
        'sheets': SPREADSHEETS_BODY_SHEETS
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Даёт доступ к таблице."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover(
        DRIVE,
        DRIVE_VERSION
    )
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        close_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """Обновляет таблицу."""
    now_date_time = datetime.now().strftime(FORMAT_DATETIME)
    service = await wrapper_services.discover(
        SHEETS,
        SHEETS_VERSION
    )
    table_values = [
        (TEXT_ONE_ROW_TABLE_PROJECTS, now_date_time),
        TWO_ROW_TABLE_PROJECTS,
        FREE_ROW_TABLE_PROJECTS

    ]

    for close_project in close_projects:
        time_was_open = str(close_project.close_date -
                            close_project.create_date)
        new_row = [close_project.name,
                   time_was_open,
                   close_project.description]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=RANGE_TABLE_PROJECTS,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
