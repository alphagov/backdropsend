import argparse
import sys

import requests


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

    try:
        response = requests.post(url=arguments.url, data=data, headers={
            "Authorization": "Bearer " + arguments.token,
            "Content-type": "application/json"
        })

        if response.status_code < 200 or response.status_code >= 300:
            print >> sys.stderr, "Unable to send to backdrop. Server responded with %s" %  response.status_code
            exit(1)
    except requests.ConnectionError as e:
        print >> sys.stderr, "Unable to send to backdrop. Connection error."
        exit(1)



if __name__ == "__main__":
    send(sys.argv[1:], input=sys.stdin)
