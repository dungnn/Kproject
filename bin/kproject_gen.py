#!/usr/bin/env python

import os
import sys

if not 'KPROJECT_HOME' in os.environ:
    print 'KPROJECT_HOME environment variable is not set.'
    sys.exit

kproject_home = os.environ['KPROJECT_HOME']
sys.path.append(kproject_home + '/libs')

from kconfig import *
from kproject import *

def main():
    try:
        configs = load_configs()
        KProjectFactory().create_project(configs).gen()
    except Exception as err:
        print err
        sys.exit()

if __name__ == '__main__':
    main()
