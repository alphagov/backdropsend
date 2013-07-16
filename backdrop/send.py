import argparse
import sys
import select

import requests
import time


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
    parser.add_argument('--failfast', help="Don't retry sending data",
                        required=False, default=False, action='store_true')
    parser.add_argument('--sleep', help=argparse.SUPPRESS,
                        required=False, default=3, type=int)
    parser.add_argument('file', help="File containing JSON to send", nargs='?',
                        type=argparse.FileType('r'),
                        default=input)
    arguments = parser.parse_args(args)

    if no_piped_input(arguments):
        parser.error("No input provided")

    return arguments

class Status():
    def __init__(self, message, code):
        self.code = code
        self.message = message
        self.details = {}
  
    def description(self):
        return self.message.format(**self.details)
  
    def with_details(self, details):
        self.details = details
        return self
  
    def is_ok(self):
        return self.code == 0

OK = Status("", 0)
UNAUTHORIZED = Status("Unable to send to backdrop. "
                "Unauthorised: check your access token.", 4)
HTTP_ERROR = Status("Unable to send to backdrop. Server responded with {status}. "
              "Error: {message}.", 8)
CONNECTION_ERROR = Status("Unable to send to backdrop. Connection error.", 16)

def log(message):
    print >> sys.stderr, message

def handle_response(response):
    if response.status_code == 403:
        return UNAUTHORIZED

    if response.status_code < 200 or response.status_code >= 300:
        return HTTP_ERROR.with_details({ 'status': response.status_code, 'message': response.text })
    
    return OK

def post(data, arguments):
    try:
        response = requests.post(url=arguments.url, data=data, headers={
            "Authorization": "Bearer " + arguments.token,
            "Content-type": "application/json"
        }, timeout=arguments.timeout)

        return handle_response(response)
    except (requests.ConnectionError, requests.exceptions.Timeout) as e:
        return CONNECTION_ERROR

def post_attempts(arguments):
    data = arguments.file.read()
    attempts = arguments.attempts

    if arguments.failfast:
        attempts = 1

    for i in range(attempts):
        last_attempt = i == (attempts - 1)
        
        status = post(data, arguments)

        yield status, last_attempt

        log("Retrying...")
        time.sleep(arguments.sleep)


def send(args, input=None):
    arguments = parse_args(args, input)

    for status, is_last_attempt in post_attempts(arguments):
        log(status.description())

        if status.is_ok() or is_last_attempt:
            break

    exit(status.code)
