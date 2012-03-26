import os
import re
import shutil
from kutil import *

class KAbstractPlugin:
    def __init__(self, configs):
        self.configs = configs

    def hook_prepare(self):
        pass

    def hook_configure_ac(self):
        pass

    def hook_makefile_am(self):
        pass

    def hook_others(self):
        pass

class KPluginFactory:
    def get_plugin(self, name, configs):
        if name == 'boost':
            return KBoostPlugin(configs)
        else:
            raise Exception('Plugin not found: %s' % name)

class KBoostPlugin(KAbstractPlugin):
    def hook_prepare(self):
        if not os.path.exists('m4'):
            os.mkdir('m4')
        kproject_home = os.environ['KPROJECT_HOME']
        if not os.path.isfile('m4/ax_boost_base.m4'):
            shutil.copy(kproject_home + '/data/m4/ax_boost_base.m4', 'm4/ax_boost_base.m4')
        self.configs['library']['extra_cppflags'] += ' $(BOOST_CPPFLAGS)'
        self.configs['library']['extra_libs'] += ' $(BOOST_LIBS)'
        if 'pkgconfig' in self.configs:
            self.configs['pkgconfig']['extra_libs'] += ' @BOOST_LIBS@'
            self.configs['pkgconfig']['extra_cflags'] += ' @BOOST_CPPFLAGS@'

    def hook_configure_ac(self):
        configs = self.configs
        output = 'm4_include([m4/ax_boost_base.m4])\n'
        output += 'AX_BOOST_BASE([%s])\n' % configs['plugin']['boost_version']
        output += 'if test "x$succeeded" == "xno" ; then\n'
        output += '\tAC_MSG_ERROR([no boost found])\n'
        output += 'fi\n'
        output += 'AC_SUBST([BOOST_LIBS], ["${BOOST_LDFLAGS}'
        for boost_ld in split(configs['plugin']['boost_libs']):
            output += ' -l' + boost_ld
        output += '"])\n'

        return output
