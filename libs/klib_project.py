import os
import re
import shutil
from kabstract_project import *
from kutil import *

class KLibProject(KAbstractProject):
    def prepare(self):
        self.configs['pkgconfig'] = {'extra_libs': '', 'extra_cflags': ''}
        KAbstractProject.prepare(self)
        self.ignore_header_files = re.split('\s+', self.configs['src']['ignore_header_files'])
        if not os.path.exists('m4'):
            os.mkdir('m4')
        shutil.copy(os.environ['KPROJECT_HOME'] + '/data/autogen.lib.sh', 'autogen.sh')

    def gen_configure_ac(self):
        configs = self.configs
        f = open('configure.ac', 'w')
        f.write('#Generate by kproject\n\n')

        #Name, version
        f.write('AC_INIT([%s], [%s])\n' % (configs['project']['name'], configs['project']['version']))
        f.write('AC_PREREQ([2.59])\n')
        f.write('AM_INIT_AUTOMAKE([1.08 no-define foreign])\n\n')

        #Prog compiler, install, libtool
        if configs['project']['compiler'] != 2:
            f.write('AC_PROG_CC\n')
        if configs['project']['compiler'] != 1:
            f.write('AC_PROG_CXX\n')
        f.write('AC_PROG_INSTALL\n')
        f.write('AC_PROG_LIBTOOL\n')
        f.write('AC_SUBST([VERSION], [%s])\n' % configs['project']['version'])
        f.write('AC_CONFIG_MACRO_DIR([m4])\n\n')

        #pkg-config
        for pkg_name in self.pkg_config_libs:
            lib_name = pkg_name.replace('-', '_')
            f.write('PKG_CHECK_MODULES([%s], [%s],,)\n' % (lib_name, pkg_name))
        f.write('\n')

        #Plugin
        for plugin in self.plugins:
            output = plugin.hook_configure_ac()
            if output:
                f.write(output)
                f.write('\n')

        #Debug
        if configs['misc']['debug'] == 1:
            fdebug = open(os.environ['KPROJECT_HOME'] + '/data/debug.ac')
            f.write(fdebug.read())
            fdebug.close()
        f.write('\n')

        #Finish
        f.write('AC_CONFIG_FILES([Makefile %s.pc])\n' % configs['project']['name'])
        f.write('AC_OUTPUT\n')

        f.close()


    def gen_makefile_am(self):
        configs = self.configs
        f = open('Makefile.am', 'w')

        #Begin
        f.write('AUTOMAKE_OPTIONS = subdir-objects\n')
        f.write('ACLOCAL_AMFLAGS = ${ACLOCAL_FLAGS} -I m4\n')
        f.write('pkgconfigdir = $(libdir)/pkgconfig\n')
        f.write('pkgconfig_DATA = %s.pc\n\n' % configs['project']['name'])

        #Project
        f.write('VERSION_INFO = %s\n' % configs['project']['lib_version'])
        f.write('lib_LTLIBRARIES = lib%s.la\n' % configs['project']['name'])
        f.write('lib%s_la_LDFLAGS = -version-info ${VERSION_INFO}\n' % configs['project']['name'])
        
        #Cppflags
        f.write('lib%s_la_CPPFLAGS =' % configs['project']['name'])
        for lib in self.pkg_config_libs:
            f.write(' $(%s_CFLAGS)' % lib.replace('-', '_'))

        for cppflags in self.extra_cppflags:
            f.write(' %s' % cppflags)

        for extra_include_dir in self.extra_include_dirs:
            if not start_with(extra_include_dir, '/'):
                f.write(' -I$(srcdir)/%s' % extra_include_dir)
            else:
                f.write(' -I%s' % extra_include_dir)
        f.write('\n')

        #LIBADD
        f.write('lib%s_la_LIBADD =' % configs['project']['name'])
        for lib in self.pkg_config_libs:
            f.write(' $(%s_LIBS)' % lib.replace('-', '_'))

        for lib in self.extra_libs:
            f.write(' %s' % lib)
        f.write('\n')

        #source
        f.write('lib%s_la_SOURCES = ' % configs['project']['name'])
        sources = []
        for source_dir in self.source_dirs:
            sources += scan_recursive(source_dir, self.ignore_source_dirs)
        f.write(print_source(sources))

        #include dir
        f.write('library_includedir = $(includedir)/%s\n' % configs['project']['name'])
        sources = []
        for source_dir in self.source_dirs:
            sources += scan_recursive(source_dir, self.ignore_source_dirs + self.ignore_header_files, 0)
        f.write('library_include_HEADERS =')
        includes = []
        for source_file in sources:
            bname = os.path.basename(source_file)
            includes.append('includes/' + bname)
        main_include = 'includes/%s.h' % configs['project']['name']
        if not main_include in includes:
            includes.append(main_include)
        f.write(print_source(includes))

        #Extra dist
        f.write('dist_noinst_SCRIPTS = autogen.sh ')
        for extra_dist in self.extra_dist:
            f.write(' %s' % extra_dist)
        f.write('\n\n')

        #Clean
        f.write('clean-local:\n\t$(RM) %s.pc\n' % configs['project']['name'])

        #Plugin
        for plugin in self.plugins:
            output = plugin.hook_makefile_am()
            if output:
                f.write(output)
                f.write('\n')

        f.close()

    def gen_others(self):
        configs = self.configs

        #Includes
        if not os.path.exists('includes'):
            os.mkdir('includes')
        os.system('rm -rf includes/*')
        sources = []
        for source_dir in self.source_dirs:
            sources += scan_recursive(source_dir, self.ignore_source_dirs + self.ignore_header_files, 0)
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
            
        #pkg-config
        f = open('%s.pc.in' % configs['project']['name'], 'w')
        f.write('prefix=@prefix@\nexec_prefix=@exec_prefix@\nlibdir=@libdir@\nincludedir=@includedir@\n\n')
        f.write('Name: %s\n' % configs['project']['name'])
        f.write('Description: %s\n' % configs['project']['description'])
        f.write('Version: @VERSION@\n')
        f.write('Requires:')
        for lib in self.pkg_config_libs:
            f.write(' %s' % lib)
        f.write('\n')
        f.write('Libs: %s -L${libdir} -l%s\n' % (configs['pkgconfig']['extra_libs'], configs['project']['name']))
        f.write('Cflags: %s -I${includedir}\n' % configs['pkgconfig']['extra_cflags'])
        f.close()

        #Plugin
        for plugin in self.plugins:
            plugin.hook_others()

