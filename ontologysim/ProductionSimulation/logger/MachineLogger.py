import math

from ontologysim.ProductionSimulation.database.models.MachineKPI import MachineTimeKPI, MachineTimeKPIValue, MachineKPI
from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum
from ontologysim.ProductionSimulation.logger import SubLogger
from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Queue_Enum
import copy

class MachineLogger(SubLogger.SubLogger):
    """
    calculates all machine related kpi's
    """

    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.kpi_list = ["TTFp", "TTRp", "FE", "CMTp", "AUITp", "AUBTp", "ADOTp", "AUSTp", "APTp", "AUPTp", "AUSTTp","PBTp", "AUBLTp","PRIp"]

        self.basic_kpi_list = ["A", "AE", "TE", "UE", "SeRp","E","OEE","NEE"]

        self.last_value = {}
        self.number_of_machines = 0

           
        #Time to failure (TTF):
        #   The actual time during which a machine is able to produce, starting from the completion of
        #  the repair and ending at a new failure. Such element is also referred to as Time between failure (TBF)

        #   Time to repair (TTR):
        #       The actual time during which a machine is unavailable due to a failure, i.e. under repair.

        #  Failure event (FE):
        #       The count over a specified time interval of the terminations of the ability for a machine to
        #       perform a required operation.

        #  Corrective maintenance time (CMT):
        #       The part of maintenance time during which corrective maintenance is performed
        #       on a machine.

        #  Actual unit processing time (AUPT):
        #      The time necessary for production and setup on a machine for an order.
        #  Actual production time (APT):
        #      The actual time in which the machine is producing for an order, which only includes
        #       the value-adding functions.
        #  Actual unit setup time (AUST):
        #      The time used for the preparation, i.e. setup, of an order on a machine.
        #      Thus, the following relationship is observed:

        #   Actual unit down time (ADOT):
        #      The actual time in which the production process is delayed due to malfunction-caused
        #      interruptions, minor stoppages, and other unplanned events.
        #   Actual unit idle time (AUIT):
        #      The actual time when the machine is not executing order production even if it is
        #      available. This can also be referred to as actual unit delay time (ADET).
    
        #   Actual unit busy time (AUBT):
        #       The actual time that a machine is used for the execution of a production order.
    
        #   Actual unit starviation time (AUSTT):
        #   Actural unit bloccking time (AUBLT):
    
        #   Availability (A):
        #         The percentage of actual time a machine is available, i.e. the APT among the PBT for a machine.
        #         It represents the portion of time used for processing compared to the total time that includes AUST, delay time and
        #         down time.
    
        #   Allocation efficiency (AE):
        #      The actual usage and availability of the planned capacity of amachine, which ismeasured
        #      by the ratio of AUBT to planned unit busy time (PBT). The complementary part is the percentage of actual unit
        #      downtime.
    
        #   Technical efficiency (TE):
        #        The efficiency of production vs. malfunction-caused interruptions. It represents the
        #         relationship between APT and the sum of APT and ADOT that includes times of malfunction-caused interruptions.
            
        #    Worker efficiency (WE):
        #        The efficiency of aworker’s attendance in production, measured by the relationship between
        #         the actual personnel’s work time (APWT) related to production orders and the actual personnel’s attendance time
        #        (APAT).
    
        #    Utilization efficiency (UE):
        #       The productivity of a machine, measured by the ratio between the APT and the AUBT.
        #       If the actual unit delay time and setup time are high, the UE will be low.
    
       #     Effectiveness (E):
       #          How effective a machine can be during the production time, measured by the ratio of planned
       #          target cycle time (represented as planned runtime per item (PRI)) to actual cycle time (expressed asAPT divided by
       #          produced quantity (PQ)).
    
       #     Setup ratio (SeR):
       #         The relative loss of value adding opportunity for a machine due to setup, measured by the ratio
       #         of AUST to AUPT. The complementary proportion is the APT.
    
       #     Allocation ratio (AR):
       #         The percentage of actual busy time of allmachines (AU BT ) among theAOETof a production
       #         order. The complementary proportion describes the ratio of actual queuing and transportation time.
    
       #     Production process ratio (PR):
       #         The efficiency of production when considering the actual unit setup time, delay time,
       #         transportation time, and queuing time. It is the ratio between theAPT over all work units and work centers involved
       #         in a production order and the whole throughput time of a production order which is the AOET.

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        """
        self.type=log_type_dict[Logger_Enum.MachineLogger.value]


        if(self.isNotLogging()):

            for key,value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)

            return

        machine_list = [machine for machine in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)]
        self.number_of_machines = len(machine_list)
        self.number_of_instances = len(machine_list)

        if(not self.isNotLogging()):
            self.summarized_kpis['all'] = {}
            for kpi in self.kpi_list:
                self.summarized_kpis['all'][kpi] = 0

            for machine in machine_list:
                machine_name = machine.name
                self.summarized_kpis[machine_name] = {}

                for kpi in self.kpi_list:
                    self.summarized_kpis[machine_name][kpi] = 0

                for kpi in self.basic_kpi_list:
                    self.summarized_kpis[machine_name][kpi] = 0

        if (self.isTimeLogging() ):
            self.time_kpis['time'] = []
            self.time_kpis['all'] = {}
            for kpi in self.kpi_list:
                self.time_kpis['all'][kpi] = []

            for kpi in self.basic_kpi_list:
                self.time_kpis["all"][kpi] = []

            for machine in machine_list:
                machine_name = machine.name
                self.time_kpis[machine_name] = {}
                for kpi in self.kpi_list:
                    self.time_kpis[machine_name][kpi] = []

                for kpi in self.basic_kpi_list:
                    self.time_kpis[machine_name][kpi] = []

        if (not self.isNotLogging()):
            for machine in machine_list:
                machine_name = machine.name
                self.last_value[machine_name] = {}
                for kpi in self.kpi_list:
                    # self.kpi_current_time_slot_dict[machine_name][e.value] = 0
                    self.last_value[machine_name][kpi] = 0

                self.last_value[machine_name]["TTF"] = self.logger.simCore.getCurrentTimestep()

    def setTTFlastValue(self, start_logging_time):
        """
        set the last failure value to the last value dict

        :param start_logging_time:
        """
        if (not self.isNotLogging() ):
            machine_list = [machine.name for machine in
                            self.logger.simCore.central.machine_list]
            for machine_name in machine_list:
                self.last_value[machine_name]["TTFp"] = start_logging_time

    def update_basic_kpis(self):
        """
        calculates the basic kpi's
        """

        if(self.isTimeLogging()):

            machine_list = [machine.name for machine in
                            self.logger.simCore.central.machine_list]
            pbt = self.logger.time_intervall

            for update_index in list(set(self.update_list)):
                self.time_kpis["all"]["TE"][update_index] = 0
                self.time_kpis["all"]["UE"][update_index] = 0
                self.time_kpis["all"]["SeRp"][update_index] = 0
                self.time_kpis["all"]["A"][update_index] = 0
                self.time_kpis["all"]["AE"][update_index] = 0
                self.time_kpis["all"]["AUBTp"][update_index] = 0
                self.time_kpis["all"]["E"][update_index] = 0
                self.time_kpis["all"]["OEE"][update_index] = 0
                self.time_kpis["all"]["NEE"][update_index] = 0

                for machine_name in machine_list:

                    self.time_kpis[machine_name]["AUBTp"][update_index] = self.time_kpis[machine_name]["AUPTp"][
                                                                             update_index] + \
                                                                         self.time_kpis[machine_name]["ADOTp"][update_index]
                    self.time_kpis[machine_name]["A"][update_index] = self.time_kpis[machine_name]["APTp"][
                                                                          update_index] / pbt * pbt
                    self.time_kpis[machine_name]["AE"][update_index] = self.time_kpis[machine_name]["AUBTp"][
                                                                           update_index] / pbt * pbt
                    self.time_kpis["all"]["AE"][update_index] += self.time_kpis[machine_name]["AE"][
                                                                     update_index] / self.number_of_instances
                    self.time_kpis["all"]["A"][update_index] += self.time_kpis[machine_name]["A"][
                                                                    update_index] / self.number_of_instances
                    self.time_kpis["all"]["AUBTp"][update_index] += self.time_kpis[machine_name]["AUBTp"][
                                                                       update_index] / self.number_of_instances
                    if (self.time_kpis[machine_name]["APTp"][update_index] + self.time_kpis[machine_name]["ADOTp"][
                        update_index]) > 0:
                        self.time_kpis[machine_name]["TE"][update_index] = self.time_kpis[machine_name]["APTp"][
                                                                               update_index] / (
                                                                                   self.time_kpis[machine_name]["APTp"][
                                                                                       update_index] +
                                                                                   self.time_kpis[machine_name]["ADOTp"][
                                                                                       update_index])
                        self.time_kpis["all"]["TE"][update_index] += self.time_kpis[machine_name]["TE"][
                                                                         update_index] / self.number_of_instances

                        self.time_kpis[machine_name]["E"][update_index] = self.time_kpis[machine_name]["PRIp"][
                                                                               update_index]/self.time_kpis[machine_name]["APTp"][
                                                                               update_index]
                        self.time_kpis["all"]["E"][update_index] += self.time_kpis[machine_name]["E"][update_index] / self.number_of_instances

                        self.time_kpis[machine_name]["OEE"][update_index] = self.time_kpis[machine_name]["A"][
                                                                              update_index] * \
                                                                          self.time_kpis[machine_name]["E"][
                                                                              update_index]
                        self.time_kpis["all"]["OEE"][update_index] += self.time_kpis[machine_name]["OEE"][
                                                                        update_index] / self.number_of_instances

                    if self.time_kpis[machine_name]["AUBTp"][update_index] > 0:
                        self.time_kpis[machine_name]["UE"][update_index] = self.time_kpis[machine_name]["APTp"][
                                                                               update_index] / \
                                                                           self.time_kpis[machine_name]["AUBTp"][
                                                                               update_index]
                        self.time_kpis["all"]["UE"][update_index] += self.time_kpis[machine_name]["UE"][
                                                                         update_index] / self.number_of_instances
                    if self.time_kpis[machine_name]["AUPTp"][update_index] > 0:
                        self.time_kpis[machine_name]["SeRp"][update_index] = self.time_kpis[machine_name]["AUSTp"][
                                                                                update_index] / \
                                                                            self.time_kpis[machine_name]["AUPTp"][
                                                                                update_index]
                        self.time_kpis["all"]["SeRp"][update_index] += self.time_kpis[machine_name]["SeRp"][
                                                                          update_index] / self.number_of_instances

                    if self.time_kpis[machine_name]["PBTp"][update_index] > 0:
                        self.time_kpis[machine_name]["NEE"][update_index] = self.time_kpis[machine_name]["AUPTp"][
                                                                                 update_index] / \
                                                                             self.time_kpis[machine_name]["PBTp"][
                                                                                 update_index] * self.time_kpis[machine_name]["E"][update_index]
                        self.time_kpis["all"]["NEE"][update_index] += self.time_kpis[machine_name]["NEE"][
                                                                           update_index] / self.number_of_instances

            self.logger.simLogger.update_list.extend([update_index for update_index in list(set(self.update_list))])
            self.update_list = []

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
                self.addNewTimeElement([machine.name for machine in
                                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                       self.kpi_list, time)
                self.addNewTimeElement([machine.name for machine in
                                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                       self.basic_kpi_list, time)
                time_multiple = math.floor(time / self.logger.time_intervall)
                time_len = len(self.time_kpis['time'])
                for i in range(time_index - time_len, -1, -1):
                    self.time_kpis["time"].append((time_multiple - i) * self.logger.time_intervall)

                machine_list = [machine.name for machine in
                                self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)]

                # print(time,self.logger.start_time_logging, self.time_kpis["time"])

                self.update_basic_kpis()
                self.logger.simLogger.machine_update = True
                self.logger.simLogger.update_basic_kpis()

        if event_type == Machine_Enum.Defect.value:
            machine_name = dict_element['machine_name']
            repair_time = dict_element['repair_time']
            triggered_defect_time = dict_element['triggered_defect_time']
            time = dict_element['event_onto_time']
            if(self.isSummaryLogging()):
                self.summarized_kpis[machine_name]['FE'] += 1
                self.summarized_kpis[machine_name]["TTFp"] += triggered_defect_time - self.last_value[machine_name]["TTFp"]
                self.summarized_kpis[machine_name]["TTRp"] += time - triggered_defect_time
                self.summarized_kpis[machine_name]["PBTp"] += time - triggered_defect_time
                self.summarized_kpis[machine_name]["CMTp"] += repair_time
                self.summarized_kpis[machine_name]["ADOTp"] = self.summarized_kpis[machine_name]["TTRp"]
            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["TTFp"], triggered_defect_time,
                                    triggered_defect_time - self.last_value[machine_name]["TTFp"])
                self.addTimeElement(machine_name, ["TTRp","PBTp"], time, time - triggered_defect_time)
                self.addTimeElement(machine_name, ["CMTp"], time, repair_time)
                self.addTimeSumElement(machine_name, ["FE"], time, time - triggered_defect_time)

            self.last_value[machine_name]["TTFp"] = time


        elif event_type == Machine_Enum.SetUp.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            machine_name = dict_element['machine_name']
            time_diff = dict_element['time_diff']
            time = dict_element['event_onto_time']
            if (self.isSummaryLogging()):
                self.summarized_kpis[machine_name]["AUSTp"] += time_diff
                self.summarized_kpis[machine_name]["AUPTp"] += time_diff
                self.summarized_kpis[machine_name]["PBTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["AUSTp", "AUPTp","PBTp"], time, time_diff)

        elif event_type == Machine_Enum.Process.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            machine_name = dict_element['machine_name']
            time_diff = dict_element['time_diff']
            time = dict_element['event_onto_time']
            meanProcessTime=dict_element['meanProcessTime']
            if (self.isSummaryLogging()):
                self.summarized_kpis[machine_name]["PRIp"] += meanProcessTime
                self.summarized_kpis[machine_name]["APTp"] += time_diff
                self.summarized_kpis[machine_name]["AUPTp"] += time_diff
                self.summarized_kpis[machine_name]["PBTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["APTp", "AUPTp","PBTp"], time, time_diff)
                self.addTimeElement(machine_name, ["PRIp"], time, meanProcessTime)


        elif event_type == Queue_Enum.StartProcess.value or event_type == Queue_Enum.StartProcessStayBlocked.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            queue_name = dict_element["queue_name"]
            time = dict_element['event_onto_time']
            machine_name = self.logger.simCore.central.queue_to_machine[queue_name]
            if (self.isSummaryLogging()):
                self.summarized_kpis[machine_name]["AUSTp"] += time_diff
                self.summarized_kpis[machine_name]["AUPTp"] += time_diff
                self.summarized_kpis[machine_name]["PBTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["AUSTp", "AUPTp","PBTp"], time, time_diff)

        elif event_type == Queue_Enum.EndProcess.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            old_queue_name = dict_element["old_queue_name"]
            time = dict_element['event_onto_time']
            machine_name = self.logger.simCore.central.queue_to_machine[old_queue_name]
            if (self.isSummaryLogging()):
                self.summarized_kpis[machine_name]["AUSTp"] += time_diff
                self.summarized_kpis[machine_name]["AUPTp"] += time_diff
                self.summarized_kpis[machine_name]["PBTp"] += time_diff
            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["AUSTp", "AUPTp","PBTp"], time, time_diff)

        elif event_type == Machine_Enum.Wait.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            machine_name = dict_element['machine_name']
            time = dict_element['event_onto_time']
            input_queue_current_size = dict_element['input_queue_current_size']
            output_queue_current_size = dict_element['output_queue_current_size']

            if (self.isSummaryLogging()):
                self.summarized_kpis[machine_name]['AUITp'] += time_diff
                self.summarized_kpis[machine_name]["PBTp"] += time_diff
                if input_queue_current_size == 0:
                    self.summarized_kpis[machine_name]["AUSTTp"] += time_diff
                elif output_queue_current_size == 1:
                    self.summarized_kpis[machine_name]["AUBTp"] += time_diff
                else:
                    self.summarized_kpis[machine_name]["AUSTTp"] += time_diff

            if (self.isTimeLogging()):
                self.addTimeElement(machine_name, ["AUITp","PBTp"], time, time_diff)
                if input_queue_current_size == 0:
                    self.addTimeElement(machine_name, ["AUSTTp"], time, time_diff)
                elif output_queue_current_size == 1:
                    self.addTimeElement(machine_name, ["AUBTp"], time, time_diff)
                else:
                    self.addTimeElement(machine_name, ["AUSTTp"], time, time_diff)


    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """


        if(not self.isNotLogging()):
            last_time_element=int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)
            if(self.isTimeLogging()):
                if(len(self.time_kpis["time"])<=last_time_element):
                    self.addNewTimeElement([machine.name for machine in
                                            self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                           self.kpi_list, time)
                    self.addNewTimeElement([machine.name for machine in
                                            self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                           self.basic_kpi_list, time)
                #print(last_time_element,time,len(self.update_list),self.start_logging_multiple,self.logger.time_intervall)

            self.update_list.append(last_time_element)

            self.update_basic_kpis()
            self.logger.simLogger.machine_update = True
            self.logger.simLogger.update_basic_kpis()

            machine_list = [machine.name for machine in
                            self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)]
            number_of_machines = len(machine_list)
            self.pbt = time - self.logger.start_time_logging

            if(self.isSummaryLogging()):
                for machine_name in machine_list:
                    self.summarized_kpis[machine_name]["ADOTp"] = self.summarized_kpis[machine_name]["TTRp"]
                    self.summarized_kpis[machine_name]["AUBTp"] = self.summarized_kpis[machine_name]["AUPTp"] + \
                                                                 self.summarized_kpis[machine_name]["ADOTp"]
                    self.summarized_kpis[machine_name]["TTFp"] += time - self.last_value[machine_name]["TTFp"]

                    for k1, v1 in self.summarized_kpis['all'].items():

                        self.summarized_kpis['all'][k1] += self.summarized_kpis[machine_name][k1]
                        if k1 != 'FE' and k1 in self.kpi_list:
                            self.summarized_kpis[machine_name][k1] /= self.pbt

            if(self.isTimeLogging()):
                for machine_name in machine_list:
                    self.addTimeElement(machine_name, ["TTFp"], time, time - self.last_value[machine_name]["TTFp"])
                for k, v in self.summarized_kpis.items():
                    self.time_kpis[k]["ADOTp"] = self.time_kpis[k]["TTRp"]
                    self.time_kpis[k]["AUBTp"] = self.time_kpis[k]["AUPTp"] + \
                                                self.time_kpis[k]["ADOTp"]

            if(self.isSummaryLogging()):
                # additional_kpis
                self.summarized_kpis['all']["A"] = 0
                self.summarized_kpis['all']["AE"] = 0
                self.summarized_kpis['all']["TE"] = 0
                self.summarized_kpis['all']["UE"] = 0
                self.summarized_kpis['all']["SeRp"] = 0
                self.summarized_kpis['all']["E"] = 0
                self.summarized_kpis['all']["OEE"] = 0
                self.summarized_kpis['all']["NEE"] = 0

                for machine_name in machine_list:
                    self.summarized_kpis[machine_name]["A"] = self.summarized_kpis[machine_name][
                                                                  "APTp"] / self.pbt * self.pbt
                    self.summarized_kpis[machine_name]["AE"] = self.summarized_kpis[machine_name][
                                                                   "AUBTp"] / self.pbt * self.pbt

                    if self.summarized_kpis[machine_name]["APTp"] > 0:
                        self.summarized_kpis[machine_name]["E"] = self.summarized_kpis[machine_name]["PRIp"] / \
                                                                  self.summarized_kpis[machine_name]["APTp"]

                        self.summarized_kpis[machine_name]["OEE"] = self.summarized_kpis[machine_name]["A"] * \
                                                                    self.summarized_kpis[machine_name]["E"]

                    if self.summarized_kpis[machine_name]["PBTp"] > 0:
                        self.summarized_kpis[machine_name]["NEE"] = self.summarized_kpis[machine_name]["AUPTp"] / \
                                                                    self.summarized_kpis[machine_name]["PBTp"] * \
                                                                    self.summarized_kpis[machine_name]["E"]

                    if self.summarized_kpis[machine_name]["APTp"] + self.summarized_kpis[machine_name]["ADOTp"] > 0:
                        self.summarized_kpis[machine_name]["TE"] = self.summarized_kpis[machine_name]["APTp"] / (
                                self.summarized_kpis[machine_name]["APTp"] + self.summarized_kpis[machine_name][
                            "ADOTp"])
                    else:
                        self.summarized_kpis[machine_name]["TE"] = 0
                    if self.summarized_kpis[machine_name]["AUBTp"] > 0:
                        self.summarized_kpis[machine_name]["UE"] = self.summarized_kpis[machine_name]["APTp"] / \
                                                                   self.summarized_kpis[machine_name]["AUBTp"]
                    else:
                        self.summarized_kpis[machine_name]["UE"] = 0

                    if self.summarized_kpis[machine_name]["AUPTp"] > 0:
                        self.summarized_kpis[machine_name]["SeRp"] = self.summarized_kpis[machine_name]["AUSTp"] / \
                                                                     self.summarized_kpis[machine_name]["AUPTp"]

                    else:
                        self.summarized_kpis[machine_name]["SeRp"] = 0

                    self.summarized_kpis['all']["A"] += self.summarized_kpis[machine_name]["A"]
                    self.summarized_kpis['all']["AE"] += self.summarized_kpis[machine_name]["AE"]
                    self.summarized_kpis['all']["TE"] += self.summarized_kpis[machine_name]["TE"]
                    self.summarized_kpis['all']["UE"] += self.summarized_kpis[machine_name]["UE"]
                    self.summarized_kpis['all']["SeRp"] += self.summarized_kpis[machine_name]["SeRp"]
                    self.summarized_kpis['all']["E"] += self.summarized_kpis[machine_name]["E"]
                    self.summarized_kpis['all']["OEE"] += self.summarized_kpis[machine_name]["OEE"]
                    self.summarized_kpis['all']["NEE"] += self.summarized_kpis[machine_name]["NEE"]

                for k1, v1 in self.summarized_kpis['all'].items():

                    if k1 != 'FE' and k1 in self.kpi_list:
                        self.summarized_kpis['all'][k1] /= self.pbt

                    self.summarized_kpis['all'][k1] /= number_of_machines

    def save_to_database(self):
        """
        save data to database
        :return:
        """
        machine_list = [machine.name for machine in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)]

        if (self.isTimeLogging()):
            machineTimeKPI = MachineTimeKPI(name='all')

            for i in range(0, len(self.time_kpis["time"])):
                input = {}
                for key, value in self.time_kpis["all"].items():
                    input[key] = value[i]

                machineTimeKPIvalue = MachineTimeKPIValue(**input,time=self.time_kpis["time"][i])
                machineTimeKPI.machineTimeKPIValue.append(machineTimeKPIvalue)
                self.logger.dataBase.session.add(machineTimeKPIvalue)

            self.logger.simulationRunDB.machineTimeKPI.append(machineTimeKPI)
            self.logger.dataBase.session.add(machineTimeKPI)

            for machine in machine_list:

                machineTimeKPI = MachineTimeKPI(name=machine)

                for i in range(0, len(self.time_kpis["time"])):
                    input = {}
                    for key, value in self.time_kpis[machine].items():
                        input[key] = value[i]

                    machineTimeKPIvalue = MachineTimeKPIValue(**input,time=self.time_kpis["time"][i])
                    machineTimeKPI.machineTimeKPIValue.append(machineTimeKPIvalue)
                    self.logger.dataBase.session.add(machineTimeKPIvalue)
                self.logger.simulationRunDB.machineTimeKPI.append(machineTimeKPI)
                self.logger.dataBase.session.add(machineTimeKPI)


        if (self.isSummaryLogging()):

            machineKPI = MachineKPI(name="all",**self.summarized_kpis['all'])
            self.logger.dataBase.session.add(machineKPI)
            self.logger.simulationRunDB.machineKPI.append(machineKPI)

            for machine in machine_list:
                machineKPI = MachineKPI(name=machine, **self.summarized_kpis[machine])
                self.logger.simulationRunDB.machineKPI.append(machineKPI)
                self.logger.dataBase.session.add(machineKPI)

        self.logger.dataBase.session.commit()

    def finale_evaluate_summary_api(self,time):
        """
        finale evaluate summary report for api
        :param time: int
        :return: list
        """
        machine_list = [machine.name for machine in
                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)]
        number_of_machines = len(machine_list)
        self.pbt = time - self.logger.start_time_logging


        summarized_data = copy.deepcopy(self.summarized_kpis)


        for machine_name in machine_list:
            summarized_data[machine_name]["ADOTp"] = summarized_data[machine_name]["TTRp"]
            summarized_data[machine_name]["AUBTp"] = summarized_data[machine_name]["AUPTp"] + \
                                                          summarized_data[machine_name]["ADOTp"]
            summarized_data[machine_name]["TTFp"] += time - self.last_value[machine_name]["TTFp"]

            for k1, v1 in summarized_data['all'].items():

                summarized_data['all'][k1] += summarized_data[machine_name][k1]
                if k1 != 'FE' and k1 in self.kpi_list:
                    summarized_data[machine_name][k1] /= self.pbt

        summarized_data['all']["A"] = 0
        summarized_data['all']["AE"] = 0
        summarized_data['all']["TE"] = 0
        summarized_data['all']["UE"] = 0
        summarized_data['all']["SeRp"] = 0
        summarized_data['all']["E"] = 0
        summarized_data['all']["OEE"] = 0
        summarized_data['all']["NEE"] = 0

        for machine_name in machine_list:
            summarized_data[machine_name]["A"] = summarized_data[machine_name][
                                                          "APTp"] / self.pbt * self.pbt
            summarized_data[machine_name]["AE"] = summarized_data[machine_name][
                                                           "AUBTp"] / self.pbt * self.pbt

            if summarized_data[machine_name]["APTp"] > 0:
                summarized_data[machine_name]["E"] = summarized_data[machine_name]["PRIp"] / \
                                                          summarized_data[machine_name]["APTp"]

                summarized_data[machine_name]["OEE"] = summarized_data[machine_name]["A"] * \
                                                            summarized_data[machine_name]["E"]

            if summarized_data[machine_name]["PBTp"] > 0:
                summarized_data[machine_name]["NEE"] = summarized_data[machine_name]["AUPTp"] / \
                                                            summarized_data[machine_name]["PBTp"] * \
                                                            summarized_data[machine_name]["E"]

            if summarized_data[machine_name]["APTp"] + summarized_data[machine_name]["ADOTp"] > 0:
                summarized_data[machine_name]["TE"] = summarized_data[machine_name]["APTp"] / (
                        summarized_data[machine_name]["APTp"] + summarized_data[machine_name][
                    "ADOTp"])
            else:
                summarized_data[machine_name]["TE"] = 0
            if summarized_data[machine_name]["AUBTp"] > 0:
                summarized_data[machine_name]["UE"] = summarized_data[machine_name]["APTp"] / \
                                                           summarized_data[machine_name]["AUBTp"]
            else:
                summarized_data[machine_name]["UE"] = 0

            if summarized_data[machine_name]["AUPTp"] > 0:
                summarized_data[machine_name]["SeRp"] = summarized_data[machine_name]["AUSTp"] / \
                                                             summarized_data[machine_name]["AUPTp"]

            else:
                summarized_data[machine_name]["SeRp"] = 0

            summarized_data['all']["A"] += summarized_data[machine_name]["A"]
            summarized_data['all']["AE"] += summarized_data[machine_name]["AE"]
            summarized_data['all']["TE"] += summarized_data[machine_name]["TE"]
            summarized_data['all']["UE"] += summarized_data[machine_name]["UE"]
            summarized_data['all']["SeRp"] += summarized_data[machine_name]["SeRp"]
            summarized_data['all']["E"] += summarized_data[machine_name]["E"]
            summarized_data['all']["OEE"] += summarized_data[machine_name]["OEE"]
            summarized_data['all']["NEE"] += summarized_data[machine_name]["NEE"]

        for k1, v1 in summarized_data['all'].items():

            if k1 != 'FE' and k1 in self.kpi_list:
                summarized_data['all'][k1] /= self.pbt

            summarized_data['all'][k1] /= number_of_machines


        return summarized_data

