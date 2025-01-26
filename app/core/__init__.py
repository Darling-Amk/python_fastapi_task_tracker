import logging

from pydantic_core import ValidationError

from app.core.config import Config

try:
    app_config: Config = Config()
except ValidationError as ex:
    logging.error(f"Ошибка загрузки конфига, проверьте наличие/актуальность .env файла\nОшибка:{ex}")
    exit(1)