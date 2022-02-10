import inspect
import os
import sys

from flask import json, request

from ontologysim.Flask.Actions.UtilMethods.ProductionDict import ProductionDict
from ontologysim.ProductionSimulation.sim.Enum import Label

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.init.Initializer import Initializer
from ontologysim.ProductionSimulation.init.TransformProductionIni import TransformProductionIni
from ontologysim.ProductionSimulation.utilities import init_utilities


class ProductionAction(APIAction):
    """
    /production: post: production ini to dict
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        requestBody=request.data

        if (len(requestBody) ==0):
            return self.response400BadRequest("request body is not correct")
        requestDict =json.loads(requestBody)

        if("data" in requestDict.keys()):

            productionData=requestDict["data"]

            initializer = Initializer(current_dir)
            initializer.initSimCore()
            try:
                initializer.s.destroyOnto()
            except:
                print("not deletable")
            initializer.initSimCore()

            simCore = initializer.s
            try:

                sim_conf = init_utilities.IniString(productionData)

                sim_conf.read_ini_file()

                sim_conf.configs = TransformProductionIni(simCore).transform_ini(sim_conf.configs)

                initializer.initProductionComponents(sim_conf)

                responseDict = ProductionDict.getProductionDict(simCore)

                initializer.s.destroyOnto()


                self.response = self.response200OK(json.dumps(responseDict))
            except Exception as err:

                self.response = self.response400BadRequest(str(err))

        else:
            self.response = self.response400BadRequest("request body is not correct")

        return self.response