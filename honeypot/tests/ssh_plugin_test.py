__author__ = 'daemoniclegend'

import os
import sys

path = os.path.dirname(os.path.realpath(__file__)).replace("tests", "plugins")
sys.path.insert(0, path)

import ssh_plugin
'''
path = os.getcwd().replace('UnitTest', '')
sys.path.insert(0, path)
sys.path.append('..')
'''

ssh_plugin.server_plugin()