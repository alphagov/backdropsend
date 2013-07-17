import sys
import requests
import time

from backdrop.argumentsparser import parse_args
from backdrop.status import *

def log(message):
    print >> sys.stderr, message

def post(data, arguments):
    try:
        response = requests.post(url=arguments.url, data=data, headers={
            "Authorization": "Bearer " + arguments.token,
            "Content-type": "application/json"
        }, timeout=arguments.timeout)

        if response.status_code == 403:
            return UNAUTHORIZED

        if response.status_code < 200 or response.status_code >= 300:
            return HTTP_ERROR.with_details({ 'status': response.status_code, 'message': response.text })
        
        return OK
    except (requests.ConnectionError, requests.exceptions.Timeout) as e:
        return CONNECTION_ERROR

def post_attempts(arguments):
    data = arguments.file.read()

    for attempt in range(1, arguments.attempts + 1):
        last_attempt = attempt == arguments.attempts
        
        yield post(data, arguments), last_attempt

        log("Retrying...")
        time.sleep(arguments.sleep)


def send(args, input=None):
    arguments = parse_args(args, input)

    for post_status, is_last_attempt in post_attempts(arguments):
        log(post_status.description())

        if post_status.is_ok() or is_last_attempt:
            break

    exit(post_status.code)
