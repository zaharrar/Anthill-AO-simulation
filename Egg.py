class Egg:

    def __init__(self, position, env):
        self.moved = False
        self.position = position
        self.env = env
        self.need_cares = 20
        self.env.notify_existence(self)
