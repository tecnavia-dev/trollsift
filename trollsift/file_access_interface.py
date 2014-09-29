from abc import ABCMeta, abstractmethod
import os
import shutil

class FileAccessInterface(object):
    """
    Interface for file name and file manipulation
    methods on file systems.  This is an abstract
    base class to be inherited by implmenetions
    for local and remote file system access.
    """
    __metaclass__ = ABCMeta
    def __init__(self):
        self.os = os
        self.shutil = shutil

    def __init__(self):
        pass

    @abstractmethod
    def list_dir(self, directory):
        pass

    @abstractmethod
    def rename(self, path1, path2):
        pass

    @abstractmethod
    def make_dir(self, directory):
        pass

    @abstractmethod
    def remove(self, path):
        pass

    @abstractmethod
    def copy(self, path1, path2):
        pass

    @abstractmethod
    def exists(self, path):
        pass
