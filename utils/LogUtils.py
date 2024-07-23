import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path


class LogInitialization:
    def __init__(self):
        "log utils"

    def close_logger(self, logger):
        logging.shutdown()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

    def clear_handlers(self, logger):
        if logger:
            for handler in logger.handlers[:]:
                handler.close()
                logger.removeHandler(handler)

    def logger_func(self, app_name, log_level=10):
        try:
            file_format = '%(asctime)s:%(name)s:%(levelname)s - %(message)s'
            Path(os.path.join(os.getcwd(), "Logs")).mkdir(parents=True, exist_ok=True)
            Path(os.path.join(os.getcwd(), 'Logs', app_name)).mkdir(parents=True, exist_ok=True)
            handler = TimedRotatingFileHandler(os.path.join(os.getcwd(), 'Logs', app_name, str(app_name) + '.log'),
                                               when='Midnight',
                                               interval=1,
                                               backupCount=5)
            handler.setFormatter(logging.Formatter(file_format))
            handler.suffix = '%Y_%m_%d_%H_%M_%S'
            root_logger = logging.getLogger()
            self.clear_handlers(root_logger)
            root_logger.setLevel(log_level)
            root_logger.addHandler(handler)
            root_logger.propagate = False

            # Configure parso/httpx/ httpcore  logging to be less verbose or turned off
            for i in ['httpx', 'httpcore', 'parso', 'pdfminer', "openai._base_client",
                      "azure.core.pipeline.policies.http_logging_policy", "urllib3.connectionpool"]:
                parso_logger = logging.getLogger(i)
                self.clear_handlers(parso_logger)
                parso_logger.setLevel(logging.WARNING)  # Only log warnings and above

                parso_logger.propagate = False
            # return logger
        except Exception as error:
            print(' something went wrong in logger_func', error)