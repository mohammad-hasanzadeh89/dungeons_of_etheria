import random


class Door:
    """
        difficulty can be one of these numbers 2,3,4,5.
    """

    def __init__(self, _from, _to, name="Wooden Door", locked=False, difficulty=2):
        self.name = name
        self.locked = locked
        self.difficulty = difficulty
        self._from = _from
        self._to = _to

    def __str__(self):
        return f"{self.name}, open from room {self._from} to room {self._to}"

    def to_dict(self):
        _dict = {
            "name": self.name,
            "locked": self.locked,
            "difficulty": self.difficulty,
            "_from": self._from,
            "_to": self._to
        }
        return _dict


class Room:

    def __init__(self, characters=[], position=(0, 0), description="", difficulty=0):
        self.position = position
        self.description = description
        self.characters = characters
        self.difficulty = difficulty

    def __str__(self):
        return f"{self.position}\n" + self.description

    def to_dict(self):
        _characters = []
        for character in self.characters:
            _characters.append(character.to_dict())

        _dict = {
            "position": self.position,
            "description": self.description,
            "difficulty": self.difficulty,
        }
        _dict["characters"] = _characters
        return _dict


class Dungeon:

    def __init__(self, difficulty=0, dungeon_size=2):
        self.dungeon_size = dungeon_size
        self.difficulty = difficulty
        self.boss = None
        self.rooms = {}
        self.doors = {}

    def create_dungeon(self):
        self.create_rooms()
        self.create_doors()
        return self

    def create_doors(self):
        for x in range(0, self.dungeon_size):
            for y in range(0, self.dungeon_size):
                rand = 0.0
                is_locked = False
                if x < self.dungeon_size-1:
                    rand = random.random()
                    is_locked = rand > 0.6
                    difficulty = random.randint(2, 3)
                    self.add_door(Door(_from=(x, y), _to=(x+1, y), locked=is_locked,
                                       difficulty=difficulty))
                    if random.random() > 0.9 and y < self.dungeon_size-1:
                        difficulty = random.randint(4, 5)
                    self.add_door(Door(_from=(x, y), _to=(x+1, y), locked=is_locked,
                                       difficulty=difficulty))
                else:
                    if y < self.dungeon_size-1:
                        rand = random.random()
                        is_locked = rand > 0.4
                        self.add_door(Door(_from=(x, y), _to=(0, y+1), locked=is_locked,
                                           difficulty=difficulty))

    def create_rooms(self):
        for x in range(0, self.dungeon_size):
            for y in range(0, self.dungeon_size):
                room = Room(characters=[], position=[x, y],
                            difficulty=random.randint(1, self.difficulty))
                if x == self.dungeon_size - 1 and y == self.dungeon_size - 1:
                    room.difficulty = self.difficulty
                self.rooms[(x, y)] = room

    def add_door(self, door):
        self.doors[(door._from, door._to)] = door

    def to_dict(self):
        _doors = {}
        for key in self.doors:
            _doors[str(key)] = self.doors[key].to_dict()
        _rooms = {}
        for key in self.rooms:
            _rooms[str(key)] = self.rooms[key].to_dict()
        _dict = {
            "dungeon_size": self.dungeon_size,
            "difficulty": self.difficulty,
            "boss": self.boss.to_dict()
        }
        _dict["doors"] = _doors
        _dict["rooms"] = _rooms
        return _dict
