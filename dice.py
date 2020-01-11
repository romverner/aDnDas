import random

class Dice:
    def __init__(self, sides):
        self.sides = sides
        self.previous_roles = []
        self.current_role = -1

    def role(self):
        self.current_role = random.randint(1, self.sides)
        self.previous_roles.append(self.current_role)
        return self.current_role