import unittest

from trollsift.local_file_access import LocalFileAccess
import os, shutil

def make_dummy_file(path):
    open(path, 'w').close()

class TestLocalFileAccess(unittest.TestCase):
    def setUp(self):
        # make some files and dir under /tmp
        self.workdir="/tmp/test_pygranule"

        os.mkdir(self.workdir)
        os.mkdir(self.workdir+"/testdir1")
        os.mkdir(self.workdir+"/testdir2")
        make_dummy_file(self.workdir+"/file1")
        make_dummy_file(self.workdir+"/file2")
        make_dummy_file(self.workdir+"/file3")
        make_dummy_file(self.workdir+"/testdir1/file4")
        make_dummy_file(self.workdir+"/testdir1/filetoremove")

        # instance
        self.access = LocalFileAccess()

    def tearDown(self):
        shutil.rmtree(self.workdir)

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
