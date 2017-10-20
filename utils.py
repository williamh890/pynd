import math


def mod(stat):
    return math.floor((stat - 10) / 2)


def get_proficiency_bonus(total_level):
    return math.floor((total_level - 1) / 4) + 2


def format_attribute(name, description):
    return "-> {} : \n\t{}\n".format(name, description)


class Attribute(object):
    def __init__(self, description, label):
        self.description = description
        self.label = label

    def _str__(self):
        return "-> {} : \n\t{}\n".format(
            self.name, self.description
        )


class Ability(Attribute):
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def __str__(self):
        ret_str = self.label.upper() + "\n"

        for attribute in self.data:
            ret_str += str(attribute)


if __name__ == "__main__":
    for x in range(1, 21):
        print("bonus: " + str(get_proficiency_bonus(x)))
