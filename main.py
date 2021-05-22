import random
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from utils.generators import *
from utils.logger import Logger
from utils.data_base_manager import *
# region global_variable
logger = Logger.instance()
logger.log_type = 0
dungeon_size = 3
dungeon_difficulty = 3
create_tables()

directions = [{"name": "East", "value": [1, 0]}, {"name": "North", "value": [0, 1]},
              {"name": "West", "value": [-1, 0]},
              {"name": "South", "value": [0, -1]},
              {"name": "Down", "value": [dungeon_size-1, -1]},
              {"name": "Up", "value": [dungeon_size, 1]}]
player = None
# endregion

# region methods and function


def create_new_dungeon():
    _dungeon = dungeon_gen(
        abilities, dungeon_difficulty=dungeon_difficulty,
        dungeon_size=dungeon_size)
    player.position = [0, 0]
    player.health = player.max_health
    player.mana = player.max_mana
    return _dungeon


def load_save_or_new_game():
    _dungeon = None
    inner_command = inquirer.select(
        message="Do you want to continue from the last save?:",
        choices=["Yes", "No", "Quit"],
        default=None,
    ).execute()
    if inner_command == "Quit":
        quit()
    elif inner_command == "Yes":
        _dungeon = create_dungeon_from_json(
            abilities=abilities, json_data=fetch_dungeon(player))
    elif inner_command == "No":
        _dungeon = create_new_dungeon()
    return _dungeon


def save():
    print("start")
    if dungeon:
        print("saving...")
        if dungeon.boss.health > 0:
            insert_dungeon(player, dungeon)
            update_player(player)
            print("save dungeon...")
        else:
            print("updating save file...")
            remove_dungeon(player)
            update_player(player)
        update_player(player=player)


def is_game_over(dungeon):
    if player.health <= 0:
        logger.add_log("""
        -------------------------------------------------
                            GAME OVER
        -------------------------------------------------
        """)
        quit()
        return dungeon
    elif dungeon.boss.health <= 0:
        logger.add_log("""
        -------------------------------------------------
                            Victory
        -------------------------------------------------
        """)
        save()
        quit()


def next_turn():
    player.mana_regenerate()
    for character in dungeon.rooms[tuple(player.position)].characters:
        character.mana_regenerate()
    logger.add_log(player.status()["Log"])


def command_checker(uinput):
    if uinput == "Quit":
        save()
        quit()
    else:
        if uinput == "Description":
            log_room_desc(uinput)
        elif uinput == "Inventory":
            logger.add_log(player.inventory.show_inventory(), uinput)
            while True:
                inner_command = inquirer.select(
                    message="Select a category:",
                    choices=["Scrolls", "Armors", "Weapons",
                             "Potions", "Miscs", "Back", ],
                    default=None,
                ).execute()
                if inner_command == "Back":
                    break
                else:
                    item = inquirer.select(
                        message="Select an item to inspect:",
                        choices=player.inventory.get_items_by_type(inner_command) +
                        ["Back", ],
                        default=None,
                    ).execute()
                    if item == "Back":
                        continue
                    else:
                        logger.add_log(item.inspect()["Log"],
                                       uinput + " inspect")
                        while True:
                            choice = inquirer.select(
                                message=f"Do you want to use {item.name}:",
                                choices=["Yes", "No"],
                                default=None,
                            ).execute()
                            if choice == "No":
                                break
                            else:
                                logger.add_log(item.use(player)[
                                               "Log"], "Use " + item.name)
                                next_turn()
                                break
        elif uinput == "Merlin Shop":
            logger.add_log(merlin_Shop.show_shop()["Log"], uinput)
            while True:
                category = inquirer.select(
                    message="Select a category:",
                    choices=["Scrolls", "Armors", "Weapons",
                             "Potions", "Miscs", "Back", ],
                    default=None,
                ).execute()
                if category == "Back":
                    break
                else:
                    while True:
                        trade_type = inquirer.select(
                            message=f"Select a trade type for {category}:",
                            choices=["Buy", "Sell", "Sell All", "Back", ],
                            default=None,
                        ).execute()
                        if trade_type == "Back":
                            break
                        elif trade_type == "Buy":
                            while True:
                                item_to_buy = inquirer.select(
                                    message="Select a item to inspect:",
                                    choices=merlin_Shop.inventory.get_items_by_type(
                                        category) + ["Back", ],
                                    default=None,
                                ).execute()
                                if item_to_buy == "Back":
                                    break
                                else:
                                    logger.add_log(
                                        item_to_buy.inspect()["Log"], category)
                                    confirmation = inquirer.select(
                                        message="Do want to buy it?:",
                                        choices=["Yes", "No", ],
                                        default=None,
                                    ).execute()
                                    if confirmation == "No":
                                        break
                                    else:
                                        result = merlin_Shop.buy_from_shop(
                                            item_to_buy, player)
                                        logger.add_log(
                                            result["Log"], f"Buy {item_to_buy.name}")
                                        next_turn()
                                        continue
                        elif trade_type == "Sell":
                            while True:
                                item_to_sell = inquirer.select(
                                    message="Select a trade type:",
                                    choices=player.inventory.get_items_by_type(
                                        category) + ["Back", ],
                                    default=None,
                                ).execute()
                                if item_to_sell == "Back":
                                    break
                                else:
                                    logger.add_log(
                                        item_to_sell.inspect()["Log"], category)
                                    confirmation = inquirer.select(
                                        message="Do want to sell it?:",
                                        choices=["Yes", "No", ],
                                        default=None,
                                    ).execute()
                                    if confirmation == "No":
                                        break
                                    else:
                                        result = merlin_Shop.sell_to_shop(
                                            item_to_sell, player)
                                        logger.add_log(
                                            result["Log"], f"Sell {item_to_sell.name}")
                                        next_turn()
                                        continue
                        elif trade_type == "Sell All":
                            confirmation = inquirer.select(
                                message=f"Do want to sell all {category}?:",
                                choices=["Yes", "No", ],
                                default=None,
                            ).execute()
                            if confirmation == "No":
                                break
                            else:
                                for item in player.inventory.get_items_by_type(category):
                                    result = merlin_Shop.sell_to_shop(
                                        item["value"], player)
                                    logger.add_log(
                                        result["Log"], f"Sell All {category}")
                                next_turn()
                                continue
        elif uinput == "Inspect":
            characters_name = [{"name": ch.name, "value": ch} for ch in dungeon.rooms[tuple(
                player.position)].characters]
            while True:
                selected_character = inquirer.select(
                    message="Select a character to inspect:",
                    choices=["Your self"] + characters_name + ["Back", ],
                    default=None,
                ).execute()
                if selected_character == "Your self":
                    logger.add_log(player.inspect()["Log"], uinput +
                                   " " + selected_character)
                    next_turn()
                elif selected_character == "Back":
                    break
                else:
                    logger.add_log(selected_character.inspect()["Log"], uinput)
                    next_turn()
        elif uinput == "Wait":
            next_turn()
        elif uinput == "Go to":
            while True:
                inner_command = inquirer.select(
                    message="Select a direction to go to:",
                    choices=directions + ["Back", ],
                    default=None,
                ).execute()
                dir_name = ""
                if inner_command == "Back":
                    break
                else:
                    for item in directions:
                        if type(inner_command) != str and item["value"] == inner_command:
                            dir_name = item["name"]
                    if len(dungeon.rooms[tuple(player.position)].characters) > 0:
                        logger.add_log(
                            [("#ff0000", "for moving to another room you need to kill all enemies in this one")],
                            uinput + " " + dir_name)
                        break
                    result = player.move(
                        dungeon, direction=inner_command, max=dungeon.dungeon_size)
                    if result == "":
                        log_room_desc()
                        next_turn()
                    else:
                        logger.add_log(result["Log"])
        elif uinput == "Abilities":
            while True:
                inner_command = inquirer.select(
                    message="Select an ability to use:",
                    choices=list(player.abilities.keys()) + ["Back", ],
                    default=None,
                ).execute()
                if inner_command == "Back":
                    break
                elif inner_command == "lockpicking":
                    if len(dungeon.rooms[tuple(player.position)].characters) > 0:
                        log_room_desc()
                        logger.add_log(
                            [("#ff0000", "you need to kill these persons first")], inner_command)
                        return
                    else:
                        while True:
                            direction = inquirer.select(
                                message="Select a door direction to go cracking it's lock:",
                                choices=directions + ["Back", ],
                                default=None,
                            ).execute()
                            dir_name = ""
                            for item in directions:
                                if type(direction) != str and item["value"] == direction:
                                    dir_name = item["name"]
                            if direction == "Back":
                                break
                            else:
                                key, _to = player.create_vector(
                                    direction, 1, dungeon.dungeon_size)
                                if key in dungeon.doors and dungeon.doors[key].locked:
                                    result = player.abilities["lockpicking"].execute(
                                        player, dungeon.doors[key], dungeon, dungeon.doors[key].difficulty)
                                    dungeon.doors[key].locked = result["IsLocked"]
                                    logger.add_log(
                                        result["Log"], inner_command)
                                    if not dungeon.doors[key].locked:
                                        dungeon.rooms[key[0]].description = room_description_gen(
                                            dungeon.doors, dungeon.rooms[key[0]])
                                        dungeon.rooms[key[1]].description = room_description_gen(
                                            dungeon.doors, dungeon.rooms[key[1]])
                                elif key not in dungeon.doors:
                                    logger.add_log(
                                        [("#ff0000", "there is no door in this direction")], inner_command)
                                else:
                                    logger.add_log(
                                        [("#ffff00", "This door is not locked. Why you try to pick-locking it? just pass-through it")], inner_command)
                            next_turn()
                else:
                    characters = dungeon.rooms[tuple(
                        player.position)].characters
                    characters_list = [{"name": ch.name, "value": ch}
                                       for ch in characters]
                    character = inquirer.select(
                        message=f"Select a character to use {inner_command}:",
                        choices=characters_list + ["Your Self"] + ["Back", ],
                        default=None,
                    ).execute()
                    if character == "Your Self":
                        result = player.abilities[inner_command].execute(
                            executor=player, target=player, dungeon=dungeon)
                        logger.add_log(
                            result["Log"], inner_command + " on yourself")
                        is_game_over(dungeon)
                        next_turn()
                    elif character == "Back":
                        continue
                    else:
                        target = character
                        ability = player.abilities[inner_command]
                        result = ability.execute(
                            executor=player, target=target, dungeon=dungeon)
                        logger.add_log(result["Log"], inner_command +
                                       " on " + character.name)
                        if target.health <= 0:
                            dungeon.rooms[tuple(player.position)].description = room_description_gen(
                                dungeon_doors=dungeon.doors, room=dungeon.rooms[tuple(player.position)])
                            is_game_over(dungeon)
                        else:
                            ability = random.choice(
                                list(target.abilities.values()))
                            if ability.ability_type == 0:
                                result = ability.execute(
                                    executor=target, target=player, dungeon=dungeon)
                                logger.add_log(
                                    result["Log"], "Enemy attack you")
                                is_game_over(dungeon)
                            else:
                                result = ability.execute(
                                    executor=target, target=target, dungeon=dungeon)

                                logger.add_log(
                                    result["Log"], "Enemy Heal self")
                        next_turn()


def log_room_desc(command=""):
    logger.add_log(
        dungeon.rooms[tuple(player.position)].description, command)
# endregion


abilities = create_abilities()
dungeon = None
# dungeon = dungeon_gen(abilities, dungeon_difficulty=dungeon_difficulty,
#                       dungeon_size=dungeon_size)


while True:
    user_input = inquirer.text(
        message="What's your name:\n",
        validate=lambda text: len(text) > 0,
        invalid_message="name cannot be empty.",).execute()
    greetMassage = "Hello Brave "
    name = user_input
    if name != "":
        if name.lower() == "quit" or name.lower() == "exit":
            quit()
        _player = fetch_player(name=name)
        if _player:
            logger.add_log(f"welcome back Brave {name}")
            player = _player
            json_dungeon = fetch_dungeon(player)
            if json_dungeon:
                dungeon = load_save_or_new_game()
                break
            else:
                dungeon = create_new_dungeon()
                break
        else:
            dungeon = dungeon_gen(
                abilities, dungeon_difficulty=dungeon_difficulty,
                dungeon_size=dungeon_size)
            logger.add_log(f"welcome {name}")
            player_abilities = {}
            player_abilities["fast attack"] = abilities["fast attack"]
            player_abilities["flame"] = abilities["flame"]
            player_abilities["zen"] = abilities["zen"]
            player_abilities["lockpicking"] = abilities["lockpicking"]
            armor = armor_gen(base_power_ratio=3, rarity="common")
            insert_item(armor)
            weapon = weapon_gen(base_power_ratio=3, rarity="common")
            insert_item(weapon)
            player = character_gen(character_type="player", _name=name,
                                   abilities=player_abilities, _position=[0, 0], armor=armor, weapon=weapon)
            insert_player(player)
            break

logger.add_log(player.inspect()["Log"])
log_room_desc()
merlin_Shop = shop_gen(shop_type="Merlin", abilities=abilities)
while True:
    user_input = inquirer.select(
        message="Select an action:",
        choices=["Go to", "Abilities", "Wait", "Description",
                 "Inspect", "Inventory", "Merlin Shop", "Quit"],
        default=None,
    ).execute()
    command_checker(user_input)
