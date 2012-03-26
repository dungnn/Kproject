#!/usr/bin/env python

import os
import sys

if not 'KPROJECT_HOME' in os.environ:
    print 'KPROJECT_HOME environment variable is not set.'
    sys.exit

kproject_home = os.environ['KPROJECT_HOME']
sys.path.append(kproject_home + '/libs')

from kconfig import *
from kutil import *

def main():
    try:
        configs = load_configs()
        if configs['project']['type'] == 'lib':
            if not os.path.exists('includes'):
                os.mkdir('includes')
            os.system('rm -rf includes/*')
            sources = []
            for source_dir in split(configs['src']['source_dirs']):
                sources += scan_recursive(source_dir, split(configs['src']['ignore_source_dirs']) + split(configs['src']['ignore_header_files']), 0)
                for source_file in sources:
                    bname = os.path.basename(source_file)
                    writer = open('includes/' + bname, 'w')
                    reader = open(source_file)
                    for line in reader:
                        m = re.search('#include\s+"(.+)"', line)
                        if m:
                            pieces = re.split('/', m.group(1).strip())
                            line = '#include <%s/%s>\n' %  (configs['project']['name'], pieces[len(pieces) - 1])
                        writer.write(line)
                    reader.close()
                    writer.close()

            if not os.path.exists('includes/%s.h' % configs['project']['name']):
                f = open('includes/%s.h' % configs['project']['name'], 'w')
                for source_file in sources:
                    f.write('#include <%s/%s>\n' % (configs['project']['name'], os.path.basename(source_file)))
                f.close()
    except Exception as err:
        print err
        sys.exit()

if __name__ == '__main__':
    main()
