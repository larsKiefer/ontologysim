from ontologysim.Flask.Actions.APIAction import APIAction

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.init.Initializer import Initializer
from ontologysim.ProductionSimulation.sim.Enum import Label

class KPIAction(APIAction):
    """

    get: /kpi: get list of all kpi values (summary and time)
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        if(self.flaskApp.simCore!=None):
            if self.flaskApp.simCore!=None:

                time = self.flaskApp.simCore.getCurrentTimestep()
                machineSummary = self.flaskApp.simCore.logger.machineLogger.finale_evaluate_summary_api(time)
                productSummary = self.flaskApp.simCore.logger.productAnalyseLogger.finale_evaluate_summary_api(time)
                transporterSummary = self.flaskApp.simCore.logger.transporterLogger.finale_evaluate_summary_api(time)
                simSummary = self.flaskApp.simCore.logger.simLogger.finale_evaluate_summary_api(time,machineSummary,productSummary)
                queueSummary = self.flaskApp.simCore.logger.queueFillLevelLogger.finale_evaluate_summary_api(time)
                transporterLocationSummary = self.flaskApp.simCore.logger.transporterLocationLogger.finale_evaluate_summary_api(
                    time)
                response_dict ={
                    "transporter": {"summarized": transporterSummary, "time":
                        self.flaskApp.simCore.logger.transporterLogger.time_kpis},
                    "transporter_location": {"summarized":transporterLocationSummary,"time":
                                             self.flaskApp.simCore.logger.transporterLocationLogger.time_kpis},
                    "machine": {"summarized": machineSummary, "time":
                        self.flaskApp.simCore.logger.machineLogger.time_kpis},
                    "product": {"summarized": productSummary, "time":
                        self.flaskApp.simCore.logger.productAnalyseLogger.time_kpis},
                    "sim": {"summarized": simSummary, "time":
                        self.flaskApp.simCore.logger.simLogger.time_kpis},
                    "queue": {"summarized": queueSummary, "time":
                        self.flaskApp.simCore.logger.queueFillLevelLogger.time_kpis}
                }

                self.response = self.response200OK(json.dumps(response_dict))
            else:

                self.response = self.response200OK(json.dumps({"transporter":{},"transporter_location":{},"machine":{},"product":{},"sim":{},"queue":{}}))
        else:
            self.response = self.response200OK(
                json.dumps({"transporter": {},"transporter_location":{}, "machine": {}, "product": {}, "sim": {}, "queue": {}}))

        return self.response