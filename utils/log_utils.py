import logging

FORMAT_LOG = '%(asctime)s %(message)s'
FORMAT_DATE = '%Y/%m/%d %I:%M:%S %p'
FILE_NAME = "log.txt"

INFO = '[INFO ]'
ERROR = '[ERROR]'
FORMAT1_LOG = "%(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"


def info_log(process_name, is_start=None):
    """
        Log the program that start or end

        is_start  = true --> Write start log

        is_start  = false --> Write end log

        is_start  is None --> Write info log
    """
    logging.basicConfig(format=FORMAT_LOG, datefmt=FORMAT_DATE,
                        filename=FILE_NAME, level=logging.INFO)
    if is_start is True:
        logging.info(get_log('Start', process_name))
    elif is_start is None:
        logging.info('[INFO]')
    else:
        logging.info(get_log('End', process_name))


def error_log(exception):
    """Log error"""
    logging.basicConfig(format=FORMAT1_LOG, datefmt=FORMAT_DATE,
                        filename=FILE_NAME, level=logging.ERROR)
    logging.error("[ERROR] %s", exception)


def get_log(status, process_name):
    """Edit info log message"""
    return INFO + ' ' + status + ' ' + process_name
