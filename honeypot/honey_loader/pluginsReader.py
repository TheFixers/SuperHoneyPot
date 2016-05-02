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
	return removeExtraLines(re.split ('\n', text_file.read()))

"""
 removes lines that start with # and blank lines
"""
def removeExtraLines(lines):
	temp = []
	for line in lines:
		if line != '' and line[:1] != '#' and not line.isspace():
			temp.append(line)
	return lines_to_line_plus_port(temp)

"""
 temp example [['http_reader', '80', '1111'], ...]
 arr  example {'http_reader' : ['80', '1111'], ...}
 returns plugin in first plines_to_line_plus_port(osition followed by ports to be used by plugin
"""
def lines_to_line_plus_port(lines):
	temp = []
	arr = {}
	for line in lines:
		temp.append(line.split())
	
	for line in temp:
		key = line.pop(0);
		if key in arr:
			arr[key] = set(arr[key] + line)
		else:
			arr[key] = line
	return dashes(arr)

"""
  Checks to see if there are dashes in between port numbers, and then creates a range of ports to open
  lines begining  example {'http_reader' : ['80-82', '1111'], ...}
  lines ending    example {'http_reader' : ['80', '81', '82', '1111'], ...}

"""
def dashes(lines):
	lineArray = []
	for key in lines:
		for port in lines[key]:
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
		lines[key] = lineArray[:]
		del lineArray[:]
	return repeat_check(lines)

"""
  Checks the list again for repeats of plugin names or duplicate port numbers.
"""
def repeat_check(lines):
	ports = []
	useablePorts = []
	for key in lines:
		for port in lines[key]:
			if not port in ports:
				ports.append(port)
				useablePorts.append(port)
			else:
				print 'Error: attempted to open port:' + port + ' twice. This is not allowed. Only running first mention.'
		lines[key] = useablePorts[:]
		del useablePorts[:]	
	return lines


if __name__ == '__main__':
	print lineReader()