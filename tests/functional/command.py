from collections import namedtuple
import shlex
import subprocess


Command = namedtuple("Command", ["exit_status", "stderr", "stdout"])


def do(command, stdin=None):
    if stdin:
        p = subprocess.Popen(shlex.split(command),
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        p.stdin.write(stdin)
    else:
        p = subprocess.Popen(shlex.split(command),
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)

    stdout, stderr = p.communicate()

    return Command(exit_status=p.returncode, stderr=stderr, stdout=stdout)
