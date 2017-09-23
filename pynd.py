
from dice import HitDice

from contextlib import contextmanager
import math
import json


class Inventory(object):
    def __init__(self, items):
        self.items = items

        if isinstance(self.items, list):
            self.items = {i['name']: i['amount'] for i in self.items}

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
        return [{"name": n, "amount": a} for n, a in self.items.items()]


class Skill(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.stat = kwargs['stat']

        self.training = kwargs.get('training', 'none')

    def set_stat_mod(self, bonus):
        self.stat_mod = mod(bonus)

    @property
    def training_mod(self):
        return {
            'perficient': 3,
            'expertic': 2 * 3,
            'none': 0
        }.get(self.training, 0)

    def get_mod(self):
        return self.stat_mod + self.training_mod

    def to_dict(self):
        ret_dict = {}
        for prop in ['name', 'stat', 'training']:
            ret_dict[prop] = eval('self.' + prop)

        return ret_dict


class Character(object):
    def load_from_file(self, character_file):
        self.char_file = character_file

        with open(character_file, "r") as char_file:
            stats = json.loads(char_file.read())

        with open("backup_" + character_file, "w") as backup:
            backup.write(json.dumps(stats))

        self.skills = [Skill(**s) for s in stats['skills']]
        self.str = stats['str']
        self.dex = stats['dex']
        self.con = stats['con']
        self.int = stats['int']
        self.wis = stats['wis']
        self.cha = stats['cha']

        for s in self.skills:
            skill_mod = eval("self." + s.stat)
            s.set_stat_mod(skill_mod)

        self.max_hp = stats['max_hp']
        self.curr_hp = stats['curr_hp']

        self.speed = stats['speed']
        self.ac = stats['ac']
        self.pass_perc = stats['pass_perc']
        self.prof_bonus = stats['prof_bonus']

        self.class_skills_list = stats['class-skills']

        self.hitdice = HitDice(self.prof_bonus, stats)
        self.inventory = Inventory(stats['inventory'])

    def save(self, char_file=""):
        stats = ['str', 'dex', 'con', 'int', 'wis', 'cha', 'max_hp',
                 'curr_hp', 'speed', 'ac', 'pass_perc', 'prof_bonus']

        saved_stats = {}
        for s in stats:
            saved_stats[s] = eval('self.' + s)

        saved_stats.update({"hitdice": self.hitdice.to_dict()})
        saved_stats.update({"inventory": self.inventory.get()})

        skills = {"skills": [s.to_dict() for s in self.skills]}
        saved_stats.update(skills)

        saved_stats.update({"class-skills": self.class_skills_list})
        with open(self.char_file, "w") as save_file:
            save_file.write(json.dumps(saved_stats, indent=2))

    @property
    def class_skills(self):
        pass

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

    def show_skills(self):
        print("|{0} Skills {0}|".format('*' * 20))
        for skill in self.skills:
            print("{:<20} : {}".format(skill.name, skill.get_mod()))

    def show_inventory(self):
        print("|{0} Inventory {0}|".format('*' * 20))
        for item, amount in self.inventory.items.items():
            print("{:<25} : {}".format(item, amount))


def mod(stat):
    return math.floor((stat - 10) / 2)


if __name__ == "__main__":
    stab = Character()

    with stab.load("benjen.json"):
        print(stab.initiative)
        stab.hitdice.use('d6')
        print(stab.curr_hp)

        stab.show_inventory()
        stab.show_skills()
