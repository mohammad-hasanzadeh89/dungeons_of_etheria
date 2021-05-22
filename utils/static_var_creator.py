from pathlib import Path
import json
# region global_variable
male_names = ["Adam", "Loki", "Thor", "Odin", "Fenrir", "Ghoul", "Solomon", "Cain", "Lucifer", "Lazarus",
              "Judas", "John", "Mike", "Bob", "Bernard", "Gormak", "Zerof", "Mardok", "Mark"]
female_names = ["Eve", "Sylvana", "Sethi", "Sara", "Lucy", "Nina",
                "Anna", "Helga", "Helena", "Morgana", "Rose", "Valkyrie"]
places = ["Wood", "River", "Castle", "Mountain",
          "Cliff", "Valley", "Village", "City", ""]
races = ["Elf", "Orc", "Dwarf", "Human",
         "Goblin", "Demon", "Spirit", "Undead"]
prefixes = ["", "Elven", "Dwarven", "Orcish",
            "Demonic", "Holy", "Night", "Dark"]
boss_titles = ["Boss", "king", "Master"]
outlaws = ["Thug", "Bandit", "Thief",
           "Outlaws", "Necromancer", "Sorcerer", "Assassin"]
jobs = ["Carpenter", "Lumberman", "Black Smith",
        "Alchemist", "Miner", "Lord", "King", ""]
animals = ["Snake", "Viper", "Serpent", "Bear",
           "Lion", "Wolf", "Tiger", "Panter", "Wolf", "Rat", "Dragon"]
lvl = ["", "Petit", "Common", "Lieutenant", "Cheif"]
potion_size = ["Tiny", "Greate", "Heavy", "Super"]
weapons_type = ["Knife", "Dagger", "Sword", "Club", "Axe",
                "Hammer", "Long Sword", "Mace", "Wand", "Stuff"]
armors_type = ["Hat", "Robe", "Helmet",
               "Chain mail", "Shield", "Armor", "Cloak"]
items_elements = ["", "Wooden", "Iron", "Silver", "Golden", "Wind", "Earth", "Ice", "Fire",
                  "Frost", "Flame", "Lightning", "Dark", "Light"]
loots_types = ["Coin", "Ore", "Ingot", "Plate", "Cup", "Goblet", "Trinket", "Ring",
               "Bracelet", "Armlet", "Wristlet", "Necklace", "Tiara", "Crown"]
loots_elements = ["Copper", "Bronze", "Silver", "Gold", "Ether"]

room_desc = ["this room light come from two torch that flickering",
             "this room has no light but you can barely see",
             "this room light come from windows"]
char_desc = [" is an angry person with a clumsy eye", " is calm as a stone and deadly as venom",
             " has a short temper and has a red face all the time", " is ugly and fools as a troll",
             " is a deceiver and deadly as serpent"]

all_abilities = {
    "fast attack":
                {"ability_type": 0, "dice_type": 10,
                 "dice_count": 1, "base_power": 5, "mana_cost": 0, "price": 100},
    "flip attack":
                {"ability_type": 0, "dice_type": 10,
                 "dice_count": 1, "base_power": 10, "mana_cost": 0, "price": 500},
    "heavy attack":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 1, "base_power": 20, "mana_cost": 0, "price": 1000},
    "slash":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 1, "base_power": 40, "mana_cost": 0, "price": 2000},
    "wild beast":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 1, "base_power": 60, "mana_cost": 0, "price": 5000},
    "whirlwind":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 1, "base_power": 80, "mana_cost": 0, "price": 10000},
    "zen":
                {"ability_type": 1, "dice_type": 4,
                 "dice_count": 1, "base_power": 4, "mana_cost": 0, "price": 500},
    "intoxication":
                {"ability_type": 1, "dice_type": 4,
                    "dice_count": 1, "base_power": 5, "mana_cost": 0, "price": 1000},
    "nature call":
                {"ability_type": 1, "dice_type": 4,
                    "dice_count": 1, "base_power": 7, "mana_cost": 0, "price": 5000},
    "lockpicking":
                {"ability_type": 2, "dice_type": 4,
                 "dice_count": 1, "base_power": 1, "mana_cost": 0, "price": 1},
    "frost":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 2, "base_power": 10, "mana_cost": 10, "price": 100},
    "flame":
                {"ability_type": 0, "dice_type": 10,
                 "dice_count": 2, "base_power": 20, "mana_cost": 15, "price": 500},
    "blast":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 2, "base_power": 40, "mana_cost": 20, "price": 1000},
    "thunder":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 2, "base_power": 80, "mana_cost": 100, "price": 2000},
    "phoenix":
                {"ability_type": 0, "dice_type": 10,
                    "dice_count": 2, "base_power": 80, "mana_cost": 25, "price": 5000},
    "dark ritual":
                {"ability_type": 1, "dice_type": 4,
                 "dice_count": 2, "base_power": 7, "mana_cost": 5, "price": 100},
    "healing light":
                {"ability_type": 1, "dice_type": 4,
                 "dice_count": 2, "base_power": 10, "mana_cost": 5, "price": 500},
    "holy light":
                {"ability_type": 1, "dice_type": 4,
                 "dice_count": 2, "base_power": 20, "mana_cost": 5, "price": 1000},
    "divine healing":
                {"ability_type": 1, "dice_type": 4,
                 "dice_count": 2, "base_power": 100, "mana_cost": 25, "price": 5000}
}

base_power_ratios = {
    "armor": {
        "common": 1,
        "epic": 3
    },
    "weapon": {
        "common": 1,
        "epic": 3
    }
}
# endregion
# region player_desc
player_desc = """
You are an expert mage how to like sneaking around dungeons and loot them.
Merlin found you at an Orphanage in Listeriavally and taught combat skills and scrolls to you to be his legacy to the world.
After ten years, he leaves you, but you can talk to him with your magic orb.
When he was leaving, he said to you: 'do not bother me with nonsense,  contact me just when you want to learn new scrolls or combat skills.'
"""
# endregion
static_vars = {
    "player_desc": player_desc,
    "all_abilities": all_abilities,
    "char_desc": char_desc,
    "room_desc": room_desc,
    "loots_elements": loots_elements,
    "loots_types": loots_types,
    "items_elements": items_elements,
    "armors_type": armors_type,
    "weapons_type": weapons_type,
    "potion_size": potion_size,
    "lvl": lvl,
    "outlaws": outlaws,
    "boss_titles": boss_titles,
    "races": races,
    "female_names": female_names,
    "male_names": male_names,
    "base_power_ratios": base_power_ratios
}

data_folder = Path("source_data")


def source_data_dir():
    if not data_folder.is_dir():
        data_folder.mkdir(parents=True, exist_ok=True)
        return data_folder
    else:
        return data_folder


def static_vars_creator():
    if not Path.is_file(data_folder / "stcv.json"):
        with open(data_folder / "stcv.json", "w") as file:
            file.writelines(json.dumps(static_vars, indent=4))
