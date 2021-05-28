# Auteur : ngbamedistingue@yahoo.com
# Python version 3.7
# !/usr/bin/env python3
# encoding=utf8
"""
TFTP Server Command.
"""
import sys
import os
import argparse
import tftp

TIMEOUT = 2
PORT = 6969

parser = argparse.ArgumentParser(prog='tftp-server')
parser.add_argument('-p', '--port', type=int, default=PORT)
parser.add_argument('-t', '--timeout', type=int, default=TIMEOUT)
parser.add_argument('-c', '--cwd',  type=str, default='')
parser.add_argument('--thread', action='store_true')
args = parser.parse_args()

# change current working directory
if args.cwd != '': os.chdir(args.cwd)

# run main server loop
tftp.runServer(('', args.port), args.timeout, args.thread)

# EOF