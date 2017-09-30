


class Item(object):
    def __init__(self, name, amount=1, description=""):
        self.name = name
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "name": self.name,
            "amount": self.amount,
            "description": self.description
        }

    def __str__(self):
        item_s = "{:<30} ({}) : {}".format(
            self.name, self.amount, self.description)

        return item_s


class Inventory(object):
    def __init__(self, items):
        self.items = []

        for item_dict in items:
            new_item = Item(
                item_dict['name'],
                item_dict['amount'],
                item_dict.get('description', "")
            )

            self.items.append(new_item)

    def add(self, new_item):
        for i in self.items:
            if i.name == new_item.name:
                i.amount += 1
                break
        else:
            self.items.append(new_item)

    def remove(self, item):
        for i in self.items:
            if i.name == self.new_item.name:
                i.amount -= 1

                if i.amount == 0:
                    self.items.remove(i)
                else:
                    break

    def get(self):
        return [
            i.to_dict() for i in self.items
        ]


