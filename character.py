
from items import Inventory
from utils import mod, get_proficiency_bonus
from dice import HitDice
from classes import class_factory

import math
import json
from contextlib import contextmanager


class Character(object):
    def load_from_file(self, character_file):
        if character_file[-5:] != ".json":
            character_file += ".json"

        self.char_file = character_file

        with open(character_file, "r") as char_file:
            stats = json.loads(char_file.read())

        with open("backup_" + character_file, "w") as backup:
            backup.write(json.dumps(stats, indent=2))

        self.classes = [class_factory(**c) for c in stats['classes']]
        self.total_level = sum([c.level for c in self.classes])
        self.prof_bonus = get_proficiency_bonus(self.total_level)

        self.skills = [Skill(self.prof_bonus, **s) for s in stats['skills']]

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

        saved_stats.update({"classes": [c.to_dict() for c in self.classes]})

        with open(self.char_file, "w") as save_file:
            save_file.write(json.dumps(saved_stats, indent=2))

    def show(self):
        self.show_inventory()
        for c in self.classes:
            print(c)
        self.show_skills()
        self.show_mods()

    @property
    def class_skills(self):
        pass

    @property
    def stat_keys(self):
        return ['str', 'dex', 'con', 'int', 'wis', 'cha']

    @property
    def stats(self):
        ret_stats = {}

        for stat in self.stat_keys:
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

    @property
    def spell_save(self):
        return 8 + self.spell_attack_mod

    @property
    def spell_attack_mod(self):
        return mod(self.char) + self.prof_bonus

    def show_skills(self):
        print("|{0} Skills {0}|".format('*' * 20))
        for skill in self.skills:
            print("{:<20} : {}".format(skill.name, skill.get_mod()))

    def show_inventory(self):
        print("|{0} Inventory {0}|".format('*' * 20))
        for item in self.inventory.items:
            print(item)

    def show_classes(self):
        for c in self.classes:
            print(c)

    def show_mods(self):
        print("|********** MODS ************|")
        for label, stat in self.stats.items():
            print("{}    : {}".format(label, mod(stat)))


class Skill(object):
    def __init__(self, prof_bonus, **kwargs):
        self.name = kwargs['name']
        self.stat = kwargs['stat']
        self.prof_bonus = prof_bonus
        self.training = kwargs.get('training', 'none')

    def set_stat_mod(self, bonus):
        self.stat_mod = mod(bonus)

    @property
    def training_mod(self):
        return {
            'perficient': self.prof_bonus,
            'expertic': 2 * self.prof_bonus,
            'none': math.floor(self.prof_bonus / 2)
        }.get(self.training, 0)

    def get_mod(self):
        return self.stat_mod + self.training_mod

    def to_dict(self):
        ret_dict = {}
        for prop in ['name', 'stat', 'training']:
            ret_dict[prop] = eval('self.' + prop)

        return ret_dict
