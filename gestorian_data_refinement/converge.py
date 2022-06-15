import pathlib
import glob
import os
import shutil
from typing import Union

#Pathlike = Union[str, pathlib.Path]
class converge():
    def __init__(self):
        return None
    def converge(self):
        parent_dir = '../Lab_strains'
        li = []
        for dir in os.listdir(parent_dir):
            path = os.path.join(parent_dir, dir)
            files = glob.glob(path + '/*pattern_identification.txt')
            li.append(files)
        return li

    def converge_files(self, out_file_path):
        with open(out_file_path , 'wb') as wfd:
            li = self.converge()
            for f in li:
                if len(f)> 0:
                    for n in range(len(f)):
                        f = str(f[n])
                        with open(f, 'rb') as fd:
                            shutil.copyfileobj(fd,wfd) 
        return None


