from utils import format_attribute


def class_factory(**kwargs):
    name = kwargs.get("name", "")

    if name == "Sorcerer":
        return Sorcerer(**kwargs)
    else:
        return Class(**kwargs)


class Class(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.level = kwargs['level']
        self.skills = kwargs.get('skills', [])
        self.spells = kwargs.get('spells', [])
        self.cantrips = kwargs['cantrips']

    def __str__(self):
        class_str = "|----- {} ({}) -----|\n".format(self.name, self.level)

        abilities = [(self.skills, "SKILLS"),
                     (self.spells, "SPELLS"),
                     (self.cantrips, "CANTRIPS")]

        for data, label in abilities:
            if len(data) <= 0:
                continue

            class_str += label + '\n'
            for datum in data:
                class_str += format_attribute(datum['name'],
                                              datum['description'])

        return class_str

    def to_dict(self):
        attrs = {
            "level": self.level,
            "skills": self.skills,
            "name": self.name,
            "spells": self.spells,
            "cantrips": self.cantrips
        }
        attrs.update(self.extra_class_attrs())

        return attrs

    def extra_class_attrs(self):
        return {}


class Sorcerer(Class):
    def __init__(self, **kwargs):
        self.max_sorcery_points = kwargs['max_sorcery_points']
        self.current_sorcery_points = kwargs['current_sorcery_points']

        super().__init__(**kwargs)

    def extra_class_attrs(self):
        attrs, ret_dict = ['max_sorcery_points', 'current_sorcery_points'], {}

        for attr in attrs:
            ret_dict[attr] = eval('self.' + attr)

        return ret_dict
