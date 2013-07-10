import requests


def send(args, input):
    requests.post(url=args[0], data=input.read(), headers={
        "Authorization": "Bearer " + args[1],
        "Content-type": "application/json"
    })
