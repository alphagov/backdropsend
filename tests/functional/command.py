from collections import namedtuple
import shlex
import subprocess


Command = namedtuple("Command", ["exit_status"])


def do(command, stdin=None):
    if stdin:
        p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE)
        p.stdin.write(stdin)
    else:
        p = subprocess.Popen(shlex.split(command))
    p.communicate()

    return Command(exit_status=p.returncode)
