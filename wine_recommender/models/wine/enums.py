from enum import Enum

class ExperienceLevel(Enum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'

class DrinkingFrequency(Enum):
    RARELY = 'rarely'
    OCCASIONALLY = 'occasionally'
    REGULARLY = 'regularly'
    FREQUENTLY = 'frequently'

class WineType(Enum):
    RED = 'red'
    WHITE = 'white'
    ROSE = 'rose'
    SPARKLING = 'sparkling'

class BodyType(Enum):
    LIGHT = 'light'
    MEDIUM = 'medium'
    FULL = 'full'

class SweetnessLevel(Enum):
    DRY = 'dry'
    MEDIUM = 'medium'
    SWEET = 'sweet'

class FlavorIntensity(Enum):
    LIGHT = 'light'
    MEDIUM = 'medium'
    INTENSE = 'intense' 