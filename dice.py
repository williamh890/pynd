from abc import abstractmethod
from random import randint


class Dice(object):
    @abstractmethod
    def roll(self):
        pass


class D6(Dice):
    def get_type(self):
        return "d6"

    def roll(self):
        return randint(1, 6)


class D8(Dice):
    def get_type(self):
        return "d8"

    def roll(self):
        return randint(1, 8)


class D10(Dice):
    def get_type(self):
        return "d10"

    def roll(self):
        return randint(1, 10)


class D12(Dice):
    def get_type(self):
        return "d12"

    def roll(self):
        return randint(1, 12)


class HitDice(object):
    def __init__(self, prof_bonus, stats):
        self.d6_max = stats['d6_max']
        self.d8_max = stats['d8_max']
        self.d10_max = stats['d10_max']
        self.d12_max = stats['d12_max']

        self.d6_curr = stats['d6_curr']
        self.d8_curr = stats['d8_curr']
        self.d10_curr = stats['d10_curr']
        self.d12_max = stats['d12_curr']

        self.d6 = D6()
        self.d8 = D8()
        self.d10 = D10()
        self.d12 = D12()

    def to_dict(self):
        vals = ['d6_max', 'd8_max', 'd10_max', 'd12_max',
                'd6_max', 'd8_max', 'd10_max', 'd12_max']

        ret_vals = {}
        for v in vals:
            ret_vals[v] = eval('self.' + v)

        return ret_vals

    def long_rest(self):
        self.d6_curr = self.d6_max
        self.d8_curr = self.d8_max
        self.d10_curr = self.d10_max
        self.d12_max = self.d12_max

    def use(self, die_str):
        die = {'d6': self.d6,
               'd8': self.d8,
               'd10': self.d10,
               'd12': self.d12}.get(die_str)

        if die is None:
            raise TypeError(
                "Die string is not valid, given '{}'".format(die_str))

        if '6' in die_str:
            if self.d6_curr <= 0:
                print("Out of d6 hit die")
            else:
                self.d6_curr -= 1
                return self.d6().roll()

        elif '8' in die_str:
            if self.d8_curr <= 0:
                print("Out of d6 hit die")
            else:
                self.d8_curr -= 1
                return self.d8().roll()

        elif '10' in die_str:
            if self.d10_curr <= 0:
                print("Out of d6 hit die")
            else:
                self.d10_curr -= 1
                return self.d10().roll()

        else:
            if self.d12_curr <= 0:
                print("Out of d6 hit die")
            else:
                self.d12_curr -= 1
                return self.d12().roll()
