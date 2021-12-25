from distutils.util import strtobool

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from Flask.Actions.APIAction import APIAction
from Flask.Actions.UtilMethods.ProductionDict import ProductionDict
from ProductionSimulation.init.Initializer import Initializer
from ProductionSimulation.sim.Enum import Label


class EventAction(APIAction):
    """
    get: /nextEvent get event list
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()
        number = request.args.get('number', default=1, type=int)
        full_data = request.args.get('full', default="True", type=str)
        production_included = request.args.get('production', default="True", type=str)

        self.flaskApp.simCore.changeStorageState=strtobool(production_included)

        if(self.flaskApp.startAlready):
            even_onto_list = []

            if not self.flaskApp.simCore.run:
                    self.response = Response(status=200, headers={},
                                             response={json.dumps({"eventOntoList": [],"simulationFinished":not self.flaskApp.simCore.run})},
                                             mimetype='application/json')

            else:
                for i in range(number):

                    event_list = self.flaskApp.simCore.runNextEvent()
                    if strtobool(full_data):
                        even_onto_list.append(self.flaskApp.simCore.event_utilities.transformEventListToFullDict(event_list))
                    else:
                        even_onto_list.append(self.flaskApp.simCore.event_utilities.transformEventListToDict(event_list))



                if(self.flaskApp.simCore.changeStorageState):
                    production_dict = ProductionDict.getProductionDict(self.flaskApp.simCore)
                    self.response =  Response(status=200, headers={}, response={json.dumps({"eventOntoList":even_onto_list,"productionDict":production_dict,"simulationFinished":not self.flaskApp.simCore.run})},
                                         mimetype='application/json')
                else:
                    self.response = Response(status=200, headers={},
                                             response={json.dumps({"eventOntoList": even_onto_list,"simulationFinished":not self.flaskApp.simCore.run})},
                                             mimetype='application/json')
        else:
            self.response = self.response400BadRequest("simulation not started")

        return self.response


