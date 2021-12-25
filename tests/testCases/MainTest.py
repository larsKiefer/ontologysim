import os
import subprocess
import unittest
import inspect
import sys
from importlib import reload
from os import listdir
from os.path import isfile

import owlready2
from owlready2 import Construct, close_world


from subprocess import Popen, PIPE

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)


from ProductionSimulation.utilities import init_utilities
from ProductionSimulation.utilities.init_utilities import Init

from ProductionSimulation.init.Initializer import Initializer

from example.Main import main
from tests.util.Timeout import timeoutTestCase

class MainTest(unittest.TestCase):
    """
    test all default files
    """

    def setUp(self):
        """
        set up method, which is called before every test
        :return:
        """
        self.init = None
        self.timeoutShort = 30
        self.timeoutMiddle = 60
        self.timeoutLong = 180

    #@unittest.skip
    def test_default_test(self):
        """
        test all files in /tests/configFiles/defaultTest/
        :return:
        """

        defaultTestPath = "/tests/configFiles/defaultTest/"

        onlyfiles = [f for f in listdir(parent_parent_dir + defaultTestPath) if isfile(os.path.join(parent_parent_dir + defaultTestPath, f))]

        self.assertTrue(len(onlyfiles)==4)

        listConfig = {}
        listConfig["production"] = defaultTestPath + "production_config_lvl3.ini"
        listConfig["config"] = defaultTestPath + "owl_config.ini"
        listConfig["controller"] = defaultTestPath + "controller_config.ini"
        listConfig["logger"] = defaultTestPath + "logger_config_lvl3.ini"
        output=""

        output = subprocess.check_output(
        'python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"',
        shell=True, stderr=subprocess.STDOUT, timeout=self.timeoutMiddle)

        self.assertTrue(output)

    #@unittest.skip
    def test_run_main_file(self):
        """
        test Main.py file
        :return:
        """
        output = subprocess.check_output('python '+ parent_parent_dir+'/example/Main.py',shell=True,stderr=subprocess.STDOUT, timeout=self.timeoutLong)

        self.assertTrue(output)

    #@unittest.skip
    def test_main_config_files(self):
        """
        test all predefined files in "/example/config/"
        :return:
        """
        defaultTestPath = "/example/config/"
        productionConifgFiles = ["production_config_lvl3.ini", "production_config_lvl2.ini",
                                 "production_config_lvl1.ini", "production_config.ini"]
        controllerConfigFiles = ["controller_config.ini"]
        owlConfigFiles = ["owl_config.ini"]
        loggerConfigFiles = ["logger_config_lvl3.ini", "logger_config_lvl2.ini"]

        #TODO add production_config_merge_lvl1

        onlyfiles = [f for f in listdir(parent_parent_dir+defaultTestPath) if isfile(os.path.join(parent_parent_dir+ defaultTestPath, f))]

        for file in onlyfiles:

            init = init_utilities.Init(parent_parent_dir+defaultTestPath+file)
            init.read_ini_file()
            init.identifyType()
            for type in init.type:
                if(type == "production"):
                    #TODO remove or case
                    self.assertTrue(file in productionConifgFiles or file == "production_config_merge_lvl1.ini")
                elif(type == "logger"):
                    self.assertTrue(file in loggerConfigFiles)
                elif(type == "controller"):
                    self.assertTrue(file in controllerConfigFiles)
                elif(type == "owl"):
                    self.assertTrue(file in owlConfigFiles)
                else:
                    raise Exception(str(type) + "not defined")


        for i, productionConfigFile in enumerate(productionConifgFiles):

            listConfig = {}
            listConfig["production"] = defaultTestPath + productionConfigFile
            listConfig["config"] =  defaultTestPath + owlConfigFiles[i%len(owlConfigFiles)]
            listConfig["controller"] = defaultTestPath + controllerConfigFiles[i%len(controllerConfigFiles)]
            listConfig["logger"] = defaultTestPath + loggerConfigFiles[i%len(loggerConfigFiles)]

            output = subprocess.check_output('python '+ parent_parent_dir+'/tests/processes/MainProcess.py '+ ' "'+str(listConfig)+'"',
                                        shell=True, stderr=subprocess.STDOUT, timeout=self.timeoutLong)

            self.assertTrue(output)




    def test_for_docu(self):
        """
        test all files in "/example/config/for_docu/"
        :return:
        """

        defaultTestPath = "/example/config/for_docu/"
        productionConifgFiles = ["production_config_lvl3.ini", "production_config_lvl2.ini",
                                 "production_config_lvl1.ini", "production_config.ini"]
        controllerConfigFiles = ["controller_config.ini","controller_config_extern.ini"]
        owlConfigFiles = ["owl_config.ini"]
        loggerConfigFiles = ["logger_config_lvl3.ini", "logger_config_lvl2.ini"]
        listConfig = {}

        onlyfiles = [f for f in listdir(parent_parent_dir + defaultTestPath) if
                     isfile(os.path.join(parent_parent_dir + defaultTestPath, f))]

        for file in onlyfiles:

            init = init_utilities.Init(parent_parent_dir + defaultTestPath + file)
            init.read_ini_file()
            init.identifyType()
            for type in init.type:
                if (type == "production"):
                    # TODO remove or case
                    self.assertTrue(file in productionConifgFiles or file == "production_config_merge_lvl1.ini")
                elif (type == "logger"):
                    self.assertTrue(file in loggerConfigFiles)
                elif (type == "controller"):
                    self.assertTrue(file in controllerConfigFiles)
                elif (type == "owl"):
                    self.assertTrue(file in owlConfigFiles)
                else:
                    raise Exception(str(type) + "not defined")

        for i, productionConfigFile in enumerate(productionConifgFiles):
            listConfig = {}
            listConfig["production"] = defaultTestPath + productionConfigFile
            listConfig["config"] = defaultTestPath + owlConfigFiles[i % len(owlConfigFiles)]
            listConfig["controller"] = defaultTestPath + controllerConfigFiles[i % len(controllerConfigFiles)]
            listConfig["logger"] = defaultTestPath + loggerConfigFiles[i % len(loggerConfigFiles)]

            output = subprocess.check_output(
                'python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"',
                shell=True, stderr=subprocess.STDOUT, timeout=self.timeoutMiddle)

            self.assertTrue(output)

    def test_flaskDefaultFiles(self):
        """
        test file in "/Flask/Assets/DefaultFiles/"
        :return:
        """
        defaultTestPath = "/Flask/Assets/DefaultFiles/"

        onlyfiles = [f for f in listdir(parent_parent_dir + defaultTestPath) if
                     isfile(os.path.join(parent_parent_dir + defaultTestPath, f))]

        self.assertTrue(len(onlyfiles) == 4)

        listConfig = {}
        listConfig["production"] = defaultTestPath + "production_config_lvl3.ini"
        listConfig["config"] = defaultTestPath + "owl_config.ini"
        listConfig["controller"] = defaultTestPath + "controller_config.ini"
        listConfig["logger"] = defaultTestPath + "logger_config_lvl3.ini"

        output = subprocess.check_output(
            'python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"',
            shell=True, stderr=subprocess.STDOUT, timeout=self.timeoutMiddle)
        print(output)
        self.assertTrue(output)



if __name__ == '__main__':
    unittest.main()