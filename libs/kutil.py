import re
import os

def split(s):
    ss = s.strip()
    if len(ss) == 0:
        return []
    else:
        return re.split('\s+', ss)

def end_with(s, tail):
    return re.search("^.*\\.%s$" % tail, s)

def start_with(s, head):
    return re.search('^%s$' % head, s)

def scan_recursive(folder, ignore, c = 1):
    file_list = []
    _scan_recursive(file_list, folder, ignore, c)
    return file_list

def _scan_recursive(file_list, folder, ignore, c):
    folder_files = os.listdir(folder)
    folder_files.sort()
    for fname in folder_files:
        path = folder + '/' + fname
        if not (path in ignore):
            if os.path.isdir(path):
                _scan_recursive(file_list, path, ignore, c)
            else:
                if c == 1:
                    if end_with(fname, "c") or end_with(fname, "cpp") or end_with(fname, "h") or end_with(fname, "hpp") or end_with(fname, "cc"):
                        file_list.append(path)
                else:
                    if end_with(fname, "h") or end_with(fname, "hpp"):
                        file_list.append(path)
                    


def print_source(sources):
    l = len(sources)
    output = ''
    if l > 0:
        output += '\\\n\t\t' + sources[0]
        if l == 1:
            output += '\n'
        elif l == 2:
            output += '\\\n'
            output += '\t\t' + sources[1] + '\n'
        else:
            output += '\\\n'
            for i in xrange(1, l - 1):
                output += '\t\t' + sources[i] + '\\\n'
            output += '\t\t' + sources[l - 1] + '\n'
    output += '\n'
    return output
    
