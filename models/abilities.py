import math
from dice.dice import Dice


class Abilities():
    """
        there are 3 type of ability: Attack = 0, Heal = 1, General = 2.
        \ndice can be one of these numbers 20, 12, 10, 8, 6, 4.
    """

    def __init__(self, id=0, name="", description="", ability_type=0, dice_type=20, dice_count=1, base_power=1, mana_cost=10, price=0):
        self.id = id
        self.name = name
        self.description = description
        self.ability_type = ability_type
        self.dice = Dice(1, dice_type)
        self.dice_count = dice_count
        self.base_power = base_power
        self.mana_cost = mana_cost
        self.price = price
        self.luck = -1

    def execute(self, executor, target, dungeon, difficulty=1):
        result = self.calculate_luck(executor, target, difficulty)
        if (self.mana_cost > 0 and executor.mana > self.mana_cost) or self.mana_cost <= 0:
            executor.mana = executor.mana - self.mana_cost
            if self.ability_type == 0:
                damage = math.floor((self.base_power * self.luck) /
                                    (self.dice.last * self.dice_count)) + executor.base_atk
                target.take_damage(damage, executor, dungeon, result)

                return result

            elif self.ability_type == 1:
                heal = math.floor((self.base_power * self.luck) /
                                  (self.dice.last * self.dice_count))

                target.healing(heal, executor, result)

                return result

            elif self.ability_type == 2:
                result["Log"].append((
                    "#ffffff", f"{executor.name} {self.name} {target.name}"))
                if self.luck >= (self.dice.last * difficulty) - 4:
                    target.locked = False

                result["IsLocked"] = target.locked

                if not target.locked:
                    result["Log"].append(("#008000", " with success\n"))
                else:
                    result["Log"].append(("#ff0000", " failed\n"))

                return result

        else:
            return result["Log"].append(("#ff0000",
                                         f"you can't preform {self.name} without at least {self.mana_cost} mp"))

    def calculate_luck(self, executor, target, difficulty):
        self.luck = 0
        if self.dice_count > 1:
            self.luck = self.dice.roll_multiply(
                self.dice_count, difficulty)[1]
        else:
            self.luck = self.dice.roll(difficulty)
        total = self.dice.last * difficulty * self.dice_count
        result = {
            "Executor": executor.name,
            "Ability": self.name,
            "Target": target.name,
            "Luck": self.luck,
            "Total": total,
            "Log": [("#ffffff", f"Name: {executor.name} | "),
                    ("#ffff00", f"Ability: {self.name}"),
                    ("#ffffff", f" | "),
                    ("#ff0000", f"On: {target.name}"),
                    ("#ffffff", f" | "),
                    ("#ffff00", f"Luck: {self.luck}/{total}\n")]
        }
        return result

    def __str__(self):
        return self.name + ": " + self.description

    def to_dict(self):
        _dict = self.name
        return _dict
