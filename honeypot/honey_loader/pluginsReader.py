import sys
import re
import os


def lineReader():
	path = os.path.dirname(os.path.realpath(__file__)).replace("honey_loader", "data_files")
	text_file = open(path + os.path.sep + "plugins.txt", "r")
	lines = lines_to_line_plus_port(removeExtraLines(re.split ('\n', text_file.read())))
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
 returns plugin in first position followed by ports to be used by plugin
"""
def lines_to_line_plus_port(lines):
	temp = []
	for line in lines:
		temp.append(line.split())
	return temp
if __name__ == '__main__':
    lineReader()
