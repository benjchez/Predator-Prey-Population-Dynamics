import random as rd

# Define parameters
class animal:
    def __init__(self, offense, sharing, mating, fighting):
        self.offense = offense
        self.sharing = sharing
        self.mating = mating
        self.fighting = fighting

class interaction:
    def __init__(self, animal1: animal, animal2: animal):
        self.animal1 = animal1
        self.animal2 = animal2
    def fight(self):
        outcome = self.animal1.fighting - self.animal2.fighting + rd.random() * 2 - 1
        if outcome >= 0:
            # Animal 1 is dead.



# Define mating

# Define eating

# Define dying

# Generate species