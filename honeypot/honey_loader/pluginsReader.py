#!/usr/bin/python2
"""
    This file is part of SuperHoneyPot.

    SuperHoneyPot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    SuperHoneyPot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with SuperHoneyPot.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import os


def lineReader():
	path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "data_files")
	text_file = open(path + os.path.sep + "plugins.txt", "r")
	lines = removeExtraLines(re.split ('\n', text_file.read()))
	lines = lines_to_line_plus_port(lines)
	lines = dashes(lines)
	lines = repeat_check(lines)
	return lines

"""
 removes lines that start with # and blank lines
"""
def removeExtraLines(lines):
	temp = []
	for line in lines:
		if line != '' and line[:1] != '#' and not line.isspace():
			temp.append(line)
	return temp

"""
 array example ['http_reader', '80', '1111']
 returns plugin in first lines_to_line_plus_port(position followed by ports to be used by plugin)
"""
def lines_to_line_plus_port(lines):
	temp = []
	for line in lines:
		temp.append(line.split())
	return temp

"""
  Checks to see if there are dashes in between port numbers, and then creates a range of ports to open
"""
def dashes(lines):
	temp = []
	lineArray = []
	for line in lines:
		for port in line:
			if '-' in port:
				ranges = port.split('-')
				lowerLimit = int(float(ranges[0]))
				upperLimit = int(float(ranges[1]))
				if upperLimit > lowerLimit:
					while (lowerLimit <= upperLimit):
						lineArray.append(str(lowerLimit))
						lowerLimit = lowerLimit +1
				else:
					lineArray.append(str(lowerLimit))
					lineArray.append(str(upperLimit))
			else:
				lineArray.append(port)
		temp.append(lineArray[:])
		del lineArray[:]
	return temp

"""
  Checks the list again for repeats of plugin names or duplicate port numbers.
"""
def repeat_check(lines):
	ports = []
	plugins = []
	array = []
	temp = []
	for line in lines:
		if not line[0] in plugins:
			plugins.append(line[0])
			array.append(line.pop(0))
			for port in line:
				if not port in ports:
					ports.append(port)
					array.append(port)
				else:
					print 'Error: attempted to open port:' + port + ' twice. This is not allowed. Only running first mention.'
			temp.append(array[:])
			del array[:]
		else:
			print 'Error: attempted to have multiple lines of plugin: ' + line[0] + '. This is not allowed.'

	return temp


if __name__ == '__main__':
	print lineReader()