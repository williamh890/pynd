from abc import abstractmethod
from random import randint


class Dice(object):
    @abstractmethod
    def roll(self):
        pass


class RollDice(Dice):
    @abstractmethod
    def __init__(self):
        pass

    def get_type(self):
        return "d" + str(self.max)

    def roll(self):
        return randint(1, self.max)


class D6(RollDice):
    def __init__(self):
        self.max = 6


class D8(RollDice):
    def __init__(self):
        self.max = 8


class D10(RollDice):
    def __init__(self):
        self.max = 10


class D12(RollDice):
    def __init__(self):
        self.max = 12


class D20(RollDice):
    def __init__(self):
        self.max = 20


class OutOfHitDieError(Exception):
    pass


def dice_factory(lookup_str):
    try:
        return {"d6": D6(),
                "d8": D8(),
                "d10": D10(),
                "d12": D12()}[lookup_str]
    except KeyError:
        raise KeyError("Invalid dice type '{}'".format(lookup_str))


class HitDie(object):
    def __init__(self, **kwargs):
        self.dice = dice_factory(kwargs['dice'])
        self.curr = kwargs['curr']
        self.max = kwargs['max']

    def use(self):
        if self.curr > 0:
            self.curr -= 1
            return self.dice.roll()

        else:
            raise OutOfHitDieError("Out of hit dice")

    def reset(self):
        self.curr = self.max

    def to_dict(self):
        return {"dice": self.dice.get_type(),
                "max": self.max,
                "curr": self.curr}


class HitDice(object):
    def __init__(self, prof_bonus, stats):
        hitdice = stats['hitdice']
        self.dice = {d['dice']: HitDie(**d) for d in hitdice}

    def to_dict(self):
        return [d.to_dict() for d in self.dice.values()]

    def long_rest(self):
        [d.reset() for d in self.dice.values()]

    def use(self, die_str):
        try:
            return self.dice[die_str].use()
        except:
            print("out of hit {}".format(die_str))
