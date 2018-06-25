# clusterbot: bring cluster monitoring into channels
# Copyright (C) 2018  Julien Peloton
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import argparse
from libbot import ClusterBot

def addargs(parser):
    """ Parse command line arguments """
    parser.add_argument(
        '--services',
        dest='services',
        help="""
            Services to monitor, space separated. Example to monitor YARN and
            Spark use `--service yarn spark`.
        """,
        nargs='+',
        required=True)

    parser.add_argument(
        '--webhook_url',
        dest='webhook_url',
        help="""
            Unique URL to which you will send the JSON payload.
            This url must be associated to an existing
            channel (Slack, Mattermost, ...)
        """,
        required=True)

    parser.add_argument(
        '--test_mode',
        dest='test_mode',
        help="""
            Run the bot in test mode, that is logs are read from local sources,
            and no commands are launched (useful for CI tests for example).
        """,
        action='store_true')

def grabargs(args_param=None):
    """ Parse command line arguments """
    parser = argparse.ArgumentParser(description='TBD')
    addargs(parser)
    args = parser.parse_args(args_param)
    return args


if __name__ == "__main__":
    args_param = None
    args = grabargs(args_param)

    cb = ClusterBot(args.webhook_url, args.services, args.test_mode)
    cb.run_all()
    cb.send_data()
