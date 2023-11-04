import os
import subprocess
import unittest
import inspect
import sys
from os import listdir
from os.path import isfile


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


from ontologysim.ProductionSimulation.utilities import init_utilities


class CreateDataBaseTest(unittest.TestCase):
    """
    test all default files
    """

    def setUp(self):

        path="/ontologysim/ProductionSimulation/database/SimulationRun.db"
        try:
            path = PathTest.check_dir_path_current_dir_given(path,os.getcwd())
            print(path)
            os.remove(path)
        except Exception as ex:
            print(ex)
        pass

    def test_get_test_connection(self):
        """
        test setup of new database
        :return:
        """

        output = ""
        path = "/ontologysim/ProductionSimulation/database/CreateDatabase.py"
        path = PathTest.check_file_path_current_dir_given(path,os.getcwd())

        output = subprocess.check_output(
            'python ' + path ,
            shell=True, stderr=subprocess.STDOUT, timeout=180)

        self.assertTrue("DB creation successfull" in output.decode("utf-8"))




if __name__ == "__main__":
    unittest.main()