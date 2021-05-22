from InquirerPy.utils import color_print
from InquirerPy import inquirer


class Logger:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.logBook = []
            # Put any initialization here.
        return cls._instance

    def add_log(self, log, command=""):
        if type(log) == list:
            self.instance().logBook.append(
                f"{command}:\n{log}" if command != "" else log)
            if command != "":
                print(f"{command}:\n")
            color_print(log)
        else:
            self.instance().logBook.append(
                f"{command}:\n{log}" if command != "" else log)
            print(self.instance().logBook[-1])
