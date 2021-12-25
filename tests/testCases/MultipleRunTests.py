import ast
import configparser
import inspect
import json
import multiprocessing
import os
import shutil
import subprocess
import sys
import unittest
import logging
from datetime import datetime


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)

from tests.util.ControllerGenerator import ControllerGenerator
from tests.util.LoggerGenerator import LoggerGenerator
from tests.util.OwlGenerator import OwlGenerator
from tests.util.ProductionGenerator import ProductionGenerator


class MultipleRunTests(unittest.TestCase):
    """
    test simulation multiple times with ramdom configuration
    """
    def setUp(self):
        pass

    def test_100_runs_lvl1(self):
        """
        test only lvl1 configuration, 100 different configuration
        :return:
        """
        s = SimulationRun()
        fileName = "TestRun100.log"
        logging.basicConfig(filename=fileName, level=logging.INFO)
        logging.info(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        errorFound = False
        for i in range(100):
            try:
                s.simulationRunFixedLevel()
            except Exception as e:
                errorFound = True
                if (len(e.args) == 1):
                    error = e.args[0]
                    logging.error(error)
                else:
                    logging.error(e)

            logging.info("simulation run " + str(i) + " finished")

        self.assertTrue(not errorFound)

    def test_100_runs(self):
        """
        test 100 simulation run, all lvls
        :return:
        """

        s = SimulationRun()
        """
        procs = [multiprocessing.Process(target=s.simulationRun, args=()) for i in range(3)]

        for p in procs: p.start()
        for p in procs: p.join()
        """

        fileName = "TestRun100.log"
        logging.basicConfig(filename=fileName,level=logging.INFO)
        logging.info(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        errorFound = False
        for i in range(100):
            try:
                s.simulationRun(i)
            except Exception as e:
                errorFound = True
                if(len(e.args)==1):
                    error = e.args[0]
                    logging.error(error)
                else:
                    logging.error(e)

            logging.info("simulation run "+str(i)+" finished")

        self.assertTrue(not errorFound)


if __name__ == '__main__':
    unittest.main()

class SimulationRun():
    """
    class for creating a random configuration and run it in terminal
    """

    def __init__(self):
        """
        generate all Gnerator
        """
        #self.val = multiprocessing.Value('i', 0)
        #self.lock = multiprocessing.Lock()
        self.val = 0

        self.controllerGernerator = ControllerGenerator(100)
        self.owlGenerator = OwlGenerator()
        self.loggerGenerator = LoggerGenerator(100, "/example/log")
        self.productGenerator = ProductionGenerator(seedParameter=100)
        self.fixedLvl="lvl1"

    def simulationRun(self,number=-1):
        """
        run simulation in terminal with timoeout
        :param number: int: counter
        :return:
        """
        #with self.lock:
        #    self.val.value += 1
        #cretae config dicts
        self.val +=1
        owlDict = self.owlGenerator.createConfigDict()
        loggerDict = self.loggerGenerator.createConfigDict()
        productionDict = self.productGenerator.createConfigDict()
        controllerDict = self.controllerGernerator.createConfigDict()

        #folderName = "process" + str(self.val.value)
        folderName = "process" + str(self.val)
        try:
            os.mkdir(parent_dir + "/iniFiles/" + folderName)
        except:
            pass

        #write config files
        self.config_writer("../iniFiles/" + folderName + "/owl.ini", owlDict)
        self.config_writer("../iniFiles/" + folderName + "/logger.ini", loggerDict)
        self.config_writer("../iniFiles/" + folderName + "/production.ini", productionDict)
        self.config_writer("../iniFiles/" + folderName + "/controller.ini", controllerDict)
        defaultTestPath = "/tests/iniFiles/" + folderName + "/"
        listConfig = {}
        listConfig["production"] = defaultTestPath + "production.ini"
        listConfig["config"] = defaultTestPath + "owl.ini"
        listConfig["controller"] = defaultTestPath + "controller.ini"
        listConfig["logger"] = defaultTestPath + "logger.ini"
        output = None
        try:
            #print('python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"')
            output = subprocess.check_output(
                'python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"',
                shell=True, stderr=subprocess.STDOUT, timeout=180)
        except subprocess.CalledProcessError as e:

            raise Exception(json.dumps({"number":number,"message":e.output.decode("utf-8"),"cmd":e.cmd}))

        except Exception as e:
            print(output)
            raise e

        try:
            os.chmod(parent_dir + "/iniFiles/" + folderName, 0o777)
            shutil.rmtree(parent_dir + "/iniFiles/" + folderName)

        except:
            pass

        return True

    def simulationRunFixedLevel(self,number=-1):
        """
        run simulation in terminal with timoeout only lvl1 for production
        :param number: int: counter
        :return:
        """
        #with self.lock:
        #    self.val.value += 1
        self.val +=1
        owlDict = self.owlGenerator.createConfigDict()
        loggerDict = self.loggerGenerator.createConfigDict()
        productionDict = self.productGenerator.createConfigDict(self.fixedLvl)
        controllerDict = self.controllerGernerator.createConfigDict()

        #folderName = "process" + str(self.val.value)
        folderName = "process" + str(self.val)
        try:
            os.mkdir(parent_dir + "/iniFiles/" + folderName)
        except:
            pass

        self.config_writer("../iniFiles/" + folderName + "/owl.ini", owlDict)
        self.config_writer("../iniFiles/" + folderName + "/logger.ini", loggerDict)
        self.config_writer("../iniFiles/" + folderName + "/production.ini", productionDict)
        self.config_writer("../iniFiles/" + folderName + "/controller.ini", controllerDict)
        defaultTestPath = "/tests/iniFiles/" + folderName + "/"
        listConfig = {}
        listConfig["production"] = defaultTestPath + "production.ini"
        listConfig["config"] = defaultTestPath + "owl.ini"
        listConfig["controller"] = defaultTestPath + "controller.ini"
        listConfig["logger"] = defaultTestPath + "logger.ini"
        output = None
        try:
            #print('python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"')
            output = subprocess.check_output(
                'python ' + parent_parent_dir + '/tests/processes/MainProcess.py ' + ' "' + str(listConfig) + '"',
                shell=True, stderr=subprocess.STDOUT, timeout=180)
        except subprocess.CalledProcessError as e:

            raise Exception(json.dumps({"number":number,"message":e.output.decode("utf-8"),"cmd":e.cmd}))

        except Exception as e:
            print(output)
            raise e

        try:
            os.chmod(parent_dir + "/iniFiles/" + folderName, 0o777)
            shutil.rmtree(parent_dir + "/iniFiles/" + folderName)

        except:
            pass

        return True


    def config_writer(self, config_path, config: configparser.ConfigParser):
        """
        write config files to folder
        :param config_path: path
        :param config: configparser.ConfigParser
        :return:
        """
        with open(config_path, 'w') as configfile:
            config.write(configfile)