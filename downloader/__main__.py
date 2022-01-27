# Copyright (c) 2022, Ivan Koldakov.
# All rights reserved.
#
# Use as you want, modify as you want but please include the author's name.

import argparse
import sys

from downloader.maintain import Maintain


def run():
    _data = None
    _mode = 'standard'
    _usernames_nargs = '+'

    parser = argparse.ArgumentParser(description='Download user.')

    if not sys.stdin.isatty():
        _mode = 'pipe'
        _usernames_nargs = '?'
        _data = "\n".join([line.strip() for line in sys.stdin.readlines() if line.strip()])

    parser.add_argument('-q', '--quiet',
                        required=False,
                        help='No stdout',
                        action='store_true')

    parser.add_argument('usernames',
                        type=str,
                        nargs=_usernames_nargs,
                        help='Usernames to download')

    parser.add_argument('-p', '--path',
                        required=False,
                        type=str,
                        nargs=1,
                        help='Path to save files')

    parser.add_argument('-n', '--network',
                        required=False,
                        type=str,
                        nargs=1,
                        help='Network to scrap')

    args = parser.parse_args()
    dict_args = vars(args)

    dict_args.update({'data': _data})
    dict_args.update({'mode': _mode})

    maintain = Maintain(**dict_args)

    maintain.process()


if __name__ == '__main__':
    run()
