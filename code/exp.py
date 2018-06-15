class Orb:
    orbs = []

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.orbs.append(self)

    def get_pos(self):
        return self.x, self.y

    def get_force(self, partner):
        pass

    def move(self, x_step, y_step=0):
        self.x += x_step
        self.y += y_step

    @classmethod
    def printall(cls):
        for orb in cls.orbs:
            print(orb.x, orb.y)
        for orb in cls.orbs:
            orb.move(11, 11)
        for orb in cls.orbs:
            print(orb.x, orb.y)


import numpy as np
a = np.array([[400.999, 500.9999], [22.9999, 25.9]])
print(a.round().astype(int))
