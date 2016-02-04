__author__ = 'daemoniclegend'

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from plugins import ssh_plugin
'''
path = os.getcwd().replace('UnitTest', '')
sys.path.insert(0, path)
sys.path.append('..')
'''

sshServer = ssh_plugin()