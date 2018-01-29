import sys
import os

args = sys.argv
valid_commands = ("show", "add")
valid_flags = ('s', 'id', 'lb')

def show():
    try:
        file = open('cmd-launch-config', 'r')
        for line in file:
            print(line.replace('\n', ""))
    except FileNotFoundError:
        print("Error: no config file found")

def next_number():
    try:
        file = open('cmd-launch-config', 'r')

        last_num = 0
        counter = 0
        for line in file:
            counter += 1
            number = 0
            number_str = line.split(':')[0]
            try:
                number = int(number_str)
                last_num = number
            except TypeError:
                break

        if counter == 0:
            return 0

        return last_num + 1

    except FileNotFoundError:
        return 0

def read_config():
    valid_lines = []

    try:
        file = open('cmd-launch-config', 'r')
        for line in file:
            line_components = line.split(':')

            if len(line_components) == 1:
                continue

            configs = line_components[1].split('|')

            if len(configs) != 2:
                continue

            valid_lines.append(line.replace("\n", ""))

        file.close()
        file = open('cmd-launch-config', 'w')

        for line in valid_lines:
            file.write("{}\n".format(line))

        commands = []
        launch_bins = []
        for line in valid_lines:
            new_line = line.split(':')[1]
            new_line = str(new_line).replace(" ", "")
            new_line = str(new_line).replace("\n", "")

            commands.append(str(new_line).split('|')[0])
            launch_bins.append(str(new_line).split('|')[1])

        return commands, launch_bins
    except FileNotFoundError:
        return None

def add(id, launch_bin):
    commands = []
    launch_bins = []
    if not read_config() is None:
        commands, launch_bins = read_config()

    if id in commands:
        print("The command {} is already in use. Please pick another command id.".format(id))
        return
    for counter, launcher in enumerate(launch_bins):
        if (launch_bin == launcher):
            print("The launch binary '{0}' is already being used".format(launcher) + 
                " under the command id '{0}'.".format(commands[counter]) + 
                " Are you sure you want to continue? (y/n)")
            
            while True:
                answer = input()
                answer = str(answer).replace('\n', "").lower()
                if answer not in ('y', 'n'):
                    print("The launch binary '{0}' is already being used".format(launcher) + 
                        " under the command id '{0}'.".format(commands[counter]) + 
                        " Are you sure you want to continue? (y/n)")
                    continue
                elif answer == 'n':
                    print('Canceling...')
                    return
                elif answer == 'y':
                    break

    file = open('cmd-launch-config', 'a')
    file.write("{0}: {1} | {2}\n".format(next_number(), id, launch_bin))

def setId():
    pass

def setLaunchBinary():
    pass

def parseArgs():
    id = ""
    launch_bin = ""
    activeCommands = {'show': False, 'add': False}

    if "-" not in args[1]:
        if args[1] in valid_commands:
            if args[1] == "show":
                activeCommands['show'] = True
            elif args[1] == "add":
                activeCommands['add'] = True
        else:
            print("Error: {0} is not a valid argument.".format(args[1]))
            return

    for counter, arg in enumerate(args):
        if arg.startswith('-'):
            new_arg = arg.replace("-", "")
            if new_arg in valid_flags:
                if new_arg == "id":
                    id = args[counter + 1]
                elif new_arg == "lb":
                    launch_bin = args[counter + 1]
                elif new_arg == 's':
                    show()
            else:
                print("Error: -{} is not a valid argument.".format(new_arg))

    if activeCommands['add']:
        add(id, launch_bin)
    elif activeCommands['show']:
        show()

parseArgs()
