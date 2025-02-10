from loguru import logger

logger.add("weather_service.log", rotation="1 MB", level="INFO")


def get_logger():
    return logger
