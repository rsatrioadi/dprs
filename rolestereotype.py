from enum import Enum

class RoleStereotype(Enum):
    CONTROLLER = ('#984ea3', '#decbe4')
    COORDINATOR = ('#4daf4a', '#ccebc5')
    INFORMATION_HOLDER = ('#e41a1c', '#fbb4ae')
    INTERFACER = ('#ff7f00', '#fed9a6')
    SERVICE_PROVIDER = ('#377eb8', '#b3cde3')
    STRUCTURER = ('#f781bf', '#fddaec')
    def __init__(self, fcolor, bcolor):
        self.fcolor = fcolor
        self.bcolor = bcolor
    def __str__(self):
        return self.name.replace('_', ' ').title()
    @classmethod
    def from_str(cls, name):
        return cls[name.replace(' ', '_').upper()]
