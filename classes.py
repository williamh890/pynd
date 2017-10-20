from utils import format_attribute
from class_components import ClassComponent, BaseComponent, SpellComponent, SorcererComponent, BardComponent


def class_factory(**kwargs):
    name = kwargs.get("name", "")

    if name == "Sorcerer":
        return Sorcerer(**kwargs)
    elif name == "Bard":
        return Bard(**kwargs)
    else:
        return DefaultClass(**kwargs)


class Class(object):
    def __init__(self, components):
        self.abilities = []
        self.attributes = []

        for component in components:
            if not isinstance(component, ClassComponent):
                raise TypeError("invalid compenent type")

            self.abilities += component.get_abilities()
            self.attributes += component.get_attributes()

        for attr, label in self.attributes:
            setattr(self, label, attr)

    def __str__(self):
        class_str = "|----- {} ({}) -----|\n".format(self.name, self.level)

        for data, label in self.abilities:
            if len(data) < 1:
                continue

            class_str += label + '\n'
            for datum in data:
                class_str += format_attribute(datum['name'],
                                              datum['description'])

        return class_str

    def to_dict(self):
        attr_dict = {}

        for attr, label in self.attributes:
            attr_dict[label] = attr

        return attr_dict


class DefaultClass(Class):
    def __init__(self, **kwargs):
        components = [
            BaseComponent(**kwargs)
        ]

        super().__init__(components)


class Sorcerer(Class):
    def __init__(self, **kwargs):
        components = [
            BaseComponent(**kwargs),
            SpellComponent(**kwargs),
            SorcererComponent(**kwargs)
        ]

        super().__init__(components)


class Bard(Class):
    def __init__(self, **kwargs):
        components = [
            BaseComponent(**kwargs),
            SpellComponent(**kwargs),
            BardComponent(**kwargs)
        ]
        super().__init__(components)
