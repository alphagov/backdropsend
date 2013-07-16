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

def status(message, code):
  return { 'code': code, 'message': message, 'details': {} }

OK = status("", 0)
UNAUTHORIZED = status("Unable to send to backdrop. "
                "Unauthorised: check your access token.", 4)
HTTP_ERROR = status("Unable to send to backdrop. Server responded with {status}. "
              "Error: {message}.", 8)
CONNECTION_ERROR = status("Unable to send to backdrop. Connection error.", 16)

def log(message):
    print >> sys.stderr, message

def handle_response(response):
    if response.status_code == 403:
        return UNAUTHORIZED

    if response.status_code < 200 or response.status_code >= 300:
        HTTP_ERROR['details'] = { 'status': response.status_code, 'message': response.text }
        return HTTP_ERROR
    
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

def send(args, input=None):
    arguments = parse_args(args, input)

    data = arguments.file.read()
    attempts = arguments.attempts

    if arguments.failfast:
        attempts = 1

    for i in range(attempts):
        last_retry = i == (attempts - 1)
        
        status = post(data, arguments)

        log(status['message'].format(**status['details']))

        if status['code'] == 0 or last_retry:
            break

        log("Retrying...")
        time.sleep(arguments.sleep)

    exit(status['code'])
