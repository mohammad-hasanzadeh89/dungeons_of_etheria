import random
import math
from pathlib import Path
import json

from models.env import *
from models.character import Character
from models.abilities import Abilities
from models.item import *
from models.inventory import Inventory
from models.shop import Shop
from utils.static_var_creator import static_vars_creator, source_data_dir
from utils.data_base_manager import *

# region global_variable
static_vars_creator()
static_vars = {}

data_folder = source_data_dir()
with open(data_folder / "stcv.json", "r") as file:
    static_vars = json.load(file)

room_desc = static_vars["room_desc"]
all_abilities = static_vars["all_abilities"]
base_power_ratios = static_vars["base_power_ratios"]

abilities = {}
common_armors = []
common_weapons = []
common_miscs = []
common_potions = []
epic_armors = []
epic_weapons = []
epic_potions = []
items_names = [""]
# endregion


def __one_name_gen(name, first_prefix="", second_prefix="", first_suffix="", second_suffix=""):
    return f"{first_prefix} {second_prefix} {name} {first_suffix} {second_suffix}".replace("  ", " ").strip()


def character_names_gen(first_prefix=[""], second_prefix=[""], first_suffix=[""], second_suffix=[""]):
    name = ""
    gender = 0
    if random.random() >= 0.5:
        name = __one_name_gen(random.choice(static_vars["male_names"]),
                              random.choice(first_prefix), random.choice(
                              second_prefix),
                              random.choice(first_suffix), random.choice(second_suffix))
    else:
        name = __one_name_gen(random.choice(static_vars["female_names"]),
                              random.choice(first_prefix), random.choice(
                              second_prefix),
                              random.choice(first_suffix), random.choice(second_suffix))
        gender = 1
    return name, gender


def armor_gen(name="", description="", price=1, price_ratio=5, base_power_ratio=1, factor=0, rarity="common"):
    name, rand1, rand2 = item_name_gen(
        static_vars["armors_type"], static_vars["items_elements"], factor)
    base_power = item_base_power_gen(rand1, rand2, base_power_ratio)
    price = item_price_gen(rand1, rand2, price_ratio)
    item = Armor(name=name, description=f"{name} with base_def: {base_power}", price=price,
                 base_power=base_power, rarity=rarity)
    return item


def weapon_gen(name="", description="", price=1, price_ratio=4, base_power_ratio=1, factor=0, rarity="common"):
    name, rand1, rand2 = item_name_gen(
        static_vars["weapons_type"], static_vars["items_elements"], factor)
    base_power = item_base_power_gen(rand1, rand2, base_power_ratio)
    price = item_price_gen(rand1, rand2, price_ratio)
    item = Weapon(name=name, description=f"{name} with base_atk: {base_power}", price=price,
                  base_power=base_power, rarity=rarity)
    return item


def potion_gen(name="", description="", potion_type="Health", size=0, price_ratio=10, base_power_ratio=25):
    rarity = ""
    if size > (len(static_vars["potion_size"])/2) - 1:
        rarity = "epic"
    else:
        rarity = "common"
    base_power = item_base_power_gen(size, 1, base_power_ratio)
    price = item_price_gen(size, 2, price_ratio)
    item = Potion(name=name, description=f"{name} will add {base_power} {potion_type} point", price=price,
                  base_power=base_power, potion_type=potion_type, rarity=rarity)
    return item


def misc_gen(factor=0, price_ratio=2):
    name, rand1, rand2 = item_name_gen(
        static_vars["loots_types"], static_vars["loots_elements"], factor)
    price = item_price_gen(rand1, rand2, price_ratio)
    item = Misc(name=name, price=price)
    return item


def item_name_gen(item_names, item_elements, factor):
    name = ""
    while True:
        element_choices = list(range(len(item_elements)))
        rand1 = random.choices(element_choices, k=1)
        if rand1[0] + factor > len(element_choices) - 1:
            rand1 = len(element_choices) - 1
        else:
            rand1 = rand1[0] + factor
        item_element = item_elements[rand1]
        type_choices = list(range(len(item_names)))
        rand2 = random.choices(type_choices, k=1)
        if rand2[0] + factor > len(item_names) - 1:
            rand2 = len(item_names) - 1
        else:
            rand2 = rand2[0] + factor
        item_name = item_names[rand2]
        name = item_element + " " + item_name
        if name not in items_names:
            break
    items_names.append(name)
    return name, rand1, rand2


def item_price_gen(first, second, price_ratio=20):
    return (first + 1) * (second + 1) * price_ratio


def item_base_power_gen(first, second, base_power_ratio=1):
    return (first + second + 1) * base_power_ratio


def create_items(common_count=40, epic_count=10):

    if is_first:
        print("creating items...")
        for _ in range(0, common_count):
            armor = armor_gen(
                base_power_ratio=base_power_ratios["armor"]["common"])
            insert_item(armor)
            common_armors.append(armor)
            weapon = weapon_gen(
                base_power_ratio=base_power_ratios["weapon"]["common"])
            insert_item(weapon)
            common_weapons.append(weapon)
            misc = misc_gen()
            insert_item(misc)
            common_miscs.append(misc)
        for _ in range(0, epic_count):
            armor = armor_gen(
                base_power_ratio=base_power_ratios["armor"]["epic"], factor=2, rarity="epic")
            insert_item(armor)
            epic_armors.append(armor)
            weapon = weapon_gen(
                base_power_ratio=base_power_ratios["weapon"]["epic"], factor=2, rarity="epic")
            insert_item(weapon)
            epic_weapons.append(weapon)
            misc = misc_gen(factor=2)
            insert_item(misc)
            common_miscs.append(misc)
        for size in static_vars["potion_size"]:
            helath_potion = potion_gen(
                name=f"{size} healing", size=static_vars["potion_size"].index(size), potion_type="Health")
            insert_item(helath_potion)
            mana_potion = potion_gen(
                name=f"{size} mana flask", size=static_vars["potion_size"].index(size), potion_type="Mana")
            insert_item(mana_potion)
            if helath_potion.rarity == "epic":
                epic_potions.append(helath_potion)
                epic_potions.append(mana_potion)
            else:
                common_potions.append(helath_potion)
                common_potions.append(mana_potion)
    else:
        print("fetching items...")
        all_items = fetch_all_items_by_types(
            ["Armor", "Weapon", "Potion", "Misc"])
        for item in all_items:
            if type(item).__name__ == "Armor":
                if item.rarity == "epic":
                    epic_armors.append(item)
                elif item.rarity == "common":
                    common_armors.append(item)
            elif type(item).__name__ == "Weapon":
                if item.rarity == "epic":
                    epic_weapons.append(item)
                elif item.rarity == "common":
                    common_weapons.append(item)
            elif type(item).__name__ == "Potion":
                if item.rarity == "epic":
                    epic_potions.append(item)
                elif item.rarity == "common":
                    common_potions.append(item)
            else:
                common_miscs.append(item)


def create_abilities(abilities_key_list=list(all_abilities.keys())):
    _abilities = {}
    if is_first:
        print("creating abilities...")
        for key in abilities_key_list:
            values = all_abilities[key]
            desc = ""
            if values["ability_type"] == 0:
                desc = desc + "attack target with "
                if values["mana_cost"] != 0:
                    desc = desc + "magic force and it's base power is " + \
                        str(values["base_power"])
                else:
                    desc = desc + "combat skills and it's base power is " + \
                        str(values["base_power"])
            elif values["ability_type"] == 1:
                desc = desc + "heal target with "
                if values["mana_cost"] != 0:
                    desc = desc + "magic force and it's base power is " + \
                        str(values["base_power"])
                else:
                    desc = desc + "meditation and it's base power is " + \
                        str(values["base_power"])
            else:
                desc = desc + "is useful to "
                if values["ability_type"] == 2:
                    desc = desc + f"cracking door locks."
            _abilities[key] = Abilities(name=key, description=desc, ability_type=values["ability_type"], dice_type=values["dice_type"], dice_count=values["dice_count"],
                                        base_power=values["base_power"], mana_cost=values["mana_cost"], price=values["price"])
        for key in _abilities:
            insert_ability(_abilities[key])
    else:
        print("fetching abilities...")
        _abilities = fetch_all_abilities()
    return _abilities


def create_scrolls(abilities):
    _scrolls = []
    if is_first:
        for key in abilities:
            ability = abilities[key]
            name = "scroll of " + ability.name
            _scroll = Scroll(name=name, description=ability.description,
                             ability=ability)
            insert_item(_scroll)
            _scrolls.append(_scroll)
    else:
        _scrolls = fetch_all_items_by_types(["Scroll"])
    return _scrolls


def room_description_gen(dungeon_doors, room):
    room.description = ""
    desc = []
    desc.append(("#ffffff", f"room {room}"))
    desc.append(("#ffffff", f"\n{random.choice(room_desc)}\n"))
    x = room.position[0]
    y = room.position[1]
    doors = [d for d in dungeon_doors.values() if d._from == (x, y)
             or d._to == (x, y)]
    if len(doors) > 0:
        if len(doors) > 1:
            desc.append(("#ffffff", f"this room has {len(doors)} doors\n"))
        else:
            desc.append(("#ffffff", f"this room has {len(doors)} door\n"))
        for door in doors:
            direction = ""
            if x < door._from[0] and y > door._from[1]:
                direction = "Down"
            elif x < door._to[0]:
                direction = "East"
            elif y > door._from[1]:
                direction = "South"
            elif x > door._to[0] and y < door._to[1]:
                direction = "Up"
            elif x > door._from[0]:
                direction = "West"
            elif y < door._to[1]:
                direction = "North"
            desc.append(("#ffff00", f"{direction } door"))
            if door.locked:
                desc.append(("#ff0000", f" is locked.\n"))
            else:
                desc.append(("#008000", f" is unlocked.\n"))

    if len(room.characters) > 0:
        tobe = ""
        if len(room.characters) > 1:
            tobe = "are"
        else:
            tobe = "is"
        desc.append(
            ("#ffffff", f"There {tobe} {len(room.characters)} person in this room.\n"))
        for characters in room.characters:
            desc.append(
                ("#ff0000", f"this person name is {characters.name}\n"))
    else:
        desc.append(("#ffffff", "there is no one in this room\n"))
    return desc


def character_gen(character_type="", difficulty=0, _name="", abilities={}, _position=[0, 0], armor=None, weapon=None, _inventory=None, heal_abilities=[], attack_abilities=[]):
    # TODO ADD Base_power_ratio list arg
    # TODO potion add to mob and boss
    # TODO use potion for mob and boss with log
    name = ""
    description = ""
    max_health = 100
    max_mana = 150
    rand_abilities = []
    _abilities = {}
    inventory = Inventory()
    inventory = inventory.remove_all()
    coin = 0
    if character_type.lower() == "mob":
        name, gender = character_names_gen(first_prefix=static_vars["lvl"],
                                           second_prefix=static_vars["outlaws"], second_suffix=static_vars["races"])
        description = character_description_gen(name, gender)
        max_health = math.floor((1 + random.random()) * 100)
        max_mana = math.floor((1 + random.random()) * 150)
        armor = common_armors[random.randint(0, len(common_armors)-1)]
        weapon = common_weapons[random.randint(0, len(common_weapons)-1)]
        name_parts = name.split(" ")
        if len(name_parts) > 3:
            lvl_index = static_vars["lvl"].index(name_parts[0])
            if lvl_index > 1:
                inventory.add(random.choice(common_potions), {})
        coin = random.randint(1, difficulty+1) * 14
        rand_heal_abilities = random.choice(heal_abilities)
        _abilities[rand_heal_abilities] = abilities[rand_heal_abilities]
        rand_attack_abilities = random.choice(attack_abilities)
        _abilities[rand_attack_abilities] = abilities[rand_attack_abilities]
        for _ in range(random.randint(1, difficulty + 1)):
            inventory.add(
                common_miscs[random.randint(0, len(common_miscs)-1)], {})
    elif character_type.lower() == "boss":
        name, gender = character_names_gen(first_prefix=static_vars["outlaws"],
                                           second_prefix=static_vars["races"], second_suffix=static_vars["races"])
        description = character_description_gen(name, gender)
        max_health = math.floor(
            ((1 + random.random()) * 100) + (100 * difficulty))
        max_mana = math.floor(
            ((1 + random.random()) * 150) + (100 * difficulty))
        armor = epic_armors[random.randint(0, len(epic_armors)-1)]
        weapon = epic_weapons[random.randint(0, len(epic_weapons)-1)]
        inventory.add(random.choice(common_potions), {})
        inventory.add(random.choice(epic_potions), {})
        coin = random.randint(difficulty, difficulty*2) * 110
        rand_abilities = random.choices(
            list(abilities.keys()), k=random.randint(difficulty, len(abilities)-1))
        rand_abilities.append(random.choice(heal_abilities))
        for key in rand_abilities:
            _abilities[key] = abilities[key]
        for _ in range(random.randint(difficulty, difficulty*2)):
            inventory.add(
                common_miscs[random.randint(0, len(common_miscs)-1)], {})
            inventory.add(
                common_miscs[random.randint(0, len(common_miscs)-1)], {})
    elif character_type.lower() == "player":
        name = _name
        description = static_vars["player_desc"]
        max_health = math.floor((1 + random.random()) * 100)
        max_mana = math.floor((1 + random.random()) * 150)
        _abilities = abilities
        if _inventory:
            inventory = _inventory
        coin = 50
    return Character(name=name, description=description, max_health=max_health, max_mana=max_mana, abilities=_abilities,
                     inventory=inventory, armor=armor, weapon=weapon, position=_position, coin=coin, character_type=character_type)


def character_description_gen(name, gender=3):
    pronoun = "he" if gender < 1 else "she"
    values = name.split(" ")
    race = values[-1]
    first_name = values[-2]
    profession = values[-3]
    result = f"this is {first_name}, " + pronoun + \
        f" is {race}. " + pronoun + f" is {profession}\n"
    result = result + pronoun + random.choice(static_vars["char_desc"])
    return result


def spawn_enemies_and_add_room_description(dungeon, dungeon_abilities, heal_abilities, attack_abilities):
    for key in dungeon.rooms:
        x = key[0]
        y = key[1]
        for _ in range(0, dungeon.rooms[key].difficulty):
            character = character_gen(character_type="mob", difficulty=random.randint(
                0, dungeon.rooms[key].difficulty), abilities=dungeon_abilities, _position=[x, y], heal_abilities=heal_abilities, attack_abilities=attack_abilities)
            dungeon.rooms[key].characters.append(character)
            description = room_description_gen(
                dungeon_doors=dungeon.doors, room=dungeon.rooms[key])
            dungeon.rooms[key].description = description
    return dungeon


def spawn_boss(dungeon, boss):
    x = dungeon.dungeon_size-1
    y = dungeon.dungeon_size-1
    dungeon.boss = boss
    dungeon.rooms[(x, y)].characters.append(dungeon.boss)
    return dungeon


def dungeon_gen(abilities, dungeon_difficulty=3, dungeon_size=3):
    # add to dict for dungeon abilities one for heal and one for attack
    # to add each character at least one of each
    create_items()
    print("create dungeon")
    _dungeon_abilities = {}
    _dungeon_abilities = abilities.copy()

    del _dungeon_abilities["lockpicking"]
    mob_abilities = {}
    boss_abilities = {}

    mob_heal_abilities = []
    mob_attack_abilities = []
    boss_heal_abilities = []

    for key in _dungeon_abilities:
        if _dungeon_abilities[key].price < 2000:
            mob_abilities[key] = _dungeon_abilities[key]
            if _dungeon_abilities[key].ability_type == 0:
                mob_attack_abilities.append(key)
            else:
                mob_heal_abilities.append(key)

        elif _dungeon_abilities[key].price > 1000:
            boss_abilities[key] = _dungeon_abilities[key]
            if _dungeon_abilities[key].ability_type == 1:
                boss_heal_abilities.append(key)
    dungeon = Dungeon(dungeon_difficulty, dungeon_size)
    dungeon = dungeon.create_dungeon()
    boss = character_gen(character_type="boss", difficulty=dungeon.difficulty,
                         abilities=boss_abilities, _position=[
                             dungeon_size-1, dungeon_size-1],
                         heal_abilities=boss_heal_abilities)
    dungeon = spawn_boss(dungeon, boss)
    dungeon = spawn_enemies_and_add_room_description(
        dungeon, mob_abilities, mob_heal_abilities, mob_attack_abilities)
    return dungeon


def shop_gen(name="shop", description="this a shop", commission=5, shop_type="All", abilities=None):
    if shop_type == "Merlin":
        name = "Merlin Shop"
        # description = "Merlin sells scrolls of knowledge that you can learn new abilities from them or you can sell scroll to him."
        description = "Merlin buy and sell everything, even souls of mortals"
        commission = 2
        shop = Shop(0, name, description, commission, Inventory(
            scroll_list=create_scrolls(abilities), armor_list=epic_armors, weapon_list=epic_weapons, potion_list=epic_potions, misc_list=[], coin=10000000))
    elif shop_type == "Blacksmith":
        name = "Vulcan Blacksmith"
        description = "Vulcan epic weapons and armors"
        commission = 10
        shop = Shop(0, name, description, commission, Inventory(
            armor_list=epic_armors, weapon_list=epic_weapons))
    elif shop_type == "Apothecary":
        shop = Shop(0, name, description, commission,
                    Inventory(potion_list=epic_potions))
    else:
        name = "Mercury shop"
        description = "Mercury buy and sell everything, even souls of mortals"
        commission = 20
        shop = Shop(0, name, description, commission, Inventory(
            armor_list=epic_armors, weapon_list=epic_weapons, potion_list=epic_potions))
    return shop


def create_dungeon_from_json(abilities, json_data):
    if json_data:
        create_items()
        print("loading dungeon")
        all_items = common_armors + common_weapons + common_potions + common_miscs
        all_items = all_items + epic_armors + epic_weapons + epic_potions

        dun = json.loads(json_data)

        _dungeon_size = dun["dungeon_size"]
        _difficulty = dun["difficulty"]
        _boss = create_character_from_json(abilities, all_items, dun["boss"])

        _rooms = create_rooms_from_json(abilities, all_items, dun["rooms"])
        _doors = create_doors_from_json(dun["doors"])

        dungeon = Dungeon(difficulty=_difficulty, dungeon_size=_dungeon_size)
        dungeon.boss = _boss
        dungeon.rooms = _rooms
        dungeon.doors = _doors

        return dungeon


def create_character_from_json(abilities, all_items, character_dict):
    _abilities = {}
    for ability_dict in character_dict["abilities"]:
        ability = abilities[ability_dict]
        _abilities[ability.name] = ability
    _armor = character_dict["armor"]
    _weapon = character_dict["weapon"]
    _inventory = Inventory()
    _inventory.remove_all()
    char_inventory = character_dict["inventory"]
    for item in all_items:
        if _inventory.count_all_item() >= len(char_inventory) and type(_armor) == Armor and type(_weapon) == Weapon:
            break
        elif item.id == _armor:
            _armor = item
            continue
        elif item.id == _weapon:
            _weapon = item
            continue
        elif item.id in char_inventory:
            for _ in range(char_inventory.count(item.id)):
                _inventory.add(item, {})
            continue

    if _inventory.count_all_item() < len(char_inventory):
        raise Exception("lost some item")
    return Character(id=character_dict["id"], name=character_dict["name"], description=character_dict["description"],
                     max_health=character_dict["max_health"], max_mana=character_dict[
                         "max_mana"], mana_regen=character_dict["mana_regen"],
                     abilities=_abilities, inventory=_inventory, armor=_armor, weapon=_weapon,
                     position=character_dict["position"], coin=character_dict["coin"], character_type=character_dict["character_type"])


def create_doors_from_json(doors_dict):
    doors = {}
    for key in doors_dict:
        name = doors_dict[key]["name"]
        locked = doors_dict[key]["locked"]
        difficulty = doors_dict[key]["difficulty"]
        _from = tuple(doors_dict[key]["_from"])
        _to = tuple(doors_dict[key]["_to"])
        _key = eval(key)
        _door = Door(_from=_from, _to=_to, name=name,
                     locked=locked, difficulty=difficulty)
        doors[_key] = _door
    return doors


def create_rooms_from_json(abilities, all_items, rooms_dict):
    rooms = {}
    for key in rooms_dict:
        values = rooms_dict[key]
        _position = tuple(values["position"])
        _description = values["description"]
        _difficulty = values["difficulty"]
        _characters = []
        for character in values["characters"]:
            _characters.append(create_character_from_json(
                abilities, all_items, character))
        rooms[_position] = Room(characters=_characters, position=_position,
                                description=_description, difficulty=_difficulty)
    return rooms
