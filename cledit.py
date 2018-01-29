#! python

import sys
import os

args = sys.argv
valid_commands = ("show", "add", "remove")
valid_params = ('s', 'id', 'lb')
valid_flags = ('s')

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
            except ValueError:
                break

        if counter == 0:
            return 0

        return last_num + 1

    except FileNotFoundError:
        return 0

def clean():
    try:
        file = open('cmd-launch-config', 'r')
        
        valid_lines = []
        last_number = -1
        for line in file:
            number = line.split(':')[0].replace(" ", "")

            is_need_fix = False
            try:
                number = int(number)
            except ValueError:
                is_need_fix = True

            valid_line = line
            if is_need_fix or number != last_number + 1:
                number = last_number + 1

                config = ""
                if len(line.split(':')) == 1:
                    config = line
                else:
                    config = line.split(':')[1]
                    
                valid_line = "{}: {}".format(number, config)
                valid_line = valid_line.replace("  ", " ")

            valid_lines.append(valid_line)
            last_number = number
        
        file.close()
        file = open('cmd-launch-config', 'w')

        for line in valid_lines:
            file.write(line)
        file.close()
    except FileNotFoundError:
        return

def remove_cmd_id(command_id):
    file = open('cmd-launch-config', 'r')
    lines_to_keep = []
    is_removal_success = False
    assoc_bin = ""

    for line in file:
        cmd = line.split(':')[1].split('|')[0].replace(" ", "")
        if cmd != command_id:
            lines_to_keep.append(line)
        else:
            assoc_bin = line.split(':')[1].split('|')[1].replace(" ", "").replace('\n', "")
            is_removal_success = True

    file.close()
    file = open('cmd-launch-config', 'w')

    for line in lines_to_keep:
        file.write(line)
    
    if is_removal_success:
        print("\nCommand \'{}\' removed successfully. Associated binary: \'{}\'\n".format(command_id, assoc_bin))
    else:
        print("\nItem with command identifier \'{}\' does not exist.\n".format(command_id))

def get_associated_launch_bin(command_id):
    file = open('cmd-launch-config', 'r')

    for line in file:
        cmd = line.split(':')[1].split('|')[0].replace(" ", "")
        if cmd == command_id:
            return line.split(':')[1].split('|')[1].replace(" ", "").replace("\n", "")
    
    return None

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

    if id in commands and launch_bin == get_associated_launch_bin(id):
        print("The command and launch binary combination already exists.")
        return

    if id in commands:

        while True:
            print("The command {} is already in use. Do you want to overwrite the current".format(id) +
                " launch binary \'{}\' with \'{}\'? (y/n)".format(get_associated_launch_bin(id), launch_bin))

            answer = str(input()).replace('\n', "").lower()

            if answer == 'n':
                print('Canceling...')
                return
            elif answer == 'y':
                remove_cmd_id(id)
                break

    for counter, launcher in enumerate(launch_bins):
        if (launch_bin == launcher):
            
            while True:
                print("The launch binary '{0}' is already being used".format(launcher) + 
                    " under the command id '{0}'.".format(commands[counter]) + 
                    " Are you sure you want to continue? (y/n)")

                answer = input()
                answer = str(answer).replace('\n', "").lower()

                if answer == 'n':
                    print('Canceling...')
                    return
                elif answer == 'y':
                    break

    file = open('cmd-launch-config', 'a')
    file.write("{}: {} | {}\n".format(next_number(), id, launch_bin))
    file.close()

    print("\nSuccessfully added \'{} | {}\'".format(id, launch_bin))

def setId():
    pass

def setLaunchBinary():
    pass

def parseArgs():
    id = ""
    launch_bin = ""
    is_command_active = False

    active_commands = {}
    active_flags = {}
    for command in valid_commands:
        active_commands[command] = False
    for flag in valid_flags:
        active_flags[flag] = False

    if len(args) <= 1:
        print("Argument list empty")
        return

    if "-" not in args[1]:
        if args[1] in valid_commands:
            active_commands[args[1]] = True
            is_command_active = True
        else:
            print("Error: {0} is not a valid argument.".format(args[1]))
            return

    for counter, arg in enumerate(args):
        if arg.startswith('-'):
            new_arg = arg.replace("-", "")
            if new_arg in valid_params:
                if new_arg == "id":
                    id = args[counter + 1]
                elif new_arg == "lb":
                    launch_bin = args[counter + 1]
                elif new_arg in valid_flags:
                    if is_command_active:
                        active_flags[new_arg] = True
                    else:
                        if new_arg == 's':
                            show()
            else:
                print("Error: -{} is not a valid argument.".format(new_arg))

    clean()

    if active_commands['add']:
        add(id, launch_bin)
        clean()
    elif active_commands['show']:
        show()
    elif active_commands['remove']:
        remove_cmd_id(id)
        clean()

    if active_flags['s']:
        show()

parseArgs()
