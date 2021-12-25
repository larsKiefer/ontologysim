from Flask.Actions.APIAction import APIAction

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from Flask.Actions.APIAction import APIAction
from ProductionSimulation.init.Initializer import Initializer
from ProductionSimulation.sim.Enum import Label

class KPIListAction(APIAction):
    """

    get: /kpiList: preparing the data so that they can be downloaded in the frontend
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
                transporterLocationSummary = self.flaskApp.simCore.logger.transporterLocationLogger.finale_evaluate_summary_api(time)
                simSummary = self.flaskApp.simCore.logger.simLogger.finale_evaluate_summary_api(time, machineSummary,
                                                                                                productSummary)
                queueSummary = self.flaskApp.simCore.logger.queueFillLevelLogger.finale_evaluate_summary_api(time)

                transporterTimeDict={}
                for k, v in self.flaskApp.simCore.logger.transporterLogger.time_kpis.items():
                    if k != "time":
                        transporterTimeDict[k]=self.flaskApp.simCore.logger.transporterLogger.getTimeList(k)
                transporterLocationTimeDict = {}
                for k, v in self.flaskApp.simCore.logger.transporterLogger.time_kpis.items():
                    if k != "time":
                        transporterLocationTimeDict[k] = self.flaskApp.simCore.logger.transporterLocationLogger.getTimeList(k)
                machineTimeDict={}
                for k, v in self.flaskApp.simCore.logger.machineLogger.time_kpis.items():
                    if k != "time":
                        machineTimeDict[k]=self.flaskApp.simCore.logger.machineLogger.getTimeList(k)
                productTimeDict={}
                for k, v in self.flaskApp.simCore.logger.productAnalyseLogger.time_kpis.items():
                    if k != "time":
                        productTimeDict[k]= self.flaskApp.simCore.logger.productAnalyseLogger.getTimeList(k)
                queueTimeDict={}

                for k, v in self.flaskApp.simCore.logger.queueFillLevelLogger.time_kpis.items():
                    if k != "time":
                        queueTimeDict[k] = self.flaskApp.simCore.logger.queueFillLevelLogger.getTimeList(k)

                response_dict ={
                    "transporter": {"summarized": self.flaskApp.simCore.logger.transporterLogger.getSummaryListAPI(transporterSummary), "time":
                        transporterTimeDict},
                    "transporter_location": {"summarized": self.flaskApp.simCore.logger.transporterLocationLogger.getSummaryListAPI(transporterLocationSummary), "time":
                        transporterLocationTimeDict},
                    "machine": {"summarized": self.flaskApp.simCore.logger.machineLogger.getSummaryListAPI(machineSummary), "time":
                        machineTimeDict},
                    "product": {"summarized": self.flaskApp.simCore.logger.productAnalyseLogger.getSummaryListAPI(productSummary), "time":
                        productTimeDict},
                    "sim": {"summarized": self.flaskApp.simCore.logger.simLogger.getSummaryListAPI(simSummary), "time":
                        {"all":self.flaskApp.simCore.logger.simLogger.getTimeList()}},
                    "queue": {"summarized": self.flaskApp.simCore.logger.queueFillLevelLogger.getSummaryListAPI(queueSummary), "time":
                        queueTimeDict}
                }

                self.response = self.response200OK(json.dumps(response_dict))
            else:

                self.response = self.response200OK(json.dumps({"transporter":{},"machine":{},"product":{},"sim":{},"queue":{}}))
        else:
            self.response = self.response200OK(
                json.dumps({"transporter": {}, "machine": {}, "product": {}, "sim": {}, "queue": {}}))

        return self.response