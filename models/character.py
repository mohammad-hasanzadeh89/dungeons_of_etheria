import math
import random
from models.item import *
from models.inventory import Inventory


class Character:
    def __init__(self, id=0, name="", description="", max_health=100, max_mana=150, mana_regen=5, abilities={},
                 inventory=Inventory(), armor=Armor(), weapon=Weapon(), position=[0, 0], coin=0, character_type="mob"):
        self.id = id
        self.name = name
        self.description = description
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.mana_regen = mana_regen
        self.abilities = abilities
        self.inventory = inventory
        self.armor = armor
        self.base_def = armor.base_power
        self.weapon = weapon
        self.base_atk = weapon.base_power
        self.position = position
        self.inventory.coin = coin
        self.character_type = character_type

    def mana_regenerate(self):
        self.mana = self.mana + self.mana_regen if self.mana < self.max_mana else self.max_mana

    def use_potion(self, result):
        if(self.health <= (self.max_health * 20 / 100)):
            health_potions = [
                item["value"] for item in self.inventory.get_items_by_type("Potions") if item["value"].potion_type == "Health"]
            if len(health_potions) > 0:
                health_potions[0].use(self, result)
        elif(self.mana <= (self.max_mana * 20 / 100)):
            mana_potions = [
                item["value"] for item in self.inventory.get_items_by_type("Potions") if item["value"].potion_type == "Mana"]
            if len(mana_potions) > 0:
                mana_potions[0].use(self, result)

    def take_damage(self, damage, executor, dungeon, result):
        armor_take = math.floor(random.random() * self.base_def)
        calc_health = math.ceil(self.health - (damage - armor_take))
        self.health = self.health if calc_health > self.health else calc_health

        result["Damage"] = damage
        result["ArmorTake"] = armor_take
        result["Log"].append(
            ("#ffffff", f"{damage} (Damage) - {armor_take} (Armor Take) = "))
        result["Log"].append(
            ("#ff0000", f"{damage - armor_take}\n"))
        result["Log"].append(
            ("#ffffff", f"{self.name}'s "))
        result["Log"].append(
            ("#008000",
             f"Health: {self.health}/{self.max_health}\n"))
        self.use_potion(result)
        if self.health <= 0:
            self.perish(executor, dungeon, result)

    def healing(self, heal, executor, result):
        self.health = self.health + heal
        if self.health > self.max_health:
            self.health = self.max_health

        result["Heal"] = heal
        result["Log"].append(("#ffffff", f"Name: {executor.name} "))
        result["Log"].append(("#008000", f"add {heal} hp to "))
        result["Log"].append(("#ffffff", f"{self.name}\n"))
        result["Log"].append(
            ("#008000", f"{self.name}'s' health: {self.health}/{self.max_health}\n"))
        self.use_potion(result)

    def move(self, dungeon, direction=[1, 0], coefficient=1, max=2):
        result = {
            "Log": []
        }
        key, _to = self.create_vector(direction, coefficient, max)
        if key in dungeon.doors:
            if dungeon.doors[key].locked:
                result["Log"].append(
                    ("#ff0000", "the door is locked you need to unlock it with picklock.\n"))
            else:
                self.position = _to
                return ""
        else:
            result["Log"].append(
                ("#ff0000", "you can't go through the walls! you are not a ugly troll!\n"))
        return result

    def create_vector(self, direction, coefficient, max):
        x = self.position[0]
        y = self.position[1]
        _to = [0, 0]
        _to[0] = x + (direction[0] * coefficient)
        _to[1] = y + (direction[1] * coefficient)
        if _to[0] >= max and direction[1] > 0:
            _to[0] = 0
            _to[1] = y + 1
        elif _to[0] < 0 and direction[1] < 0:
            _to[0] = 0
        if _to[1] >= max:
            _to[1] = max-1
        key = None
        if (x < _to[0] and y == _to[1]) or (x > _to[0] and y < _to[1]):
            key = ((x, y), (_to[0], _to[1]))
        elif x < _to[0] and y > _to[1]:
            key = ((_to[0], _to[1]), (x, y))
        else:
            key = ((_to[0], _to[1]), (x, y))
        return key, _to

    def perish(self, killer, dungeon, result):
        key = tuple(self.position)
        if self in dungeon.rooms[key].characters:
            dungeon.rooms[key].characters.remove(self)
        if self.character_type == "boss":
            dungeon.boss.health = -1

        killer.inventory.extend(self.inventory)
        result["Log"].append(("#ff0000", f"{self.name} is perished\n"))

        loots = []
        for lst in self.inventory.get_all_list():
            for item in lst:
                loots.append(item)

        killer.inventory.add(self.armor, {})
        loots.append(self.armor)
        killer.inventory.add(self.weapon, {})
        loots.append(self.weapon)
        result["Loots"] = loots

        result["Log"].append(
            ("#ffffff", f"{killer.name} loot:\n{[item.__str__() for item in loots]}\n"))

        killer.inventory.add_or_remove_coin(
            self.inventory.coin, result, killer.character_type)

    def inspect(self):
        str_abilities = ""
        for i in self.abilities:
            str_abilities = str_abilities +\
                f"{self.abilities[i].name}: {self.abilities[i].description}\n"
        result = {
            "Name": self.name,
            "Description": self.description,
            "Max_health": self.max_health,
            "Health": self.health,
            "Max_mana": self.max_mana,
            "Mana": self.mana,
            "Armor": self.armor,
            "Base_def": self.base_def,
            "Weapon": self.base_def,
            "Base_atk": self.base_def,
            "Abilities": self.abilities,
            "Log": [("#ffffff", f"Name: {self.name}\n"),
                    ("#ffffff", f"Description: {self.description}\n"),
                    ("#008000",
                     f"Health: {self.health}/{self.max_health}"),
                    ("#ffffff", " || "),
                    ("#0000ff", f"Mana: {self.mana}/{self.max_mana}"),
                    ("#ffffff",
                     f" || Armor: {self.armor.name} || Base defence: {self.base_def}"),
                    ("#ffffff",
                     f" || Weapon: {self.weapon.name} || Base attack: {self.base_atk}\n"),
                    ("#ffff00", "Abilities:\n"),
                    ("#ffff00", f"{str_abilities}")]
        }
        return result

    def status(self):
        result = {
            "Name": self.name,
            "Max_health": self.max_health,
            "Health": self.health,
            "Max_mana": self.max_mana,
            "Mana": self.mana,
            "Log": [("#ffffff", f"Name: {self.name}  || "),
                    ("#008000",
                     f"Health: {self.health}/{self.max_health}"),
                    ("#ffffff", " || "),
                    ("#0000ff", f"Mana: {self.mana}/{self.max_mana}")]
        }
        return result

    def to_dict(self):
        _abilities = []
        for key in self.abilities:
            _abilities.append(self.abilities[key].to_dict())
        _dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "max_health": self.max_health,
            "health": self.health,
            "max_mana": self.max_mana,
            "mana": self.mana,
            "mana_regen": self.mana_regen,
            "abilities": _abilities,
            "inventory": self.inventory.to_dict(),
            "armor": self.armor.to_dict(),
            "weapon": self.weapon.to_dict(),
            "position": self.position,
            "coin": self.inventory.coin,
            "character_type": self.character_type
        }
        return _dict
