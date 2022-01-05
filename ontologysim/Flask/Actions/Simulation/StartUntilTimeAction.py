from flask import Response, json, request

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.Flask.Actions.Simulation import StartAction
from ontologysim.Flask.Actions.UtilMethods.ProductionDict import ProductionDict


class StartUntilTimeAction(APIAction):
    """
    post: /startUntilTime: staring the simulation until a given time
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


        if ("defaultFiles" in requestDict.keys() and "files" in requestDict.keys() and "isDefaultSelected" in requestDict.keys() and "isDragDropSelected" in requestDict.keys() and "time" in requestDict.keys()):



            isDefaultSelected = requestDict["isDefaultSelected"]
            isDragDropSelected = requestDict["isDragDropSelected"]
            files = requestDict["files"]
            defaultFiles = requestDict["defaultFiles"]
            time= int(requestDict["time"])

            if (isDragDropSelected and isDefaultSelected):

                self.response = self.response400BadRequest("isDefaultSelected and isDragDropSelected error")

            elif (not isDragDropSelected and isDefaultSelected):

                self.flaskApp.init.restart(production_config_path=fileDict['production'],
                                           owl_config_path=fileDict['owl'],
                                           controller_config_path=fileDict['controller'],
                                           logger_config_path=fileDict['logger'],dataBase=self.flaskApp.db)
                self.flaskApp.simCore = self.flaskApp.init.s
                self.flaskApp.simCore.run_as_api = True
                self.flaskApp.simCore.run = True
                self.flaskApp.startAlready=True

                self.flaskApp.simCore.order_release.orderReleaseController.evaluateCreateOrderRelease()
                event_list = []

                if(not requestDict["onlyLastEvent"]):
                    while (self.flaskApp.simCore.getCurrentTimestep()<time and self.flaskApp.simCore.run):
                        event_list.append(self.flaskApp.simCore.event_utilities.transformEventListToFullDict(self.flaskApp.simCore.runNextEvent()))
                    production_dict = ProductionDict.getProductionDict(self.flaskApp.simCore)

                    self.response = Response(status=200, headers={}, response={json.dumps({"eventOntoList":event_list,"productionDict":production_dict,"simulationFinished":not self.flaskApp.simCore.run})},
                                             mimetype='application/json')
                else:
                    event_value=None
                    while (self.flaskApp.simCore.getCurrentTimestep() < time and self.flaskApp.simCore.run):
                        event_value=self.flaskApp.simCore.event_utilities.transformEventListToFullDict(
                            self.flaskApp.simCore.runNextEvent())
                    production_dict = ProductionDict.getProductionDict(self.flaskApp.simCore)

                    self.response = Response(status=200, headers={}, response={json.dumps({"eventOntoList": [event_value],"productionDict":production_dict,"simulationFinished": not self.flaskApp.simCore.run})},
                                             mimetype='application/json')


            elif (not isDefaultSelected and isDragDropSelected):

                StartAction.loadSimulationFromFiles(self.flaskApp.init, requestDict)
                self.flaskApp.startAlready = True
                self.flaskApp.simCore = self.flaskApp.init.s
                self.flaskApp.init.run_until_first_event()
                self.flaskApp.simCore.run_as_api = True
                event_list = []
                if (not requestDict["onlyLastEvent"]):
                    while (self.flaskApp.simCore.getCurrentTimestep()<time and self.flaskApp.simCore.run):
                        event_list.append(self.flaskApp.simCore.event_utilities.transformEventListToFullDict(self.flaskApp.simCore.runNextEvent()))

                    production_dict = ProductionDict.getProductionDict(self.flaskApp.simCore)
                    self.response = Response(status=200, headers={}, response={json.dumps({"eventOntoList": event_list,"productionDict":production_dict,"simulationFinished": not self.flaskApp.simCore.run})},
                                             mimetype='application/json')
                else:
                    event_value = None
                    while (self.flaskApp.simCore.getCurrentTimestep() < time and self.flaskApp.simCore.run):
                        event_value = self.flaskApp.simCore.event_utilities.transformEventListToFullDict(
                            self.flaskApp.simCore.runNextEvent())

                    production_dict = ProductionDict.getProductionDict(self.flaskApp.simCore)
                    self.response = Response(status=200, headers={},
                                             response={json.dumps({"eventOntoList": [event_value],"productionDict":production_dict,"simulationFinished":not self.flaskApp.simCore.run})},
                                             mimetype='application/json')


            else:
                self.response = self.response400BadRequest("no selection")

        return self.response