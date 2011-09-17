"""Class decorator example for Python 2.6 and later."""

commands = {}


def command(command_string):
    def make_command(cls):
        commands[command_string] = cls
        return cls
    return make_command


@command('fight')
class FightCommand(object):

    def fight(self):
        print("I'M FIGHTING")


if __name__ == '__main__':
    commands['fight']().fight()
