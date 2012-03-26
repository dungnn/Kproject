#!/usr/bin/env python

import os
import sys
import shutil

def main():
    if not 'KPROJECT_HOME' in os.environ:
        print 'KPROJECT_HOME environment variable is not set.'
        sys.exit
    kproject_home = os.environ['KPROJECT_HOME']
    config_file = kproject_home + '/data/kproject.conf'
    if not os.path.isfile(config_file):
        print 'Kproject config file not found: ' + config_file
        sys.exit
    shutil.copy(config_file, 'kproject.conf')
    print 'Project init successfully.'

if __name__ == '__main__':
    main()
