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

class ClusterBot():
    """ Bot which schedules a cron job to monitor a cluster """
    def __init__(self, webhook_url, cron, service):
        """
        ClusterBot instance.

        Parameters
        -----------
        webhook_url: string
            the URL to which cluster information will be sent.
        cron: string
            cron command to be scheduled.
        service: string
            Name of the service to launch

        """
        self.webhook_url = webhook_url
        self.cron = cron
        self.service = service
        self.date = time.ctime()
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

    def check_yarn(self, nslave_expected=9):
        """
        """
        logname = "yarn_{}".format(self.date.replace(" ", "_"))

        cmd = "yarn node -list -all"

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
        """
        requests.post(
            self.webhook_url,
            json={"text": self.msg, "username": self.username},
            headers={'Content-Type': 'application/json'})


def return_log(cmd, logname, remove_log=True):
    """
    """
    ## Launch the command and redirect the log
    os.system(cmd + " > {}".format(logname))

    ## Load the log in a list (line-by-line)
    data = []
    with open(logname, "r") as f:
        for line in f:
            data.append(line)

    ## Remove log from the disk
    if remove_log:
        os.system("rm {}".format(logname))

    ## Return the data
    return data
