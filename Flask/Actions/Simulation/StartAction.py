import inspect
import os
import sys
from distutils.util import strtobool

from Flask.Actions.UtilMethods.ProductionDict import ProductionDict
from Flask.Actions.UtilMethods.StateStorage import StateStorage
from ProductionSimulation.init.Initializer import Initializer
from ProductionSimulation.init.TransformLoggerIni import TransformLoggerIni
from ProductionSimulation.init.TransformProductionIni import TransformProductionIni
from ProductionSimulation.utilities import init_utilities

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from Flask.Actions.APIAction import APIAction
from ProductionSimulation.sim.Enum import Label


class StartAction(APIAction):
    """
    post: /start: start simulation
    """


    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()
        fileDict = self.flaskApp.fileDict

        try:
            self.flaskApp.init.s.destroyOnto()
        except:
            print("onto not defined")
        self.flaskApp.init.initSimCore()

        requestBody = request.data

        if (len(requestBody) == 0):
            return self.response400BadRequest("request body is not correct")
        requestDict = json.loads(requestBody)

        if ("defaultFiles" in requestDict.keys() and "files" in requestDict.keys() and "isDefaultSelected" in requestDict.keys() and "isDragDropSelected" in requestDict.keys() ):


            isDefaultSelected = requestDict["isDefaultSelected"]
            isDragDropSelected = requestDict["isDragDropSelected"]
            files = requestDict["files"]
            defaultFiles = requestDict["defaultFiles"]

            if (isDragDropSelected and isDefaultSelected):

                self.response = self.response400BadRequest("isDefaultSelected and isDragDropSelected error")

            elif (not isDragDropSelected and isDefaultSelected):

                self.flaskApp.init.restart(production_config_path=fileDict['production'],
                                           owl_config_path=fileDict['owl'],
                                           controller_config_path=fileDict['controller'],
                                           logger_config_path=fileDict['logger'],dataBase=self.flaskApp.db)


                self.flaskApp.simCore = self.flaskApp.init.s
                self.flaskApp.simCore.run_as_api = True

                responseDict = ProductionDict.getProductionDict(self.flaskApp.simCore)

                self.response = self.response200OK(json.dumps({"alreadyStarted": self.flaskApp.simCore.run_as_api,
                                                               "run": True,"production":responseDict}))
                self.flaskApp.startAlready = True

            elif (not isDefaultSelected and isDragDropSelected):

                StartAction.loadSimulationFromFiles(self.flaskApp.init,requestDict)

                self.flaskApp.init.run_until_first_event()
                self.flaskApp.simCore = self.flaskApp.init.s
                self.flaskApp.simCore.run_as_api = True

                responseDict = ProductionDict.getProductionDict(self.flaskApp.simCore)

                self.response = self.response200OK(json.dumps({"alreadyStarted": True,
                                                               "run": True, "production": responseDict}))
                self.flaskApp.startAlready = True

            else:
                self.response = self.response400BadRequest("no selection")


        return self.response

    @classmethod
    def loadSimulationFromFiles(cls,init,requestDict):
        """
        used when drag drop is selected and transform file content to ini

        :param init:
        :param requestDict:
        :return:
        """

        init.initSimCore()
        simCore = init.s
        iniConfDict = {}
        for file in requestDict["files"]:
            # print(file)
            conf = init_utilities.IniString(file["content"])
            conf.read_ini_file()
            conf.identifyType()
            for type in conf.type:
                iniConfDict[type] = conf

        if "production" in iniConfDict.keys():
            iniConfDict["production"].configs = TransformProductionIni(simCore).transform_ini(
                iniConfDict["production"].configs)
            init.initProductionComponents(iniConfDict["production"])
            init.addTask(iniConfDict["production"])
            init.addDefect(iniConfDict["production"])
        if "owl" in iniConfDict.keys():
            pass
        if "logger" in iniConfDict.keys():
            log_conf = TransformLoggerIni(simCore).transform_ini(iniConfDict["logger"].configs)
            init.addLogger(log_conf)
        if "controller" in iniConfDict.keys():
            init.loadController(iniConfDict["controller"])


