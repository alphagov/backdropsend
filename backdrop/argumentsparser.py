import argparse
import select

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


    if arguments.failfast:
        arguments.attempts = 1

    if no_piped_input(arguments):
        parser.error("No input provided")

    return arguments

