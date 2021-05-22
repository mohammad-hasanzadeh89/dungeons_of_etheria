class Item:

    def __init__(self, id=0, name="", description="", price=1, rarity="common"):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.rarity = rarity
        return self

    def use(self, user):
        result = ""
        if user.character_type != "player":
            return
        result = user.inventory.remove(self, {})
        return result

    def inspect(self):
        desc = f" {self.description} |" if self.description != "" else ""
        result = {
            "Item": self,
            "Log": [("#ffffff", f"{self.name}: {type(self).__name__} |{desc} price: {self.price} coins")]
        }
        return result

    def to_dict(self):
        _dict = self.id
        return _dict

    def __str__(self):
        return self.name + "| pirce: " + str(self.price)


class Scroll(Item):

    def __init__(self, id=0, name="", description="", ability=None, rarity="common"):
        self.ability = ability
        Item.__init__(self, id, name, description, ability.price, rarity)

    def use(self, user):
        result = {
            "Removed Scroll": self,
            "Log": [("#ffff00", f"You learned the '{self.ability.name}' scroll\n")]
        }
        user.abilities[self.ability.name] = self.ability
        user.inventory.remove(self, result)
        return result


class Armor(Item):

    def __init__(self, id=0, name="", description="", price=1, base_power=10, rarity="common"):
        self.base_power = base_power
        Item.__init__(self, id, name, description, price, rarity)

    def use(self, user):
        result = {
            "Removed Armor": self,
            "Added Armor": user.armor,
            "Log": [("#ffff00", f"you changed your armor to '{self.name}' with base_def: {self.base_power}\n")]
        }

        if user.armor.name != "":
            user.inventory.add(user.armor, result)

        user.inventory.remove(self, result)
        user.armor = self
        user.base_def = self.base_power

        return result


class Weapon(Item):

    def __init__(self, id=0, name="", description="", price=1, base_power=10, rarity="common"):
        self.base_power = base_power
        Item.__init__(self, id, name, description, price, rarity)

    def use(self, user):
        result = {
            "Removed Weapon": self,
            "Added Weapon": user.weapon,
            "Log": [("#ffff00", f"you changed your weapon to '{self.name}' with base_atk: {self.base_power}\n")]
        }

        if user.weapon.name != "":
            user.inventory.add(user.weapon, result)
            user.inventory.remove(self, result)
        else:
            user.inventory.remove(self, result)
        user.weapon = self
        user.base_atk = self.base_power

        return result


class Potion(Item):

    def __init__(self, id=0, name="", description="", price=1, base_power=20, potion_type="Health", rarity="common"):
        self.base_power = base_power
        self.potion_type = potion_type
        Item.__init__(self, id, name, description, price, rarity)

    def use(self, user, result={}):
        potion_type = ""
        color = ""
        if self.potion_type == "Health":
            potion_type = "hp"
            color = "#008000"
            user.health = user.health + \
                self.base_power if user.health < user.max_health else user.max_health
        elif self.potion_type == "Mana":
            user.mana = user.mana + self.base_power if user.mana < user.max_mana else user.max_mana
            potion_type = "mp"
            color = "#0000ff"
        if len(result) == 0:
            result = {
                "Removed Potion": self,
                "Potion User": user.name,
                "Log": [(color, f"{user.name} restored {self.base_power} {potion_type}\n")]
            }
        else:
            result["Removed Potion"]= self
            result["Potion User"]= user.name
            result["Log"].append(
                (color, f"{user.name} restored {self.base_power} {potion_type}\n"))

        user.inventory.remove(self, result)

        return result


class Misc(Item):
    def __init__(self, id=0, name="", description="", price=1):
        Item.__init__(self, id, name, description, price)

    def use(self, user):
        result = {
            "Log": [("#ffffff", f"you can't use {self.name}")]
        }
        return result
