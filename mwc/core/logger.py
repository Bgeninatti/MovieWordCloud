import logging
import logging.config


class ContextLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None):
        msg = f"{msg}"
        if extra:
            msg = f"{msg}: {'; '.join((f'{k}={v}' for k, v in extra.items()))}"
        super()._log(level, msg, args, exc_info, extra)


logging.setLoggerClass(ContextLogger)


def setup_logger(lvl="info"):

    config = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime)s|[%(levelname)s]|%(module)s:%(funcName)s|%(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": lvl.upper(),
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            'mwc': {
                "handlers": ["default"],
                "level": lvl.upper(),
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)
