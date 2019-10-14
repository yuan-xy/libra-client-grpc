import abc
import sys
import os
import traceback
from libra.cli.color import print_color


class Command(metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def get_aliases(self):
        pass

    def get_params_help(self):
        return ""

    @abc.abstractmethod
    def get_description(self):
        pass

    @abc.abstractmethod
    def execute(self, client, params):
        pass

    def subcommand_execute(self, parent_command_name, commands, client, params):
        if len(params) == 0:
            self.print_subcommand_help(parent_command_name, commands)
            return
        commands_map = {}
        for i, cmd in enumerate(commands):
            for alias in cmd.get_aliases():
                if commands_map.__contains__(alias):
                    raise AssertionError(f"Duplicate alias {alias}")
                commands_map[alias] = i
        idx = commands_map.get(params[0])
        if idx is not None:
            commands[idx].execute(client, params)
        else:
            self.print_subcommand_help(parent_command_name, commands)

    def print_subcommand_help(self, parent_command, commands):
        print(f"usage: {parent_command} <arg>\n\nUse the following args for this command:\n")
        if "get_notice" in dir(self):
            print_color("\t" + self.get_notice(), bcolors.WARNING)
            print("")
        print_commands(commands)


def get_commands_alias(commands):
    alias_to_cmd = {}
    for command in commands:
        for alias in command.get_aliases():
            alias_to_cmd[alias] = command
    return (commands, alias_to_cmd)


def report_error(msg, err, verbose):
    print(f"[ERROR] {msg}: {err}")
    if verbose:
        traceback.print_exc()

def parse_cmd(cmd_str: str):
    return cmd_str.split()

def parse_bool(para_str):
    para = para_str.lower()
    if para == "true" or para == "t":
        return True
    elif para == "false" or para == "f":
        return False
    else:
        raise IOError(f"Unknown support bool str: {para_str}")


def print_commands(commands):
    for cmd in commands:
        print_color(" | ".join(cmd.get_aliases()), bcolors.OKGREEN, end='')
        print_color(" " + cmd.get_params_help(), bcolors.OKBLUE)
        print("\t" + cmd.get_description())
        if "get_notice" in dir(cmd):
            print_color("\t" + cmd.get_notice(), bcolors.WARNING)

def blocking_cmd(cmd: str) -> bool:
    return cmd.endswith('b')


def debug_format_cmd(cmd: str) -> bool:
    return cmd.endswith('?')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
