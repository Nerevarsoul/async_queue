class BaseConfig:

    RABBIT = {
        'host': '172.17.0.3',
        'port':  5672,
        'exchange_name': 'my_exchange',
        'routing_key': 'my'
    }

    COUNTDOWN = 5
    RETRY = 5
    PERIOD = 1
