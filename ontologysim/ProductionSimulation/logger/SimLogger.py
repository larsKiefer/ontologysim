import copy
import csv
import math

from ontologysim.ProductionSimulation.database.models.SimulationKPI import SimulationTimeKPI, SimulationTimeKPIValue, SimulationKPI
from ontologysim.ProductionSimulation.logger.Enum_Logger import Folder_name, Logger_Enum
from ontologysim.ProductionSimulation.logger import SubLogger
from ontologysim.ProductionSimulation.sim.Enum import Evaluate_Enum, OrderRelease_Enum, Label
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


class SimLogger(SubLogger.SubLogger):
    """
    calculates all simulation related kpi's
    """

    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.kpi_list = ["WIP","logging_time"]
        self.basic_kpi_list = ["AR", "PR"]
        self.number_of_instances = 0
        self.last_time = 0
        self.last_WIP = 0

        self.machine_update = False
        self.product_update = False

        # Allocation ratio (AR): The percentage of actual busy time of allmachines (AU BT ) among theAOETof a production
        # order. The complementary proportion describes the ratio of actual queuing and transportation time.

        # Production process ratio (PR): The efficiency of production when considering the actual unit setup time, delay time,
        #   transportation time, and queuing time. It is the ratio between theAPT over all work units and work centers involved
        #   in a production order and the whole throughput time of a production order which is the AOET.

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        """
        self.type = log_type_dict[Logger_Enum.SimLogger.value]

        if (self.isNotLogging()):

            for key, value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)

            return


        if(not self.isNotLogging()):
            self.number_of_instances = 1
            self.summarized_kpis['all'] = {}
            self.summarized_kpis['all']["WIP"] = 0
            self.summarized_kpis['all']['logging_time'] =0

        if(self.isTimeLogging()):
            self.time_kpis['time'] = []
            self.time_kpis['all'] = {}
            self.time_kpis['all']["WIP"] = []
            self.time_kpis['all']["AR"] = []
            self.time_kpis['all']["PR"] = []
            self.time_kpis['all']['logging_time'] = []

    def setLastWIP(self):
        """
        calculates the wip and save the value to last wip

        :return:
        """
        number_of_products = 0
        for queue in self.logger.simCore.central.queue_list:
            if Label.EndQueue.value not in queue.name:
                for position in queue.has_for_position:
                    if position.blockedSpace == 1:
                        if len(position.has_for_product) > 0:
                            number_of_products += 1

        self.last_WIP = number_of_products


    def addElement(self, dict_element):
        """
        interface to the logger, all data from the simulation are provided through this class

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        """

        event_type = dict_element['type']
        time = dict_element['event_onto_time']
        time_index = int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)
        if(self.isTimeLogging()):
            if len(self.time_kpis["time"]) < math.ceil(time / self.logger.time_intervall) - math.floor(
                    self.logger.start_time_logging / self.logger.time_intervall):

                self.addNewTimeElement([],
                                       self.basic_kpi_list, time)
                self.addNewTimeElement([],
                                       ["WIP"], time)

                time_multiple = math.floor(time / self.logger.time_intervall)
                time_len = len(self.time_kpis['time'])
                for i in range(time_index - time_len, -1, -1):
                    self.time_kpis["time"].append((time_multiple - i) * self.logger.time_intervall)
                    self.time_kpis['all']["logging_time"].append(self.logger.time_intervall)
                # update-list is set by machine_logger
                self.update_list.append(time_index - 1)
                self.update_basic_kpis()

        if event_type == OrderRelease_Enum.Release.value:
            time = dict_element["event_onto_time"]
            number_of_products = dict_element["number_of_products"]
        elif event_type == Evaluate_Enum.ProductFinished.value:
            time = dict_element["event_onto_time"]
            number_of_products = -1

        if (self.isTimeLogging()):

            self.addWIPTimeElement(["WIP"], time, time - self.last_time, self.last_WIP)

        if(self.isSummaryLogging()):
            self.summarized_kpis['all']['WIP'] += (self.last_WIP ) * (time - self.last_time)

        self.last_WIP = self.last_WIP + number_of_products
        self.last_time = time

    def addWIPTimeElement(self, kpi_key_list, time, time_diff,wip):
        """
        adds a new value to the time element (time intervall)

        :param object_name: label
        :param kpi_key_list: [KPI's name]
        :param time: double
        :param time_diff: double
        :return:
        """
        if(self.isTimeLogging()):
            split_time_dict = self.split_time(time, time_diff)
            self.update_list.extend(list(split_time_dict.keys()))

            for k, v in split_time_dict.items():
                for kpi_key in kpi_key_list:
                    # if object_name=="m4" and kpi_key=="APT":
                    #    print(interval_offset, len(self.time_kpis["time"]),self.time_kpis["time"][-(i+interval_offset+1)])
                    #    print(time,time_diff,current_time_element,-(i+interval_offset+1),i)
                    # print(current_time_element,time,time_diff,-(i+interval_offset+1),self.time_kpis[object_name][kpi_key])
                    time_intervall_diff = v['time_diff']

                    self.time_kpis["all"][kpi_key][
                        k] += time_intervall_diff / self.logger.time_intervall * wip

    def update_basic_kpis(self):
        """
        calculates the basic kpi's
        """
        if(self.isTimeLogging()):
            if self.product_update and self.machine_update:

                for update_index in self.update_list:
                    if self.logger.productAnalyseLogger.time_kpis["all"]["AOET"][update_index] > 0:
                        self.time_kpis['all']["AR"][update_index] = self.logger.machineLogger.time_kpis["all"]["AUBTp"][
                                                                        update_index] / \
                                                                    self.logger.productAnalyseLogger.time_kpis["all"][
                                                                        "AOET"][update_index]
                        self.time_kpis['all']["PR"][update_index] = self.logger.machineLogger.time_kpis["all"]["APTp"][
                                                                        update_index] / \
                                                                    self.logger.productAnalyseLogger.time_kpis["all"][
                                                                        "AOET"][update_index]
                self.update_list = []
                self.product_update = False
                self.machine_update = False

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """
        if(self.isSummaryLogging() ):
            self.summarized_kpis['all']['WIP'] /= (time - self.logger.start_time_logging)
            self.summarized_kpis['all']['AR'] = self.logger.machineLogger.summarized_kpis["all"]["AUBTp"] / \
                                                self.logger.productAnalyseLogger.summarized_kpis["all"]["AOET"]
            self.summarized_kpis['all']['PR'] = self.logger.machineLogger.summarized_kpis["all"]["APTp"] / \
                                                self.logger.productAnalyseLogger.summarized_kpis["all"]["AOET"]
            self.summarized_kpis['all']['logging_time']=(time - self.logger.start_time_logging)

    def finale_evaluate_summary_api(self,time,machineSummary, productSummary):
        """
        finale evalueate for api

        :param time:
        :param machineSummary:
        :param productSummary:
        :return:
        """
        summarized_data = copy.deepcopy(self.summarized_kpis)
        summarized_data['all']['WIP'] /= (time - self.logger.start_time_logging)
        summarized_data['all']['AR'] = machineSummary["all"]["AUBTp"] / \
                                            productSummary["all"]["AOET"]
        summarized_data['all']['PR'] = machineSummary["all"]["APTp"] / \
                                            productSummary["all"]["AOET"]
        summarized_data['all']['logging_time'] = (time - self.logger.start_time_logging)

        return summarized_data

    def save_to_csv(self, path, folder_name, summarized_name):
        """
        saves the kpi to a csv

        :param path:
        :param folder_name:
        :param summarized_name:
        :return:
        """
        if(not self.isNotLogging()):
            path_sim = PathTest.create_new_folder(path, Folder_name.sim.value)


            if(self.isSummaryLogging()):
                with open(PathTest.check_dir_path(path + "/" + summarized_name + ".csv"), "w", newline='') as order_logger:
                    wr = csv.writer(order_logger, delimiter=';', quoting=csv.QUOTE_ALL)

                    erg_list=self.getSummaryList()
                    wr.writerows(erg_list)

            if(self.isTimeLogging()):
                with open(PathTest.check_dir_path(path_sim + "/sim0" + "_" + summarized_name + ".csv"), "w",
                          newline='') as sim_logger:
                    wr = csv.writer(sim_logger, delimiter=';', quoting=csv.QUOTE_ALL)

                    erg_list = self.getTimeList()
                    wr.writerows(erg_list)

    def getTimeList(self):
        """
        transform dict of time kpi data to list
        :return:
        """
        erg_list = []

        header = ["time"]
        header.extend([str(k) for k, v in self.time_kpis['all'].items()])
        erg_list.append(header)

        for i in range(len(self.time_kpis["time"])):
            erg = [self.time_kpis["time"][i]]
            for k1, v1 in self.time_kpis['all'].items():
                erg.append(round(v1[i], 4))
            erg_list.append(erg)

        return erg_list

    def getSummaryList(self):
        """
        transfrom dict of summary kpi data to list
        :return:
        """
        erg_list = []
        header = ["name"]
        header.extend([str(k) for k, v in self.summarized_kpis['all'].items()])
        erg_list.append(header)

        for k, v in self.summarized_kpis.items():
            erg = [str(k)]
            for k1, v1 in v.items():
                erg.append(round(v1, 4))
            erg_list.append(erg)

        return erg_list

    def getSummaryListAPI(self,summarized_data):
        """
        transfrom dict of summary kpi data to list
        :param summarized_data:
        :return:
        """
        erg_list = []
        header = ["name"]
        header.extend([str(k) for k, v in summarized_data['all'].items()])
        erg_list.append(header)

        for k, v in summarized_data.items():
            erg = [str(k)]
            for k1, v1 in v.items():
                erg.append(round(v1, 4))
            erg_list.append(erg)

        return erg_list

    def save_to_database(self):
        """
        save to database
        :return:
        """
        if (self.isTimeLogging()):
            simulationTimeKPI = SimulationTimeKPI(name='all')

            for i in range(0, len(self.time_kpis["time"])):
                input = {}
                for key, value in self.time_kpis["all"].items():
                    input[key] = value[i]

                simulationTimeKPIvalue = SimulationTimeKPIValue(**input,time=self.time_kpis["time"][i])
                simulationTimeKPI.simulationTimeKPIValue.append(simulationTimeKPIvalue)
                self.logger.dataBase.session.add(simulationTimeKPIvalue)

            self.logger.simulationRunDB.simulationTimeKPI.append(simulationTimeKPI)
            self.logger.dataBase.session.add(simulationTimeKPI)



        if (self.isSummaryLogging()):

            simulationKPI = SimulationKPI(name="all",**self.summarized_kpis['all'])
            self.logger.dataBase.session.add(simulationKPI)
            self.logger.simulationRunDB.simulationKPI.append(simulationKPI)


        self.logger.dataBase.session.commit()