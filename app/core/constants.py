from app.core.config import settings

MIN_LEN_DESCRIPTION = 1
MIN_LEN_NAME = 1
MAX_LEN_NAME = 100
NO_PROJECT = 'Проект не найден!'
NO_UNIQUE_NAME = 'Проект с таким именем уже существует!'
NO_UPDATE_CLOSE_PROJECT = 'Закрытый проект нельзя редактировать!'
NO_INVESTED_AMOUNT_MORE_FULL_AMOUNT = ('Нельзя тебуемую сумму устанавливать '
                                       'ниже внесённой.')
NO_DELETE_PROJECT_INVESTED_AMOUNT = ('В проект были внесены средства, '
                                     'не подлежит удалению!')
NO_DELETE_USER = 'Удаление пользователей запрещено!'
REQUIRED = 'Обязательное поле.'
SUM_MORE_ZERO = 'Сумма пожертвования должна быть больше 0.'
DESCRIPTION_NO_LESS_MIN_LEN_DESCRIPTION = ('Поле должно быть не менее '
                                           f'{MIN_LEN_DESCRIPTION} символа.')
NAME_LEN_MIN_MAX = (f'Поле должно быть от {MIN_LEN_NAME} до '
                    f'{MAX_LEN_NAME} символов включительно.')
SCOPES = (
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
)
INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key,
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
}
FORMAT_DATETIME = '%Y/%m/%d %H:%M:%S'
SHEETS = 'sheets'
SHEETS_VERSION = 'v4'
DRIVE = 'drive'
DRIVE_VERSION = 'v3'
SPREADSHEETS_BODY_SHEETS = (
    {
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Лист1',
            'gridProperties': {
                'rowCount': 100,
                'columnCount': 11
            }
        }
    }
)
LOCALE = 'ru_RU'
RANGE_TABLE_PROJECTS = 'A1:K100'
TEXT_ONE_ROW_TABLE_PROJECTS = 'Отчет от'
TWO_ROW_TABLE_PROJECTS = ('Топ проектов по скорости закрытия', )
FREE_ROW_TABLE_PROJECTS = ('Название проекта', 'Время сбора', 'Описание')
INPUT_VALUE_OPTION_USER_ENTERED = 'USER_ENTERED'