import os
from pprint import pprint
import requests
import argparse
import sys


def parse_args(args, input):
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="URL of the target bucket",
                        required=True)
    parser.add_argument('--token', help="Bearer token for the target bucket",
                        required=True)
    parser.add_argument('file', help="File containing JSON to send", nargs='?',
                        type=argparse.FileType('r'),
                        default=input)
    arguments = parser.parse_args(args)

    if arguments.file.isatty():
        parser.error("No input provided")

    return arguments


def send(args, input=None):
    arguments = parse_args(args, input)

    data = arguments.file.read()

    response = requests.post(url=arguments.url, data=data, headers={
        "Authorization": "Bearer " + arguments.token,
        "Content-type": "application/json"
    })

    response.raise_for_status()


if __name__ == "__main__":
    send(sys.argv[1:], input=sys.stdin)