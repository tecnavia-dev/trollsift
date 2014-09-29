import unittest

from trollsift.sftp_file_access import SftpFileAccess
import os, shutil

def make_dummy_file(path):
    open(path, 'w').close()

class TestSftpFileAccess(unittest.TestCase):
    def setUp(self):
        # make some files and dir under /tmp
        self.workdir="/tmp/test_trollsift"
        
        # clean up old test dir
        self.clean()

        # setup test files
        try:
            os.mkdir(self.workdir)
            os.mkdir(self.workdir+"/testdir1")
            os.mkdir(self.workdir+"/testdir2")
            make_dummy_file(self.workdir+"/file1")
            make_dummy_file(self.workdir+"/file2")
            make_dummy_file(self.workdir+"/file3")
            make_dummy_file(self.workdir+"/testdir1/file4")
            make_dummy_file(self.workdir+"/testdir1/filetoremove")
        except:
            self.skipTest("failed to write test files in "+self.workdir)

        # read in local ssh access file
        try:
            f = open("ssh_test_access","r")
            host = f.readline().strip()
            user = f.readline().strip()
            passwd = f.readline().strip()
        except:
            self.skipTest("no 'ssh_test_access' file defined")

        # instance
        self.access = SftpFileAccess(host, user, passwd)
        

    def tearDown(self):
        self.clean()
        

    def clean(self):
        try:
            shutil.rmtree(self.workdir)
        except:
            pass

    def test_list_dir(self):
        files = self.access.list_dir(self.workdir)
        self.assertItemsEqual(files,[self.workdir+'/file1',self.workdir+'/file2',self.workdir+'/file3'])

    def test_copy(self):
        self.access.copy(self.workdir+"/file1",self.workdir+"/testdir2/file5")
        self.assertItemsEqual( os.listdir(self.workdir+"/testdir2"), ['file5'])

    def test_remove(self):
        self.access.remove(self.workdir+"/testdir1/filetoremove")
        self.assertItemsEqual( os.listdir(self.workdir+"/testdir1"), ['file4'] )

    def test_rename(self):
        self.access.rename(self.workdir+"/file2", self.workdir+"/renamedfile") 
        print os.listdir(self.workdir)
        
        self.assertTrue( "renamedfile" in os.listdir(self.workdir) )
