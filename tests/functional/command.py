import shlex
import subprocess


def do(command, stdin=None):
    p = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE)
    if stdin:
        p.stdin.write(stdin)
    p.communicate()
