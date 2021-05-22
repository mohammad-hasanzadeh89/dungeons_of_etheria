import random


class Dice:

    def __init__(self, first=None, last=None):
        if first is None:
            first = 1
        if last is None:
            last = 6
        self.first = first
        self.last = last

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, value):
        self.__first = value

    @property
    def last(self):
        return self.__last

    @last.setter
    def last(self, value):
        if value <= self.__first:
            raise ValueError(
                "the last number of dice must be greater thant the first number")
        self.__last = value

    def roll(self, difficulty=1):
        """
            roll a dice
        """
        return random.randint(self.first, self.last * difficulty)

    def __str__(self):
        return f"this dice start with {self.first} and end with {self.last}"

    def roll_multiply(self, roll_count, difficulty=1):
        """
            roll multiply dice
        """
        result = []
        for _ in range(0, roll_count):
            result.append(self.roll(difficulty))
        return (result, sum(result, 0))

    def to_dict(self):
        return {"last": self.last}


if __name__ == "__main__":
    num_of = 1
    first = 0
    last = 0
    while(True):
        num_of = input(
            "please enter number of dices you want to roll for one just press enter:")
        if(num_of == ""):
            num_of = 1
            break
        elif(num_of.isdigit()):
            num_of = int(num_of)
            break
        else:
            print("please insert a digit like 2 or 3")
    while(True):
        first = input(
            "please enter the first number of dice or just press enter:")
        if(first == ""):
            first = 1
            break
        elif(first.isdigit()):
            first = int(first)
            break
        else:
            print("please insert a digit like 1 or 2")
    while(True):
        last = input(
            "please enter the last number of dice or just press enter:")
        if(last.isdigit()):
            last = int(last)
            if last <= first:
                print(f"please enter greater number than {first}")
            else:
                break
        elif(last == ""):
            last = 6
            break
        else:
            print("please insert a digit like 1 or 2")
    __d = None
    if first == 1 and last == 6:
        __d = Dice()
    else:
        __d = Dice(first, last)

    if num_of > 1:
        print(__d.roll_multiply(num_of))
    else:
        print(__d.roll())
