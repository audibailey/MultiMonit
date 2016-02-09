from site_config import SiteConfig
import logging

logging.basicConfig(filename=SiteConfig.home + '/log.txt', format=logging.BASIC_FORMAT)


# This class is just a wrapper class for logging functionality. For example, you may
# want to log to a file and a database table.
class Logger:
    @staticmethod
    def error(msg, ex, raise_ex=True):
        logging.error(msg + ': ' + str(ex))

        if raise_ex:
            raise ex if ex else Exception(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)
