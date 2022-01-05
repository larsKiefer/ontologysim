import copy
import math

from ontologysim.ProductionSimulation.database.models.QueueKPI import QueueTimeKPI, QueueTimeKPIValue, QueueKPI
from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum
from ontologysim.ProductionSimulation.logger import SubLogger
from ontologysim.ProductionSimulation.sim.Enum import Label


class QueueFillLevelLogger(SubLogger.SubLogger):
    """
   calculates all queue fill level related kpi's
   """

    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.kpi_list = ["FillLevel"]

        self.current_size_blocked = {}
        self.current_time_blocked = {}
        self.kpi_current_time_slot_dict = {}

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        """
        self.type = log_type_dict[Logger_Enum.QueueFillLevelLogger.value]

        if (self.isNotLogging()):
            for key, value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)

            return

        queue_list = [queue for queue in self.logger.simCore.central.queue_list if
                      not Label.EndQueue.value in queue.name]

        
        self.last_time_intervall = math.floor(
            self.logger.simCore.getCurrentTimestep() / self.logger.time_intervall) * self.logger.time_intervall

        if (self.isTimeLogging()):
            self.time_kpis['time'] = []

            self.time_kpis['all'] = {}
            for kpi in self.kpi_list:
                self.time_kpis['all'][kpi] = []
            for queue in queue_list:
                queue_name = queue.name
                self.time_kpis[queue_name] = {}
                for kpi in self.kpi_list:
                    self.time_kpis[queue_name][kpi] = []

        if (not self.isNotLogging()):
            self.summarized_kpis['all'] = {}
            for kpi in self.kpi_list:
                self.summarized_kpis['all'][kpi] = []
            for queue in queue_list:
                queue_name = queue.name

                self.summarized_kpis[queue_name] = {}
                for kpi in self.kpi_list:
                    self.summarized_kpis[queue_name][kpi] = 0

        if (not self.isNotLogging()):
            for queue in queue_list:
                queue_name = queue.name
                self.current_size_blocked[queue_name] = 0
                self.current_time_blocked[queue_name] = 0
                self.kpi_current_time_slot_dict[queue_name] = {}
                for i in range(queue.size + 1):
                    self.kpi_current_time_slot_dict[queue_name][i] = 0

    def setQueueSize(self, time):
        """
        calculates the current number of parts in a queue

        :param time:
        :return:
        """
        if (self.isTimeLogging()):
            for key in self.current_time_blocked.keys():
                self.current_time_blocked[key] = time
                number_of_position = 0
                for position in self.logger.simCore.onto[key].has_for_position:
                    if position.blockedSpace == 1 and len(position.has_for_product) > 0:
                        number_of_position += 1
                self.current_size_blocked[key] = number_of_position

    def addElement(self, dict_element):
        """
        interface to the logger, all data from the simulation are provided through this class

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        """
        dict_element = self.checkStartTimeLogging(dict_element)
        queue_onto_name = dict_element['queue_name']
        time = dict_element['event_onto_time']
        old_queue_onto_name = dict_element['old_queue_name']
        old_current_size = dict_element['old_queue_current_size']
        current_size = dict_element['queue_current_size']

        if not Label.EndQueue.value in queue_onto_name:
            if(self.isTimeLogging()):
                if len(self.time_kpis["time"]) < math.ceil(time / self.logger.time_intervall) - math.floor(
                        self.logger.start_time_logging / self.logger.time_intervall) - 1:
                    self.evaluate(time)

            self.kpi_current_time_slot_dict[old_queue_onto_name][old_current_size + 1] += (time -
                                                                                           self.current_time_blocked[
                                                                                               old_queue_onto_name]) / self.logger.time_intervall
            self.kpi_current_time_slot_dict[queue_onto_name][current_size - 1] += (time - self.current_time_blocked[
                queue_onto_name]) / self.logger.time_intervall
            self.current_time_blocked[queue_onto_name] = time
            self.current_size_blocked[queue_onto_name] = current_size
            self.current_time_blocked[old_queue_onto_name] = time
            self.current_size_blocked[old_queue_onto_name] = old_current_size

    def evaluate(self, time):
        """
        calcualtes the kpi

        :param time:
        """
        if (not self.isNotLogging()):
            time_multiple = math.floor(time / self.logger.time_intervall)
            if (self.isTimeLogging()):
                self.time_kpis['time'].append((time_multiple - 1) * self.logger.time_intervall)

            count_queue = 0
            sum_queue = 0
            for queue, position_dict in self.kpi_current_time_slot_dict.items():

                time_diff = time_multiple * self.logger.time_intervall - self.current_time_blocked[queue]

                self.current_time_blocked[queue] = time_multiple * self.logger.time_intervall
                self.kpi_current_time_slot_dict[queue][
                    self.current_size_blocked[queue]] += time_diff / self.logger.time_intervall * self.current_size_blocked[queue]
                count = 0
                sum = 0
                count_queue += 1
                for position_number, kpi_value in position_dict.items():
                    count += 1
                    sum += kpi_value
                    self.kpi_current_time_slot_dict[queue][position_number] = 0
                if (self.isTimeLogging()):
                    self.time_kpis[queue]["FillLevel"].append(sum / count)
                if(self.isSummaryLogging()):
                    self.summarized_kpis[queue]["FillLevel"] += sum / count
                sum_queue += sum / count
            if(self.isTimeLogging()):
                self.time_kpis['all']["FillLevel"].append(sum_queue / count_queue)

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        """
        queue_list = [queue for queue in self.logger.simCore.central.queue_list if
                      not Label.EndQueue.value in queue.name]

        self.evaluate(time + self.logger.time_intervall)

        if (self.isSummaryLogging()):
            sum = 0
            count = 0
            for queue, position_dict in self.kpi_current_time_slot_dict.items():
                self.summarized_kpis[queue]["FillLevel"] = self.summarized_kpis[queue]['FillLevel'] / (
                            time - self.logger.start_time_logging) * self.logger.time_intervall
                sum += self.summarized_kpis[queue]["FillLevel"]
                count += 1

            self.summarized_kpis['all']["FillLevel"] = sum / count

    def finale_evaluate_summary_api(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        """
        queue_list = [queue for queue in self.logger.simCore.central.queue_list if
                      not Label.EndQueue.value in queue.name]

        summarized_data = copy.deepcopy(self.summarized_kpis)
        kpiCurrentTimeSlot = copy.deepcopy(self.kpi_current_time_slot_dict)
        current_time_blocked = copy.deepcopy(self.current_time_blocked)
        current_size_blocked = copy.deepcopy(self.current_size_blocked)

        self.evaluate(time + self.logger.time_intervall)

        if (not self.isNotLogging()):
            time_multiple = math.floor(time / self.logger.time_intervall)

            count_queue = 0
            sum_queue = 0
            for queue, position_dict in kpiCurrentTimeSlot.items():

                time_diff = time_multiple * self.logger.time_intervall - current_time_blocked[queue]

                current_time_blocked[queue] = time_multiple * self.logger.time_intervall
                kpiCurrentTimeSlot[queue][
                    current_size_blocked[queue]] += time_diff / self.logger.time_intervall * current_size_blocked[queue]
                count = 0
                sum = 0
                count_queue += 1
                for position_number, kpi_value in position_dict.items():
                    count += 1
                    sum += kpi_value
                    kpiCurrentTimeSlot[queue][position_number] = 0


                summarized_data[queue]["FillLevel"] += sum / count
                sum_queue += sum / count



            sum = 0
            count = 0
            for queue, position_dict in kpiCurrentTimeSlot.items():
                summarized_data[queue]["FillLevel"] = summarized_data[queue]['FillLevel'] / (
                            time - self.logger.start_time_logging) * self.logger.time_intervall
                sum += summarized_data[queue]["FillLevel"]
                count += 1

            summarized_data['all']["FillLevel"] = sum / count

        return summarized_data

    def save_to_database(self):
        """
        save to database
        :return:
        """

        if (self.isTimeLogging()):

            for key, value in self.time_kpis.items():
                if key != "time":

                    queueTimeKPI = QueueTimeKPI(name=key)

                    for i in range(0, len(self.time_kpis["time"])):
                        input = {}
                        for k, v in self.time_kpis[key].items():
                            input[k] = v[i]

                        queueTimeKPIvalue = QueueTimeKPIValue(**input, time=self.time_kpis["time"][i])
                        queueTimeKPI.queueTimeKPIValue.append(queueTimeKPIvalue)
                        self.logger.dataBase.session.add(queueTimeKPIvalue)
                    self.logger.simulationRunDB.queueTimeKPI.append(queueTimeKPI)
                    self.logger.dataBase.session.add(queueTimeKPI)


        if (self.isSummaryLogging()):

            for key, value in self.summarized_kpis.items():

                queueKPI = QueueKPI(name=key,**self.summarized_kpis[key])
                self.logger.dataBase.session.add(queueKPI)
                self.logger.simulationRunDB.queueKPI.append(queueKPI)


        self.logger.dataBase.session.commit()
