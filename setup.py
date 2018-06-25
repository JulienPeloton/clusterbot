#!/usr/bin/env python
# clusterbot: bring cluster monitoring inside Slack
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

"""Distutils based setup script for clusterbot.

For the easiest installation just type the command (you'll probably need
root privileges for that):

    python setup.py install

This will install the library in the default location. For instructions on
how to customize the install procedure read the output of:

    python setup.py --help install

In addition, there are some other commands:

    python setup.py clean -> will clean all trash (*.pyc and stuff)
    python setup.py test  -> will run the complete test suite
    python setup.py bench -> will run the complete benchmark suite
    python setup.py audit -> will run pyflakes checker on source code

To get a full list of avaiable commands, read the output of:

    python setup.py --help-commands
"""
from setuptools import setup

if __name__ == "__main__":
    setup(name='clusterbot',
          version='0.1.0',
          author='Julien Peloton',
          author_email='peloton@lal.in2p3.fr',
          url='https://github.com/JulienPeloton/clusterbot',
          download_url='https://github.com/JulienPeloton/clusterbot/archive/0.1.0.zip',
          install_requires=[''],
          packages=['clusterbot'],
          scripts=['clusterbot/clusterbot'],
          description='Python module sending cluster data to a Slack channel.',
          license='GPL-3.0',
          long_description='See https://github.com/JulienPeloton/clusterbot',
          keywords=['Slack', 'cluster', 'monitoring'],
          classifiers=["Programming Language :: Python :: 3"])
