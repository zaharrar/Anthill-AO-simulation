class Larva:

    def __init__(self, position, env):
        self.moved = False
        self.position = position
        self.env = env
        self.env.notify_existence(self)
        self.hunger_level = 5

