#!/bin/bash
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

## Script to measure the coverage of the test suite (via doctest).
## Launch it using ./coverage
## and open the html files under the folder htmlcov/
coverage run src/libbot.py
coverage report src/libbot.py
coverage html src/libbot.py
