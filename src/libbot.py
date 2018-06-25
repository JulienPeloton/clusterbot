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
import os
import time
import requests
import numpy as np

class ClusterBot():
    """ Run services to monitor a cluster """
    def __init__(self, webhook_url, test=False):
        """
        ClusterBot instance. Currently checks: connection to executors, YARN,
        Spark, and HDFS. The summary is formatted at the JSON format and sent
        to the `webhook_url`. You can retrieve the data using a Slack or
        mattermost channel.

        Parameters
        -----------
        webhook_url : string
            the URL to which cluster information will be sent.
        test : Boolean, optional
            If True, run the bot in test mode: no commands are launched, and
            data is read from local logs.

        """
        self.webhook_url = webhook_url
        self.test = test
        if self.test:
            print("+-- RUNNING IN TEST MODE --+")

        ## Current date
        self.date = time.ctime()

        ## Header of the message to be sent
        self.msg = "Cluster report ({})\n--------------------\n".format(
            self.date)

    def run_all(self):
        """
        """
        self.msg += self.check_yarn()

        if "red_circle" in self.msg:
            self.username = "Problem(s) happened!"
        else:
            self.username = "Cluster alright!"

    def check_yarn(self, nslave_expected=9, logtest="data/yarn_test_OK.txt"):
        """
        List all nodes managed by YARN, and look at the status. A node is said
        OK if its status is RUNNING. All other keywords will be considered as
        a failure (LOST, ...).

        Parameters
        ----------
        nslave_expected : Int
            Number of slaves (executors) registered in YARN.

        Returns
        ----------
        msg : String
            Message to be sent to Slack. Contains cirle mark describing the
            status and number of slaves up.

        Examples
        ----------
        >>> bot = ClusterBot("", test=True)
        +-- RUNNING IN TEST MODE --+

        >>> msg = bot.check_yarn(logtest="data/yarn_test_OK.txt")
        >>> print(msg)
        :white_check_mark: YARN (9/9 slaves up)
        <BLANKLINE>

        >>> msg = bot.check_yarn(logtest="data/yarn_test_FAIL.txt")
        >>> print(msg)
        :red_circle: YARN (8/9 slaves up)
        <BLANKLINE>
        """
        if self.test:
            cmd = None
            logname = logtest
        else:
            cmd = "yarn node -list -all"
            logname = "yarn_{}".format(self.date.replace(" ", "_"))

        yarn_log = return_log(cmd, logname)

        nslave = len([line for line in yarn_log if "RUNNING" in line])

        if (nslave == nslave_expected):
            msg = ":white_check_mark: YARN ({}/{} slaves up)\n".format(
                nslave, nslave_expected)
        else:
            msg = ":red_circle: YARN ({}/{} slaves up)\n".format(
                nslave, nslave_expected)

        return msg

    def check_spark(self):
        """
        """
        pass

    def check_hdfs(self):
        """
        """
        pass

    def send_data(self):
        """
        Send the  to a server. The output is JSON formatted.
        The failure or success of the run will be displayed in the username.
        In addition, all commands run will be summarized with individual
        results (success/failure).

        In test mode, no data is sent, and the message is
        printed out on the screen.

        """
        if self.test:
            print(self.msg)
        else:
            requests.post(
                self.webhook_url,
                json={"text": self.msg, "username": self.username},
                headers={'Content-Type': 'application/json'})


def return_log(cmd, logname, clean_log=True):
    """
    Run a command `cmd`, redirect the output in `logname`, and return formatted
    log. The data is written line-by-line. By default, the log is
    removed from disk after the operation.

    Parameters
    ----------
    cmd : String
        Command to launch on the cluster.
    logname : String
        Name of the (temporary) log to be written on the disk.
    clean_log : Boolean, optional
        If True, remove the log after the operation. Default is True.

    Returns
    ----------
    data : List of String
        The log produced by the command, line-by-line.

    Examples
    ----------
    Clean the log after
    >>> log = return_log("echo toto", "myLog.txt", True)
    >>> assert "toto" in log[0]

    Keep the log on disk
    >>> log = return_log("echo toto", "myLog.txt", False)

    """
    ## Launch the command and redirect the log
    if cmd is not None:
        os.system(cmd + " > {}".format(logname))
        test = False
    else:
        test = True

    ## Load the log in a list (line-by-line)
    data = []
    with open(logname, "r") as f:
        for line in f:
            data.append(line)

    ## Remove log from the disk
    if clean_log and not test:
        os.system("rm {}".format(logname))

    ## Return the data
    return data


if __name__ == "__main__":
    ## Run the test suite
    import doctest
    if np.__version__ >= "1.14.0":
        np.set_printoptions(legacy="1.13")
    doctest.testmod()
