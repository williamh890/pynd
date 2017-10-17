import requests
from bs4 import BeautifulSoup
import json
import time
from multiprocessing.dummy import Pool as ThreadPool
from os.path import join


class DnDWikiSpellScraper(object):
    def __init__(self):
        self.base = "https://www.dnd-spells.com"
        self.spell_page_path = "spells"

    @property
    def spell_path(self):
        return join(self.base, self.spell_page_path)

    def get_spell_list(self):
        spell_list_soup = make_soup(self.spell_path)

        table = spell_list_soup.find("tbody")
        spells_hrefs = list(set([a['href'] for a in table.find_all("a")]))

        return list(sorted(spells_hrefs, key=str.lower))

    def get(self):
        start = time.time()
        spell_links = self.get_spell_list()

        with ThreadPool(30) as pool:
            spell_dicts = pool.map(self.get_spell_json, spell_links)

        print("Total Runtime: {} seconds".format(time.time() - start))

        return [d for d in spell_dicts if d != {}]

    def get_spell_json(self, spell_url):
        try:
            spell_soup = make_soup(spell_url)

            spell_ps = [p.text.strip() for p in spell_soup.find_all("p")]
            spell_dict = SpellParser(spell_ps).to_dict()

            print(spell_dict['name'])
        except:
            print("ERROR: Could not get spell at url \n\t- {}".format(spell_url))
            spell_dict = {}

        return spell_dict


class SpellParser(object):
    def __init__(self, spell_paragraphs):
        self.ps = spell_paragraphs

    def to_dict(self):
        name = self.ps[0].split(',')[0]
        type = self.ps[1].strip()
        level = self.get_casting_info(self.ps[2])
        description = self.ps[3].strip()

        return {
            "name": name, "type": type,
            "level": level, "description": description
        }

    def get_casting_info(self, p):
        info = {}
        for line in p.split('\n'):
            label, value = line.split(":")

            label = label.strip()
            value = value.strip()

            info[label] = value

        return info


def make_soup(url):
    html = requests.get(url).text
    html = filter_html(html)

    return BeautifulSoup(html, "lxml")


def filter_html(html):
    return html.replace("\\u2019", "'")         \
        .replace("\\r\\n", " ")


def reformat_keys(_dict_list, old_key, new_key):
    for _dict in reversed(_dict_list):
        try:
            tmp = _dict[old_key]
            del _dict[old_key]
        except KeyError:
            print(json.dumps(_dict, indent=2))
            if _dict == {}:
                _dict_list.remove(_dict)
        else:
            _dict[new_key] = tmp


def spell_scrape():
    scraper = DnDWikiSpellScraper()
    spell_dicts = scraper.get()

    with open("spells.json", "w") as f:
        f.write(json.dumps(spell_dicts, indent=2))


if __name__ == "__main__":
    spell_scrape()
