from models.item import *


class Inventory():

    def __init__(self, scroll_list=[], armor_list=[], weapon_list=[],
                 potion_list=[], misc_list=[], coin=0):
        self.scroll_list = scroll_list
        self.armor_list = armor_list
        self.weapon_list = weapon_list
        self.potion_list = potion_list
        self.misc_list = misc_list
        self.coin = coin

    def add_or_remove_coin(self, amount, result, owner="not_player"):
        self.coin = self.coin + amount
        add_or_remove = ""
        if amount > 0:
            add_or_remove = "added"
        else:
            add_or_remove = "removed"
        result["TradedCoin"] = amount
        if "Log" not in result.keys():
            result["Log"] = []
        result["Log"].append(("#ffff00", f"{amount} coins {add_or_remove}\n"))
        result["Log"].append(("#ffff00", f"total coin: {self.coin}\n"))

    def remove_all(self):
        self.scroll_list = []
        self.armor_list = []
        self.weapon_list = []
        self.potion_list = []
        self.misc_list = []
        self.coin = 0
        return self

    def get_all_list(self):
        return [self.scroll_list, self.armor_list, self.weapon_list, self.potion_list, self.misc_list]

    def add(self, item, result):
        if type(item).__name__ == "Scroll":
            self.scroll_list.append(item)
        elif type(item).__name__ == "Armor":
            self.armor_list.append(item)
        elif type(item).__name__ == "Weapon":
            self.weapon_list.append(item)
        elif type(item).__name__ == "Potion":
            self.potion_list.append(item)
        else:
            self.misc_list.append(item)
        if "Log" not in result.keys():
            result["Log"] = []
        result["Log"].append(
            ("#ffffff", f"{item.name} --> price: {item.price}. added\n"))

    def remove(self, item, result):
        if type(item).__name__ == "Scroll":
            self.scroll_list.remove(item)
        elif type(item).__name__ == "Armor":
            self.armor_list.remove(item)
        elif type(item).__name__ == "Weapon":
            self.weapon_list.remove(item)
        elif type(item).__name__ == "Potion":
            self.potion_list.remove(item)
        else:
            self.misc_list.remove(item)
        if "Log" not in result.keys():
            result["Log"] = []
        result["Log"].append(
            ("#ffffff", f"{item.name} removed\n"))

    def extend(self, inventory):
        self.scroll_list.extend(inventory.scroll_list)
        self.armor_list.extend(inventory.armor_list)
        self.weapon_list.extend(inventory.weapon_list)
        self.potion_list.extend(inventory.potion_list)
        self.misc_list.extend(inventory.misc_list)
        self.coin = self.coin + inventory.coin

    def show_inventory(self):
        return {"Scrolls": [item.name for item in self.scroll_list],
                "Armors": [item.name for item in self.armor_list],
                "Weapons": [item.name for item in self.weapon_list],
                "Potions": [item.name for item in self.potion_list],
                "Miscs": [item.name for item in self.misc_list],
                "Coins": self.coin}

    def get_all_items_id(self):
        result = [item.id for item in self.scroll_list] +\
            [item.id for item in self.armor_list] +\
            [item.id for item in self.weapon_list] +\
            [item.id for item in self.potion_list] +\
            [item.id for item in self.misc_list]
        return result

    def get_all_items(self):
        result = [item for item in self.scroll_list] +\
            [item for item in self.armor_list] +\
            [item for item in self.weapon_list] +\
            [item for item in self.potion_list] +\
            [item for item in self.misc_list]
        return result

    def get_items_by_type(self, item_type):
        result = []
        if item_type == "Scrolls":
            result = [{"name": item.name, "value": item}
                      for item in self.scroll_list]
        elif item_type == "Armors":
            result = [{"name": item.name, "value": item}
                      for item in self.armor_list]
        elif item_type == "Weapons":
            result = [{"name": item.name, "value": item}
                      for item in self.weapon_list]
        elif item_type == "Potions":
            result = [{"name": item.name, "value": item}
                      for item in self.potion_list]
        else:
            result = [{"name": item.name, "value": item}
                      for item in self.misc_list]
        return result

    def to_dict(self):
        all_list = self.get_all_items()
        items = []
        for item in all_list:
            items.append(item.to_dict())
        _dict = items
        return _dict

    def count_all_item(self):
        return len(self.scroll_list) + len(self.armor_list) + len(self.weapon_list) + len(self.potion_list) + len(self.misc_list)
