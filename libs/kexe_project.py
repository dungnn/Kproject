import os
import re
import shutil
from kabstract_project import *
from kutil import *

class KExeProject(KAbstractProject):

    def prepare(self):
        KAbstractProject.prepare(self)
        if not os.path.exists('autogen.sh'):
            shutil.copy(os.environ['KPROJECT_HOME'] + '/data/autogen.exe.sh', 'autogen.sh')

    def gen_configure_ac(self):
        configs = self.configs
        f = open('configure.ac', 'w')
        f.write('#Generate by kproject\n\n')

        #Name, version, silence
        f.write('AC_INIT([%s], [%s])\n' % (configs['project']['name'], configs['project']['version']))
        f.write('AC_PREREQ([2.59])\n')
        f.write('AM_INIT_AUTOMAKE([1.08 no-define foreign])\n\n')

        if (configs['project']['silent'] == 'yes'):
            f.write('AM_SILENT_RULES([yes])\n')
        else:
            f.write('AM_SILENT_RULES([no])\n')

        #Prog compiler, install
        if configs['project']['compiler'] != 2:
            f.write('AC_PROG_CC\n')
        if configs['project']['compiler'] != 1:
            f.write('AC_PROG_CXX\n')
        f.write('AC_PROG_INSTALL\n')
        f.write('AC_SUBST([VERSION], [%s])\n\n' % configs['project']['version'])

        #pkg-config
        for pkg_name in self.pkg_config_libs:
            lib_name = strip_lib(pkg_name.replace('-', '_'))
            f.write('PKG_CHECK_MODULES([%s], [%s],,)\n' % (lib_name, pkg_name))

        f.write('\n')

        #Plugin
        for plugin in self.plugins:
            output = plugin.hook_configure_ac()
            if output:
                f.write(plugin.hook_configure_ac())
                f.write('\n')

        #Debug
        #if configs['misc']['debug'] == 1:
        #    fdebug = open(os.environ['KPROJECT_HOME'] + '/data/debug.ac')
        #    f.write(fdebug.read())
        #    fdebug.close()

        #f.write('\n')

        #Finish
        f.write('AC_CONFIG_FILES([Makefile])\n')
        f.write('AC_OUTPUT\n')

        f.close()

    def gen_makefile_am(self):
        configs = self.configs
        f = open('Makefile.am', 'w')

        #Begin
        f.write('AUTOMAKE_OPTIONS = subdir-objects\n\n')
        
        #Program
        f.write('bin_PROGRAMS = %s\n' % configs['project']['name'])

        #CPPFLAGS
        f.write('%s_CPPFLAGS =' % configs['project']['name'])
        for lib in self.pkg_config_libs:
            f.write(' $(%s_CFLAGS)' % strip_lib(lib.replace('-', '_')))

        for cppflags in self.extra_cppflags:
            f.write(' %s' % cppflags)

        for extra_include_dir in self.extra_include_dirs:
            if not start_with(extra_include_dir, '/'):
                f.write(' -I$(srcdir)/%s' % extra_include_dir)
            else:
                f.write(' -I%s' % extra_include_dir)
        f.write('\n')

        #LDADD
        f.write('%s_LDADD =' % configs['project']['name'])
        for lib in self.pkg_config_libs:
            f.write(' $(%s_LIBS)' % strip_lib(lib.replace('-', '_')))
        
        for lib in self.extra_libs:
            f.write(' %s' % lib)
        f.write('\n')

        #Source
        f.write('%s_SOURCES = ' % configs['project']['name'])
        sources = []
        for source_dir in self.source_dirs:
            sources += scan_recursive(source_dir, self.ignore_source_dirs)
        f.write(print_source(sources))

        #Extra dist
        f.write('dist_noinst_SCRIPTS = autogen.sh ')
        for extra_dist in self.extra_dist:
            f.write(' %s' % extra_dist)
        f.write('\n')

        #Plugin
        for plugin in self.plugins:
            output = plugin.hook_makefile_am()
            if output:
                f.write(plugin.hook_configure_ac())
                f.write('\n')

        f.close()

    def gen_others(self):
        pass
