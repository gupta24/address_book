import logging

# configure logging for log the event running on app
log_format = "%(asctime)s - %(levelname)s - %(message)s - %(filename)s - %(lineno)d"
log_level = logging.INFO
logging.basicConfig(format=log_format, level=log_level)
logger = logging.getLogger(__name__)