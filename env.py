import logging

logging.info("getting resources from env")
env_const = 42


class EnvObject():
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def do_work(self):
        self.x_pos = self.x_pos + 2
        

if __name__ == "__main__":
    logging.info("in main of env")
    eo = EnvObject(4, 8)
    eo.do_work()