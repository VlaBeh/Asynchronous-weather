import logging
from loguru import logger

logger.add("weather_service.log", rotation="1 MB", level="INFO")


logger = logging.getLogger("weather_logger")
