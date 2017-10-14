import math


def mod(stat):
    return math.floor((stat - 10) / 2)


def get_proficiency_bonus(total_level):
    return math.floor((total_level - 1) / 4) + 2


def format_attribute(name, description):
    return "-> {} : \n\t{}\n".format(name, description)


if __name__ == "__main__":
    for x in range(1, 21):
        print("bonus: " + str(get_proficiency_bonus(x)))
