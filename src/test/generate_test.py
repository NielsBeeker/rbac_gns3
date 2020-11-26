import unittest
import pytest





#function to read test from a file
class MyTest(unittest.TestCase):
    @pytest.mark.usefixtures(autouse=True)
    def initdir(self, tmpdir):
        tmpdir.chdir()
        tmpdir.join("samplefile.ini").write("# testdata")
    def test_method(self):
        with open("samplefile.ini") as f:
            s = f.read()
            assert "testdata" in s



