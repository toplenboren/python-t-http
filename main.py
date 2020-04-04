"""
Main guy, gets Arguments and returns Result either printed on console or to the output arg
"""

import argparse
from http_client.client import HttpClient
from help import ARGUMENTS_PARSING, HELP_MISC


def setup_arg_parser():
    """
    Sets up arguments parser
    """
    parser = argparse.ArgumentParser(description=HELP_MISC["description"])

    class store_dict_key_pair(argparse.Action):
        """
        Gives Argparser an ability to store POST attrs
        """

        def __call__(self, parser, namespace, values, option_string=None):
            my_dict = {}
            for kv in values.split(","):
                k, v = kv.split("=")
                my_dict[k] = v
            setattr(namespace, self.dest, my_dict)

    parser.add_argument("address", type=str, help=ARGUMENTS_PARSING["address"])
    parser.add_argument(
        "-output", metavar="-o", type=str, help=ARGUMENTS_PARSING["output"]
    )
    parser.add_argument(
        "-method", metavar="-m", type=str, help=ARGUMENTS_PARSING["method"]
    )
    parser.add_argument(
        "-timeout", metavar="-t", type=int, help=ARGUMENTS_PARSING["timeout"]
    )
    parser.add_argument(
        "-body",
        metavar="-b",
        action=store_dict_key_pair,
        help=ARGUMENTS_PARSING["body"],
    )
    parser.add_argument(
        "-headers",
        metavar="-he",
        action=store_dict_key_pair,
        help=ARGUMENTS_PARSING["header"],
    )
    return parser


def main():
    parser = setup_arg_parser()
    args = parser.parse_args()
    print(vars(args))
    client = HttpClient(vars(args))
    client.fire()


if __name__ == "__main__":
    main()
