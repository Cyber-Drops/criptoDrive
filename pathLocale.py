from os import path, getcwd, walk

def leggi_directory():
    directory = getcwd()  # leggo path del programma
    return directory
def path_scan(dir_name:str):
    '''
    Dato un path: stringa scansiona l'intero albero della path
    :param dir_name: path da scansionare
    :return: dizionario, key: str (root path); value: [[directory], [files]]
    '''
    dizio_path = {} # {root:[[directory],[files]]}
    for root, dirs, files in walk(dir_name):
        dizio_path[root] = [dirs, files] # index0: directory, index1:files(della radice)
    return dizio_path



