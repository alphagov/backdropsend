import argparse
import sys
import select

import requests


def no_piped_input(arguments):
    inputs_ready, _, _ = select.select([arguments.file], [], [], 0)
    return not bool(inputs_ready)

def parse_args(args, input):
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="URL of the target bucket",
                        required=True)
    parser.add_argument('--token', help="Bearer token for the target bucket",
                        required=True)
    parser.add_argument('--timeout', help="Request timeout. Default: 5 seconds",
                        required=False, default=5, type=float)
    parser.add_argument('--attempts', help="Number of times to attempt sending data. Default: 3",
                        required=False, default=3, type=int)
    parser.add_argument('file', help="File containing JSON to send", nargs='?',
                        type=argparse.FileType('r'),
                        default=input)
    arguments = parser.parse_args(args)

    if no_piped_input(arguments):
        parser.error("No input provided")

    return arguments


UNAUTHORIZED = ("Unable to send to backdrop. "
                "Unauthorised: check your access token.", 4)
HTTP_ERROR = ("Unable to send to backdrop. Server responded with {status}.", 8)
CONNECTION_ERROR = ("Unable to send to backdrop. Connection error.", 16)


def fail(error, last_retry, **kwargs):
    print >> sys.stderr, error[0].format(**kwargs)
    if last_retry:        
        exit(error[1])
    else:
        print >> sys.stderr, "Retrying..."

def ok():
    exit(0)        

def send(args, input=None):
    arguments = parse_args(args, input)

    data = arguments.file.read()
    attempts = arguments.attempts

    for i in range(attempts):
        last_retry = i == (attempts - 1)
        try:
            response = requests.post(url=arguments.url, data=data, headers={
                "Authorization": "Bearer " + arguments.token,
                "Content-type": "application/json"
            }, timeout=arguments.timeout)

            if response.status_code == 403:
                fail(UNAUTHORIZED, True)

            if response.status_code < 200 or response.status_code >= 300:
                fail(HTTP_ERROR, last_retry, status=response.status_code)
            else:
                ok()
        except (requests.ConnectionError, requests.exceptions.Timeout) as e:
            fail(CONNECTION_ERROR, last_retry)
