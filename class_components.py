
from abc import abstractmethod


class ClassComponent(object):
    @abstractmethod
    def get_attributes(self):
        pass

    @abstractmethod
    def get_abilities(self):
        pass


class BaseComponent(ClassComponent):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.level = kwargs['level']
        self.skills = kwargs.get('skills', [])

    def get_abilities(self):
        return [(self.skills, "SKILLS")]

    def get_attributes(self):
        return [
            (self.name, "name"),
            (self.level, "level"),
            (self.skills, "skills")
        ]


class SpellComponent(ClassComponent):
    def __init__(self, **kwargs):
        self.cantrips = kwargs['cantrips']
        self.spells = kwargs['spells']

        self.spell_slots = []

    def get_abilities(self):
        return [(self.spells, "SPELLS"),
                (self.cantrips, "CANTRIPS")]

    def get_attributes(self):
        return [(self.spells, "spells"),
                (self.cantrips, "cantrips")]


class SorcererComponent(ClassComponent):
    def __init__(self, **kwargs):
        self.max_sorcery_points = kwargs['max_sorcery_points']
        self.current_sorcery_points = kwargs['current_sorcery_points']

    def get_abilities(self):
        return []

    def get_attributes(self):
        return [(self.max_sorcery_points, 'max_sorcery_points'),
                (self.current_sorcery_points, "current_sorcery_points")]


class BardComponent(ClassComponent):
    def __init__(self, **kwargs):
        pass
    def get_abilities(self):
        return []

    def get_attributes(self):
        return []
