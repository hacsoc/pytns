"""Abstract base class example for Python 3.0 and later (works with 2.6 if you
use the old metaclass and print syntax)
"""

# http://www.python.org/dev/peps/pep-3119/

from abc import ABCMeta, abstractmethod

from class_decorators import command, commands

class Command(metaclass=ABCMeta):

    @abstractmethod
    def fight(self):
        pass


@command('fight')
class FightCommand(Command):

    def fight2(self):
        print("I AM ALSO FIGHTING")


if __name__ == '__main__':
    commands['fight'].fight()
