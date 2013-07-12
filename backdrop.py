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


UNAUTHORIZED = ("Unable to send to backdrop. Unauthorised: check your access token.", 4)
HTTP_ERROR = ("Unable to send to backdrop. Server responded with {status}.", 8)
CONNECTION_ERROR = ("Unable to send to backdrop. Connection error.", 16)

def fail(error, **kwargs):
    print >> sys.stderr, error[0].format(**kwargs)
    exit(error[1])


def send(args, input=None):
    arguments = parse_args(args, input)

    data = arguments.file.read()

    try:
        response = requests.post(url=arguments.url, data=data, headers={
            "Authorization": "Bearer " + arguments.token,
            "Content-type": "application/json"
        })

        if response.status_code == 403:
            fail(UNAUTHORIZED)

        if response.status_code < 200 or response.status_code >= 300:
            fail(HTTP_ERROR, status=response.status_code)
    except requests.ConnectionError as e:
        fail(CONNECTION_ERROR)



if __name__ == "__main__":
    send(sys.argv[1:], input=sys.stdin)
