import logging
import os


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def init(self):
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s - %(lineno)d'
        logging.basicConfig(level=logging.DEBUG, format=log_format)

        current_file_path = os.path.abspath(__file__)

        # 获取项目根目录的路径（假设项目根目录中有README.md）
        project_root = os.path.dirname(os.path.dirname(current_file_path))

        # 获取项目名
        project_name = os.path.basename(project_root)
        self._logger = logging.getLogger(project_name)

    def setLevel(self, level):
        self._logger.setLevel(level)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self._logger.exception(msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)

    def fatal(self, msg, *args, **kwargs):
        self._logger.fatal(msg, *args, **kwargs)


logger = Logger()
