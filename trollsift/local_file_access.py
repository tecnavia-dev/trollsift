
from .file_access_interface import FileAccessInterface
import os
import shutil

def _make_dirs(path, os_obj = None):
    if os_obj is not None:
        os = os_obj
    if path is not None:
        dname = os.path.dirname(path)
        if not os.path.isdir(dname):
            os.makedirs(dname)


class LocalFileAccess(FileAccessInterface):

    os = os
    shutil = shutil

    def __init__(self):
        FileAccessInterface.__init__(self)

    def list_dir(self, directory):
        """
        Lists directory on the source file system
        Returns a list of filenames including their full
        paths within the source file system.
        E.g. from .list_directory("/home/ftp/data/avhrr/") -->
        ["/home/ftp/data/avhrr/avh_noaa19_20140225_1400.hrp.bz2",
         "/home/ftp/data/avhrr/avh_noaa19_20140225_1401.hrp.bz2",
         "/home/ftp/data/avhrr/avh_noaa19_20140225_1403.hrp.bz2"]
        """
        return [ directory + '/' + x for x in self.os.listdir(directory) 
                 if self.os.path.isfile(directory+'/'+x) ]

    def rename(self, path1, path2):
        self.os.rename(path1, path2)

    def make_dir(self, directory):
        pass

    def remove(self, path):
        """
        Deletes a single file.
        """
        self.os.remove(path)

    def copy(self, filepath, newfilepath):
        """
        Create copy of a file on file system.
        """
        _make_dirs(newfilepath, os_obj = self.os)
        self.shutil.copyfile(filepath, newfilepath)
