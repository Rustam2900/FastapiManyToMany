import logging


def setup_logger(name) -> logging.Logger:
    FORMAT = "[%(name)s %(module)s:%(lineno)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(
        format=FORMAT, datefmt=TIME_FORMAT, level=logging.DEBUG, filename="log-file-name.log"
    )

    logger = logging.getLogger(name)
    return logger


# in any file that import fn setup_logger from the above 'logger_config.py', you can set up local logger like:
local_logger = setup_logger(__name__)

local_logger.info(
    "I am writing to file .log. "
)
