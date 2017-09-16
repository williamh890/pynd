
from dice import HitDice

from contextlib import contextmanager
import math
import json


class Inventory(object):
    def __init__(self, items):
        self.items = {}

        for item in items:
            if isinstance(item, list):
                name, amount = item
                self.items[name] = amount
            else:
                self.items[item] = 1

    def add(self, item):
        if item in self.items:
            self.items[item] += 1
        else:
            self.item = 1

    def remove(self, item):
        if item in self.items:
            self.items[item] -= 1
        else:
            del self.item[item]

    def get(self):
        return self.items


class Character(object):
    def load_from_file(self, character_file):
        self.char_file = character_file

        with open(character_file, "r") as char_file:
            stats = json.loads(char_file.read())

        self.str = stats['str']
        self.dex = stats['dex']
        self.con = stats['con']
        self.int = stats['int']
        self.wis = stats['wis']
        self.cha = stats['cha']

        self.max_hp = stats['max_hp']
        self.curr_hp = stats['curr_hp']

        self.speed = stats['speed']
        self.ac = stats['ac']
        self.pass_perc = stats['pass_perc']
        self.prof_bonus = stats['prof_bonus']

        self.hitdice = HitDice(self.prof_bonus, stats)
        self.inventory = Inventory(stats['inventory'])

    def save(self, char_file=""):
        stats = ['str', 'dex', 'con', 'int', 'wis', 'cha', 'max_hp',
                 'curr_hp', 'speed', 'ac', 'pass_perc', 'prof_bonus']

        saved_stats = {}
        for s in stats:
            saved_stats[s] = eval('self.' + s)

        saved_stats.update(self.hitdice.to_dict())
        saved_stats.update({"inventory": self.inventory.get()})

        with open(self.char_file, "w") as save_file:
            save_file.write(json.dumps(saved_stats, indent=2))

    @property
    def stats(self):
        s_keys = ['str', 'dex', 'con', 'int', 'wis', 'cha']
        ret_stats = {}

        for stat in s_keys:
            ret_stats[stat] = eval('self.' + stat)

        return ret_stats

    @property
    def saving(self):
        throws = {mod(s) for s in self.stats}
        throws['dex'] += self.prof_bonus
        throws['wis'] += self.prof_bonus

    @property
    def initiative(self):
        return mod(self.dex)

    @contextmanager
    def load(self, character_file):
        self.load_from_file(character_file)
        yield
        self.save(character_file)


def mod(stat):
    return math.floor((stat - 10) / 2)


if __name__ == "__main__":
    stab = Character()

    with stab.load("stab.json"):
        print(stab.initiative)
        stab.hitdice.use('d6')
        print(stab.curr_hp)
        print(stab.inventory.get())
