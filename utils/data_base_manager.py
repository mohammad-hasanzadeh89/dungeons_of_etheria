from pathlib import Path
import sqlite3
import json
from models.abilities import Abilities
from models.item import *
from models.inventory import Inventory
from models.character import Character
from utils.static_var_creator import source_data_dir


data_folder = source_data_dir()
is_first = False if Path.is_file(data_folder / 'data_base.db') else True

# region global_variable
# creating an connection
conn = sqlite3.connect(data_folder / "data_base.db")
# Cursor object
cursor = conn.cursor()
# create a databse tables
players_table_create_command = """
CREATE TABLE IF NOT EXISTS players (
	id	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	name	TEXT NOT NULL UNIQUE,
	description	TEXT,
	max_health	INTEGER NOT NULL,
	health	INTEGER NOT NULL,
	max_mana	INTEGER NOT NULL,
	mana	INTEGER NOT NULL,
	armor INTEGER NOT NULL,
	weapon INTEGER NOT NULL,
	abilities TEXT NOT NULL,
	inventory TEXT NOT NULL,
	x INTEGER NOT NULL,
	y INTEGER NOT NULL,
	coin INTEGER NOT NULL
);
"""
items_table_create_command = """
CREATE TABLE IF NOT EXISTS items (
    id	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    name	TEXT NOT NULL UNIQUE,
    description	TEXT,
    price	INTEGER NOT NULL,
    type	TEXT NOT NULL,
    rarity	TEXT NOT NULL,
    ability	INTEGER,
    base_power	INTEGER,
    potion_type TEXT
);
"""
abilities_table_create_command = """
CREATE TABLE IF NOT EXISTS abilities (
    id	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    name	TEXT NOT NULL UNIQUE,
    description	TEXT,
    ability_type	INTEGER NOT NULL,
    dice	INTEGER NOT NULL,
    dice_count	INTEGER NOT NULL,
    base_power	INTEGER NOT NULL,
    mana_cost	INTEGER NOT NULL,
    price	INTEGER NOT NULL
);
"""

dungeons_table_create_command = """
CREATE TABLE IF NOT EXISTS dungeons (
	id	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	"player"	INTEGER NOT NULL UNIQUE,
	"dungeon"	BLOB NOT NULL
);
"""
# endregion


def create_tables():
    if is_first:
        cursor.execute(players_table_create_command)
        cursor.execute(items_table_create_command)
        cursor.execute(abilities_table_create_command)
        cursor.execute(dungeons_table_create_command)
        conn.commit()
    print("db connection stablished")


def fetch_dungeon(player):
    command = f"SELECT * FROM dungeons WHERE player = {player.id}"
    cursor.execute(command)
    record = cursor.fetchone()
    if record:
        return record[2]
    return record


def insert_dungeon(player, dungeon):
    record = fetch_dungeon(player)
    if record:
        update_dungeon(player, dungeon)
    else:
        str_dungeon = convert_obj_to_json(dungeon)
        command = f"INSERT INTO dungeons (player,dungeon) VALUES ({player.id},'{str_dungeon}')"
        cursor.execute(command)
        conn.commit()


def update_dungeon(player, dungeon):
    str_dungeon = convert_obj_to_json(dungeon)
    command = f"UPDATE dungeons SET dungeon = '{str_dungeon}' WHERE player = {player.id};"
    cursor.execute(command)
    conn.commit()


def remove_dungeon(player):
    command = f"DELETE FROM dungeons WHERE player = {player.id};"
    cursor.execute(command)
    conn.commit()


def fetch_player(id=-1, name=""):
    command = f"SELECT * FROM players WHERE id = {id} OR name = '{name}'"
    cursor.execute(command)
    record = cursor.fetchone()
    if record:
        abilities = {}
        inventory = Inventory()
        armor = fetch_item(id=record[7])
        weapon = fetch_item(id=record[8])
        abilities_ids = record[9].split(",")
        for ability_id in abilities_ids:
            ability_id = int(ability_id)
            ability = fetch_ability(id=ability_id)
            abilities[ability.name] = ability
        items_id = record[10].split(",")
        for item_id in items_id:
            if item_id != "":
                item_id = int(item_id)
                inventory.add(fetch_item(id=item_id), {})
        player = Character(id=record[0], name=record[1], description=record[2],
                           max_health=record[3], max_mana=record[5], abilities=abilities,
                           inventory=inventory, armor=armor, weapon=weapon, coin=record[13],
                           position=[record[11], record[12]], character_type="player")
        player.health = record[4]
        player.mana = record[6]
        return player
    return record


def insert_player(player):
    record = fetch_player(name=player.name)
    if record:
        return record
    abilities_ids = []
    inventory = []
    for key in player.abilities:
        abilities_ids.append(player.abilities[key].id)
    for item in player.inventory.get_all_items_id():
        inventory.append(item)
    abilities_ids = str(abilities_ids)[1:-1].replace(" ", "")
    inventory = str(inventory)[1:-1].replace(" ", "")
    command = 'INSERT INTO players (name, description, max_health, health, max_mana, mana, armor, weapon, ' +\
        'abilities, inventory, x, y, coin)' +\
        f'VALUES ("{player.name}", "{player.description}", {player.max_health}, {player.health}, ' +\
        f'{player.max_mana}, {player.mana}, {player.armor.id}, {player.weapon.id}, "{abilities_ids}", ' +\
        f'"{inventory}", {player.position[0]}, {player.position[1]}, {player.inventory.coin})'
    cursor.execute(command)
    player.id = cursor.lastrowid
    conn.commit()


def update_player(player):
    abilities_ids = []
    inventory = []
    for key in player.abilities:
        abilities_ids.append(player.abilities[key].id)
    for item in player.inventory.get_all_items_id():
        inventory.append(item)
    abilities_ids = str(abilities_ids)[1:-1].replace(" ", "")
    inventory = str(inventory)[1:-1].replace(" ", "")
    command = f"UPDATE players SET health = {player.health}, mana = {player.mana}, armor = {player.armor.id}, " +\
        f'weapon = {player.weapon.id},  abilities = "{abilities_ids}", inventory = "{inventory}", ' +\
        f'x = {player.position[0]}, y = {player.position[1]}, coin = {player.inventory.coin} WHERE id = {player.id}'
    cursor.execute(command)
    conn.commit()


def remove_player(name=""):
    command = ""
    cursor.execute(command)
    pass


def fetch_all_items_by_types(items_types=[]):
    command = f"SELECT * FROM items"
    if len(items_types) > 0:
        command = command + f" WHERE "
        for item_type in items_types:
            command = command + f"type = '{item_type}'"
            if len(items_types) > 1:
                command = command + " OR "
    if command[-4:] == " OR ":
        command = command[:-4]
    cursor.execute(command)
    records = cursor.fetchall()
    items = []
    for record in records:
        item = create_item(record)
        if item:
            items.append(item)
    return items


def fetch_item(id=-1, name=""):
    command = f"SELECT * FROM items WHERE id = {id} or name = '{name}'"
    cursor.execute(command)
    record = cursor.fetchone()
    return create_item(record)


def create_item(record):
    if record:
        item = None
        item_type = record[4]
        if item_type == "Scroll":
            item = Scroll(id=record[0], name=record[1], description=record[2],
                          ability=fetch_ability(id=record[6]), rarity=record[5])
        elif item_type == "Armor":
            item = Armor(id=record[0], name=record[1], description=record[2],
                         price=record[3], base_power=record[7], rarity=record[5])
        elif item_type == "Weapon":
            item = Weapon(id=record[0], name=record[1], description=record[2],
                          price=record[3], base_power=record[7], rarity=record[5])
        elif item_type == "Potion":
            item = Potion(id=record[0], name=record[1], description=record[2],
                          price=record[3], base_power=record[7], potion_type=record[8], rarity=record[5])
        elif item_type == "Misc":
            item = Misc(id=record[0], name=record[1], description=record[2],
                        price=record[3])
        return item
    else:
        return record


def insert_item(item):
    record = fetch_item(name=item.name)
    if record:
        return record
    ability = item.ability.id if hasattr(item, 'ability') else "NULL"
    base_power = item.base_power if hasattr(item, 'base_power') else "NULL"
    potion_type = item.potion_type if hasattr(item, 'potion_type') else "NULL"

    command = 'INSERT INTO items (name, description, price, type, rarity, ability, base_power, potion_type) VALUES ' +\
        f'("{item.name}", "{item.description}", {item.price}, "{type(item).__name__}", "{item.rarity}", {ability}, {base_power}, "{potion_type}")'
    cursor.execute(command)
    item.id = cursor.lastrowid
    conn.commit()


def update_item(name="", description=""):
    command = ""
    cursor.execute(command)
    pass


def remove_item(name=""):
    command = ""
    cursor.execute(command)
    pass


def fetch_all_abilities():
    command = f"SELECT * FROM abilities"
    cursor.execute(command)
    records = cursor.fetchall()
    abilities = {}
    for record in records:
        ability = Abilities(id=record[0], name=record[1], description=record[2],
                            ability_type=record[3], dice_type=record[4], dice_count=record[5],
                            base_power=record[6], mana_cost=record[7], price=record[8])
        abilities[record[1]] = ability
    return abilities


def fetch_ability(id=-1, name=""):
    command = f"SELECT * FROM abilities WHERE id = {id} or name = '{name}'"
    cursor.execute(command)
    record = cursor.fetchone()
    if record:
        ability = Abilities(id=record[0], name=record[1], description=record[2],
                            ability_type=record[3], dice_type=record[4], dice_count=record[5],
                            base_power=record[6], mana_cost=record[7], price=record[8])
        return ability
    else:
        return record


def insert_ability(ability):
    record = fetch_ability(name=ability.name)
    if record:
        return record
    command = 'INSERT INTO abilities (name, description, ability_type, dice, dice_count, base_power, mana_cost, price) VALUES ' +\
        f'("{ability.name}", "{ability.description}", {ability.ability_type}, {ability.dice.last}, ' +\
        f' {ability.dice_count}, {ability.base_power}, {ability.mana_cost}, {ability.price})'
    cursor.execute(command)
    ability.id = cursor.lastrowid
    conn.commit()


def update_ability(name="", description=""):
    command = ""
    cursor.execute(command)
    pass


def remove_ability(name=""):
    command = ""
    cursor.execute(command)
    pass


def convert_obj_to_json(obj):
    jsonStr = json.dumps(obj.to_dict())
    # jsonStr = json.dumps(obj.__dict__, default=lambda o: o.__dict__, indent=4)
    return jsonStr
