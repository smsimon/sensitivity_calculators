#!/usr/local/bin/python

import os

targets = ('log_', 'sensitivity.txt', 'opticalpower.txt', '~', '.pyc')

for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if any(target in file.lower() for target in targets):
            print "Deleting file: " + file
            os.remove(os.path.join(root, file))
