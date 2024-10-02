import config
import logging
from logging.handlers import TimedRotatingFileHandler

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

logging_level = LOG_LEVELS.get(config.LOG_LEVEL, logging.INFO)

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging_level)  # Set the global logging level

# Create handlers
console_handler = logging.StreamHandler()  # Logs to console
console_handler.setLevel(logging_level)

file_handler = TimedRotatingFileHandler('logs/app.log', when='D', interval=1, backupCount=7)
file_handler.setLevel(logging_level)

# Create a formatter and set it for both handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
