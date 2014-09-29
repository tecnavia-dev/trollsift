from .file_access_interface import FileAccessInterface
import os
import shutil
import paramiko
import stat

class SftpFileAccess(FileAccessInterface):

    __implements__ = (FileAccessInterface)

    os = os
    shutil = shutil

    def __init__(self, hostname, username, password=None, port=22):
        FileAccessInterface.__init__(self)
        # host info
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password
        # for holding connection open
        self.client = None
        self.sftp = None

    def list_dir(self, directory):
        directory = directory.rstrip("/")
        files = []

        sftp = self._get_connection()[0]
        for x in sftp.listdir_attr(directory):
            if stat.S_IFMT(x.st_mode) != stat.S_IFDIR:
                files.append(directory + "/" + x.filename)
        return files

    def rename(self, path1, path2):
        sftp = self._get_connection()[0]
        sftp.rename(path1,path2)

    def make_dir(self, directory):
        pass

    def remove(self, path):
        """
        Deletes a single file.
        """
        sftp = self._get_connection()[0]
        sftp.remove(path)

    def copy(self, filepath, newfilepath):
        """
        Create copy of a file on the file system.
        """
        client = self._get_connection()[1]
        #print client.exec_command("cp %s %s"%(filepath, newfilepath))

    def exists(self, filepath):
        sftp = self._get_connection()[0]
        try:
            sftp.lstat(filepath)
            return True
        except IOError:
            return False


    def _get_cur_connection(self):
        if self.client.get_transport().is_active():
            return self.sftp, self.client
        else:
            raise AttributeError()

    def _get_new_connection(self):
        # close for good measure
        self._close_connection()
        # establish new connection
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.hostname, self.port, username=self.username, password=self.password, timeout=10.0)
        self.sftp = self.client.open_sftp()
        return self.sftp, self.client

    def _get_connection(self):
        try:
            return self._get_cur_connection()
        except AttributeError:
            return self._get_new_connection()
            

    def _close_connection(self):
        try:
            self.sftp.close()
            self.client.close()
        except (NameError, AttributeError):
            pass
