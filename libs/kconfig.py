import sys
import os
import re
import ConfigParser

def load_configs():
    configs = {'project':{}, 'src':{}, 'library':{}, 'plugin':{}, 'misc':{}}
    config_file = 'kproject.conf'
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(config_file)
    
    #Project
    project_name = config_parser.get('project', 'name')
    if not re.match('^[a-zA-Z0-9_]+$', project_name):
        raise ValueError('Project name is not approriate: %s' % project_name)
    configs['project']['name'] = project_name

    configs['project']['description'] = config_parser.get('project', 'description')

    project_type = config_parser.get('project', 'type')
    if project_type != 'exe' and project_type != 'lib':
        raise ValueError('Project type is not approriate: %s' % project_type)
    configs['project']['type'] = project_type

    project_version = config_parser.get('project', 'version')
    if not re.match('^(\d\.)*\d$', project_version):
        raise ValueError('Project version is not approriate: %s' % project_version)
    configs['project']['version'] = project_version

    project_lib_version = config_parser.get('project', 'lib_version')
    if not re.match('^\d\:\d\:\d+$', project_lib_version):
        raise ValueError('Project lib version is not approriate: %s' % project_lib_version)
    configs['project']['lib_version'] = project_lib_version

    project_compiler = config_parser.getint('project', 'compiler')
    if project_compiler < 0 or project_compiler > 2:
        raise ValueError('Project compiler is not approriate: %d' % project_compiler)
    configs['project']['compiler'] = project_compiler

    #Src
    source_dirs = config_parser.get('src', 'source_dirs')
    if len(source_dirs) <= 0:
        raise ValueError('Source dirs is not set')
    configs['src']['source_dirs'] = source_dirs

    configs['src']['ignore_source_dirs'] = config_parser.get('src', 'ignore_source_dirs')
    configs['src']['ignore_header_files'] = config_parser.get('src', 'ignore_header_files')
    configs['src']['extra_dist'] = config_parser.get('src', 'extra_dist')

    #Library
    items = config_parser.items('library')
    for key, val in items:
        configs['library'][key] = val

    #Plugin
    items = config_parser.items('plugin')
    for key, val in items:
        configs['plugin'][key] = val

    #Misc
    debug = config_parser.getint('misc', 'debug')
    if debug != 0 and debug != 1:
        raise ValueError('Debug option error: %d' % debug)
    configs['misc']['debug'] = debug
    return configs
