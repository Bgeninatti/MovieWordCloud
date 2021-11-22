import logging
import sys


def config_logger():
    '''
    Config log format and level
    '''

    #Format de logger message
    handler = logging.StreamHandler(sys.stdout)  # Sends logging output to streams
    handler.setLevel(logging.INFO)

    # Format the loggin message file
    formatter = logging.Formatter(
        '%(asctime)s - %(threadName)s - %(levelname)s: %(message)s')
    handler.setFormatter(formatter)

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                    datefmt='%I:%M:%S %p',
                    handlers=[
                        # Save into a file
                        logging.FileHandler('logs.log'),
                        # Get sistem information
                        handler
                    ])
    # TODO hacer file handler opcional en funcion de un parametro (Ej: file name que por defecto none)


