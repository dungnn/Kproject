from kutil import *
from kplugins import *

class KAbstractProject:
    def __init__(self, configs):
        self.configs = configs

    def gen(self):        
        print "Preparing"
        self.prepare()
        print "Generating configure.ac"
        self.gen_configure_ac()
        print "Generating Makefile.am"
        self.gen_makefile_am()
        print "Generating others"
        self.gen_others()
        print "Done"

    def prepare(self):
        configs = self.configs
        plugin_factory = KPluginFactory()
        plugin_name_list = split(configs['plugin']['plugin'])
        self.plugins = []
        for plugin_name in plugin_name_list:
            plugin = plugin_factory.get_plugin(plugin_name, configs)
            self.plugins.append(plugin)
            plugin.hook_prepare()

        self.pkg_config_libs = split(configs['library']['libs'])
        self.extra_cppflags = split(configs['library']['extra_cppflags'])
        self.extra_include_dirs = split(configs['library']['extra_include_dirs'])
        self.extra_libs = split(configs['library']['extra_libs'])
        self.source_dirs = split(configs['src']['source_dirs'])
        self.ignore_source_dirs = split(configs['src']['ignore_source_dirs'])
        self.extra_dist = split(configs['src']['extra_dist'])

    def gen_configure_ac(self):
        pass

    def gen_makefile_am(self):
        pass

    def gen_others(self):
        pass


