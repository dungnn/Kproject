from kexe_project import *
from klib_project import *

class KProjectFactory:
    def create_project(self, configs):
        if configs['project']['type'] == 'exe':
            return KExeProject(configs)
        elif configs['project']['type'] == 'lib':
            return KLibProject(configs)
        else:
            raise Exception('Project type not found')
