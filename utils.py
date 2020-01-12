import logging


def logging_init(log_level=logging.DEBUG):
    log = logging.getLogger('game_logger')
    f = logging.Formatter('[%(levelname)s][%(filename)s.%(funcName)s:%(lineno)d] %(message)s')
    h = logging.StreamHandler()
    h.setFormatter(f)
    h.setLevel(log_level)
    log.addHandler(h)
    log.setLevel(log_level)
    log.propagate=False
    return log