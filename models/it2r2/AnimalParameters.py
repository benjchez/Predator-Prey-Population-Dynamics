from dataclasses import dataclass

@dataclass
class AnimalParameters:
    '''
    a is probability that if a prey gets paired with a predator, it will die
    b is probability that if a predator gets paired with a prey, it will reproduce
    c is probability that a prey will reproduce
    d is probability of death for a predator
    '''
    a: float
    b: float
    c: float
    d: float 