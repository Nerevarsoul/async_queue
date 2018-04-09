import logging

class BaseConfig:

    RABBIT = {
        'host': '172.17.0.3',
        'port':  5672,
        'exchange_name': 'my_exchange',
    }

    COUNTDOWN = 5
    RETRY = 5
    PERIOD = 1
    KEY_RANGE = 60

    LOG = {
        'filename': 'log.log',
        'level': logging.INFO
    }
