import unittest
import os
import inspect
import sys


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)

from tests.testCases import FlaskAPITest, MainTest, MultipleRunTests,CrateDataBaseTest

# load all testcases from given module
suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromModule(FlaskAPITest))
suite.addTest(unittest.TestLoader().loadTestsFromModule(MainTest))
suite.addTest(unittest.TestLoader().loadTestsFromModule(MultipleRunTests))
suite.addTest(unittest.TestLoader().loadTestsFromModule(CrateDataBaseTest))


# run all tests with verbosity
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
