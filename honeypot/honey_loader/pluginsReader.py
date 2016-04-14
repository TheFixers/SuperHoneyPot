import sys
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
 returns plugin in first plines_to_line_plus_port(osition followed by ports to be used by plugin
"""
def lines_to_line_plus_port(lines):
	temp = []
	for line in lines:
		temp.append(line.split())
	return temp

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
					print 'error: attempted to open port:' + port + ' twice. This is not allowed.'
			temp.append(array[:])
			del array[:]
		else:
			print 'error: attempted to have multiple lines of plugin: ' + line[0] + '. This is not allowed.'

	return temp


if __name__ == '__main__':
   	print lineReader()