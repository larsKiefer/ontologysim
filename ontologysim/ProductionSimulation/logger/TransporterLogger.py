import copy
import math
import sys

from ontologysim.ProductionSimulation.database.models.TransporterKPI import TransporterTimeKPI, TransporterTimeKPIValue, \
    TransporterKPI
from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum
from ontologysim.ProductionSimulation.logger import SubLogger
from ontologysim.ProductionSimulation.sim.Enum import Transporter_Enum, Queue_Enum


class TransporterLogger(SubLogger.SubLogger):
    """
    calculates all transporter related kpi's
    """
    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.kpi_list = ["TTFp", "TTRp", "FE", "CMTp","ADOTp", "AUITp", "AUSTp", "AUTTp"]
        self.basic_kpi_list=[]
        self.last_value = {}
        self.number_of_transporters = 0

        # Time to failure (TTF): The actual time during which a transporter is able to produce, starting from the completion of
        # the repair and ending at a new failure. Such element is also referred to as Time between failure (TBF)

        # Time to repair (TTR): The actual time during which a transporter is unavailable due to a failure, i.e. under repair.

        # Failure event (FE): The count over a specified time interval of the terminations of the ability for a transporter to
        # perform a required operation.

        # Corrective maintenance time (CMT): The part of maintenance time during which corrective maintenance is performed
        # on a transporter.

        # Actual unit transporting time (AUTT): 
        # Actual production time (APT): The actual time in which the transporter is producing for an order, which only includes
        #       the value-adding functions.
        # Actual unit setup time (AUST): The time used for the preparation, i.e. setup, of an order on a transporter.
        #   Thus, the following relationship is observed:

        # Actual unit down time (ADOT): The actual time in which the production process is delayed due to malfunction-caused
        # interruptions, minor stoppages, and other unplanned events.

        # Actual unit idle time (AUIT): The actual time when the transporter is not executing order production even if it is
        #   available. This can also be referred to as actual unit delay time (ADET).

      

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        :return:

        """
        self.type = log_type_dict[Logger_Enum.TransporterLogger.value]

        if (self.isNotLogging()):

            for key, value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)
            return

        transporter_list = [transporter for transporter in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]
        self.number_of_transporter = len(transporter_list)
        self.number_of_instances=len(transporter_list)

        if (not self.isNotLogging()):
            self.summarized_kpis['all'] = {}
            for kpi in self.kpi_list:
                self.summarized_kpis['all'][kpi] = 0

            for transporter in transporter_list:
                transporter_name = transporter.name
                self.summarized_kpis[transporter_name] = {}

                for kpi in self.kpi_list:
                    self.summarized_kpis[transporter_name][kpi] = 0

        if (self.isTimeLogging()):
            self.time_kpis['time'] = []
            self.time_kpis['all'] = {}

            for kpi in self.kpi_list:
                self.time_kpis['all'][kpi] = []

            for transporter in transporter_list:
                transporter_name = transporter.name
                self.time_kpis[transporter_name] = {}

                for kpi in self.kpi_list:
                     self.time_kpis[transporter_name][kpi] = []

        if(not self.isNotLogging()):

            for transporter in transporter_list:
                transporter_name = transporter.name

                self.last_value[transporter_name] = {}
                for kpi in self.kpi_list:
                    self.last_value[transporter_name][kpi] = 0
                self.last_value[transporter_name]["TTFp"] = self.logger.simCore.getCurrentTimestep()


    def update_basic_kpis(self):
        """
        calculates the basic kpi's
        """
        pass

    def addElement(self, dict_element):
        """
        interface to the logger, all data from the simulation are provided through this class

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        """

        event_type = dict_element['type']
        time = dict_element['event_onto_time']

        if(self.isTimeLogging()):
            if len(self.time_kpis["time"]) < math.ceil(time / self.logger.time_intervall) - math.floor(
                    self.logger.start_time_logging / self.logger.time_intervall):
                time_index = int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)
                self.addNewTimeElement([transport.name for transport in
                                self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)],
                                       self.kpi_list, time)
                self.addNewTimeElement([transport.name for transport in
                                self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)],
                                       self.basic_kpi_list, time)
                time_multiple = math.floor(time / self.logger.time_intervall)
                time_len = len(self.time_kpis['time'])
                for i in range(time_index - time_len ,-1,-1):
                    self.time_kpis["time"].append((time_multiple - i) * self.logger.time_intervall)

                transporter_list = [transporter.name for transporter in
                                self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]

        if event_type == Transporter_Enum.Defect.value:

            transporter_name = dict_element['transporter_name']
            repair_time = dict_element['repair_time']
            triggered_defect_time = dict_element['triggered_defect_time']
            time = dict_element['event_onto_time']
            if(self.isSummaryLogging()):
                self.summarized_kpis[transporter_name]['FE'] += 1
                self.summarized_kpis[transporter_name]["TTFp"] += triggered_defect_time - self.last_value[transporter_name]["TTFp"]
                self.summarized_kpis[transporter_name]["TTRp"] += time - triggered_defect_time
                self.summarized_kpis[transporter_name]["CMTp"] += repair_time
                self.summarized_kpis[transporter_name]["ADOTp"] = self.summarized_kpis[transporter_name]["TTRp"]

            if(self.isTimeLogging()):
                self.addTimeElement(transporter_name, ["TTFp"], triggered_defect_time,
                                    triggered_defect_time - self.last_value[transporter_name]["TTFp"])
                self.addTimeElement(transporter_name, ["TTRp"], time, time - triggered_defect_time)
                self.addTimeElement(transporter_name, ["CMTp"], time, repair_time)

                self.addTimeSumElement(transporter_name, ["FE"], time, time - triggered_defect_time)

            self.last_value[transporter_name]["TTFp"] = time



        elif event_type == Transporter_Enum.Transport.value:
            transporter_name = dict_element['transporter_name']
            time_diff = dict_element['time_diff']
            dict_element = self.checkStartTimeLogging(dict_element)
            if(self.isTimeLogging()):
                self.addTimeElement(transporter_name, ["AUTTp"], time, time_diff)

            if(self.isSummaryLogging()):
                self.summarized_kpis[transporter_name]["AUTTp"] += time_diff


        elif event_type == Queue_Enum.Change.value:
            sys.error("not implemented",event_type)

        elif event_type == Queue_Enum.Default.value:
            sys.error("not implemented",event_type)

        elif event_type == Queue_Enum.AddToTransporter.value:
            time_diff = dict_element['time_diff']
            dict_element = self.checkStartTimeLogging(dict_element)
            queue_name = dict_element["queue_name"]
            transporter_name = self.logger.simCore.central.queue_to_transporter[queue_name]

            if (self.isSummaryLogging()):
                self.summarized_kpis[transporter_name]["AUSTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(transporter_name, ["AUSTp"], time, time_diff)

        elif  event_type == Queue_Enum.RemoveFromTransporter.value or event_type == Queue_Enum.RemoveFromTransporterDeadlock.value:
            time_diff = dict_element['time_diff']
            dict_element = self.checkStartTimeLogging(dict_element)
            queue_name = dict_element["old_queue_name"]

            transporter_name = self.logger.simCore.central.queue_to_transporter[queue_name]
            if (self.isSummaryLogging()):
                self.summarized_kpis[transporter_name]["AUSTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(transporter_name, ["AUSTp"], time, time_diff)

        elif event_type == Transporter_Enum.Wait.value:
            time_diff = dict_element['time_diff']
            dict_element = self.checkStartTimeLogging(dict_element)
            transporter_name = dict_element['transporter_name']
            if (self.isSummaryLogging()):
                self.summarized_kpis[transporter_name]['AUITp'] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(transporter_name, ["AUITp"], time, time_diff)
        else:
            print(event_type)
        #print(self.time_kpis["t0"]["AUST"])

    def setTTFlastValue(self,start_logging_time):
        """
        set for kpi ttf last value
        :param start_logging_time:
        :return:
        """
        if(not self.isNotLogging()):
            transporter_list = [transporter.name for transporter in
                            self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]
            for transporter_name in transporter_list:
                self.last_value[transporter_name]["TTFp"] =start_logging_time

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """

        transporter_list = [transporter.name for transporter in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]
        number_of_transporters=len(transporter_list)

        if(self.isTimeLogging()):
            for transporter_name in transporter_list:
                self.addTimeElement(transporter_name, ["TTFp"], time, time - self.last_value[transporter_name]["TTFp"])

            for k,v, in self.summarized_kpis.items():
                self.time_kpis[k]["ADOTp"] = self.time_kpis[k]["TTRp"]

        if(self.isSummaryLogging()):
            for transporter_name in transporter_list:
                self.summarized_kpis[transporter_name]["TTFp"] += time - self.last_value[transporter_name][
                    "TTFp"]
                for k1,v1 in self.summarized_kpis['all'].items():


                    self.summarized_kpis['all'][k1] += self.summarized_kpis[transporter_name][k1]
                    if k1 != 'FE':
                        self.summarized_kpis[transporter_name][k1] /= (time-self.logger.start_time_logging)

            for k1, v1 in self.summarized_kpis['all'].items():

                if k1 != 'FE':
                    self.summarized_kpis['all'][k1] /= (time-self.logger.start_time_logging)

                self.summarized_kpis['all'][k1] /= number_of_transporters

    def finale_evaluate_summary_api(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """

        transporter_list = [transporter.name for transporter in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]
        number_of_transporters=len(transporter_list)

        summarized_data = copy.deepcopy(self.summarized_kpis)

        for transporter_name in transporter_list:
            summarized_data[transporter_name]["TTFp"] += time - self.last_value[transporter_name][
                "TTFp"]
            for k1,v1 in summarized_data['all'].items():


                summarized_data['all'][k1] += summarized_data[transporter_name][k1]
                if k1 != 'FE':
                    summarized_data[transporter_name][k1] /= (time-self.logger.start_time_logging)

        for k1, v1 in summarized_data['all'].items():

            if k1 != 'FE':
                summarized_data['all'][k1] /= (time-self.logger.start_time_logging)
            summarized_data['all'][k1] /= number_of_transporters

        return summarized_data

    def save_to_database(self):
        """
        save to database
        :return:
        """
        transporter_list = [transporter.name for transporter in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]

        if (self.isTimeLogging()):
            transporterTimeKPI = TransporterTimeKPI(name='all')

            for i in range(0, len(self.time_kpis["time"])):
                input = {}
                for key, value in self.time_kpis["all"].items():
                    input[key] = value[i]

                transporterTimeKPIvalue = TransporterTimeKPIValue(**input,time=self.time_kpis["time"][i])
                transporterTimeKPI.transporterTimeKPIValue.append(transporterTimeKPIvalue)
                self.logger.dataBase.session.add(transporterTimeKPIvalue)

            self.logger.simulationRunDB.transporterTimeKPI.append(transporterTimeKPI)
            self.logger.dataBase.session.add(transporterTimeKPI)

            for transporter in transporter_list:

                transporterTimeKPI = TransporterTimeKPI(name=transporter)

                for i in range(0, len(self.time_kpis["time"])):
                    input = {}
                    for key, value in self.time_kpis[transporter].items():
                        input[key] = value[i]

                    transporterTimeKPIvalue = TransporterTimeKPIValue(**input,time=self.time_kpis["time"][i])
                    transporterTimeKPI.transporterTimeKPIValue.append(transporterTimeKPIvalue)
                    self.logger.dataBase.session.add(transporterTimeKPIvalue)
                self.logger.simulationRunDB.transporterTimeKPI.append(transporterTimeKPI)
                self.logger.dataBase.session.add(transporterTimeKPI)


        if (self.isSummaryLogging()):

            transporterKPI = TransporterKPI(name="all",**self.summarized_kpis['all'])
            self.logger.dataBase.session.add(transporterKPI)
            self.logger.simulationRunDB.transporterKPI.append(transporterKPI)

            for transporter in transporter_list:
                transporterKPI = TransporterKPI(name=transporter, **self.summarized_kpis[transporter])
                self.logger.simulationRunDB.transporterKPI.append(transporterKPI)
                self.logger.dataBase.session.add(transporterKPI)

        self.logger.dataBase.session.commit()