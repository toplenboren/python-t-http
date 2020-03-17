import argparse
from client import http_client
from help import ARGUMENTS_PARSING, HELP_MISC


def setup_arg_parser():
    parser = argparse.ArgumentParser(description=HELP_MISC['description'])
    parser.add_argument('address',
                        type=str,
                        nargs='+',
                        help=ARGUMENTS_PARSING['address']
                        )
    parser.add_argument('-output',
                        metavar='-o',
                        type=str,
                        help=ARGUMENTS_PARSING['output']
                        )
    parser.add_argument('-method',
                        metavar='-m',
                        type=str,
                        help=ARGUMENTS_PARSING['method']
                        )
    parser.add_argument('-timeout',
                        metavar='-t',
                        type=int,
                        help=ARGUMENTS_PARSING['timeout']
                        )
    parser.add_argument('-body',
                        metavar='-b',
                        type=dict,
                        help=ARGUMENTS_PARSING['body']
                        )
    parser.add_argument('-header',
                        metavar='-h',
                        type=dict,
                        help=ARGUMENTS_PARSING['header']
                        )
    return parser


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    client = http_client(vars(args))
    client.fire()


if __name__ == '__main__':
    main()
