import csv
import math

from ProductionSimulation.database.models.TransporterDistribution import TransporterDistributionKPI, \
    TransporterDistributionTimeKPIValue, TransporterDistributionTimeKPI
from ProductionSimulation.logger.Enum_Logger import Logger_Enum
from ProductionSimulation.logger.SubLogger import SubLogger
from ProductionSimulation.logger.depreciated_logger.Logger2 import Logger
from ProductionSimulation.sim.Enum import Label
import pandas as pd


class TransporterDistributionLogger(SubLogger):
    """
    no kpi is getting calculated, is used for analysing the distribution of the transporter
    """

    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.current_number = {}
        self.current_sum = {}
        # TODO distance
        self.current_distance = {}
        self.location_from_to_list = []
        self.number_transport = {}

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        """

        self.type = log_type_dict[Logger_Enum.TransporterDistributionLogger.value]

        if (self.isNotLogging()):

            for key, value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)

            return

        transport_list = [transport for transport in
                          self.logger.simCore.onto.search(type=self.logger.simCore.central.transporter_class)]


        location_list = [queue.has_for_queue_location.__getitem__(0) for queue in
                         self.logger.simCore.central.queue_list if len(queue.has_for_queue_location) > 0]

        self.location_from_to_list = []
        for location in location_list:
            for location1 in location_list:
                self.location_from_to_list.append(location.name + " --> " + location1.name)

        if (not self.isNotLogging()):

            self.summarized_kpis['all'] = {}
            for location_string in self.location_from_to_list:
                self.summarized_kpis['all'][location_string] = 0

            for transport in transport_list:

                transport_name = transport.name
                self.summarized_kpis[transport_name] = {}
                self.current_number[transport_name] = 0
                self.current_sum[transport_name] = {}
                self.number_transport[transport_name] = 0

                for location_string in self.location_from_to_list:
                    self.current_sum[transport_name][location_string] = 0
                    self.summarized_kpis[transport_name][location_string] = 0

        if (self.isTimeLogging()):
            self.time_kpis['time'] = []
            self.time_kpis['all'] = {}

            for location_string in self.location_from_to_list:
                self.time_kpis['all'][location_string] = []

            for transport in transport_list:

                transport_name = transport.name
                self.time_kpis[transport_name] = {}

                for location_string in self.location_from_to_list:
                    self.time_kpis[transport_name][location_string] = []


    def addElement(self, dict_element):
        """
        interface to the logger, all data from the simulation are provided through this class

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        """
        dict_element = self.checkStartTimeLogging(dict_element)
        transport_onto_name = dict_element['transporter_name']
        time = dict_element['event_onto_time']
        from_name = dict_element['old_location']
        to_name = dict_element['new_location_name']
        if(self.isTimeLogging()):
            if len(self.time_kpis["time"]) < math.ceil(time / self.logger.time_intervall) - math.floor(
                    self.logger.start_time_logging / self.logger.time_intervall) - 1:
                self.evaluate(time)

        self.current_sum[transport_onto_name][from_name + " --> " + to_name] += 1
        self.summarized_kpis[transport_onto_name][from_name + " --> " + to_name] += 1
        self.number_transport[transport_onto_name] += 1
        self.current_number[transport_onto_name] += 1

    def evaluate(self, time):
        """
        summarizes all values in one time intervall

        :param time:
        """
        time_multiple = math.floor(time / self.logger.time_intervall)
        if(self.isTimeLogging()):
            self.time_kpis['time'].append((time_multiple - 1) * self.logger.time_intervall)

        for location_string in self.location_from_to_list:
            transport_sum = 0
            transport_count = 0
            for transport, location_dict in self.current_sum.items():

                if self.current_number[transport] != 0:
                    kpi_value = self.current_sum[transport][location_string] / self.current_number[transport]
                else:
                    kpi_value = 0
                if(self.isTimeLogging()):
                    self.time_kpis[transport][location_string].append(kpi_value)
                self.current_sum[transport][location_string] = 0
                transport_sum += kpi_value
                transport_count += 1
            if(self.isTimeLogging()):
                self.time_kpis['all'][location_string].append(transport_sum / transport_count)
            # self.kpi_dict['all'][location_string] = ((time_multiple - 1) * self.kpi_dict['all'][location_string] + transport_sum/transport_count) / time_multiple

        for transport, location_dict in self.current_sum.items():
            self.current_number[transport] = 0

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        """
        if(self.isSummaryLogging()):
            for location_string in self.location_from_to_list:
                sum = 0
                count = 0
                for transport, location_dict in self.current_sum.items():
                    sum += self.summarized_kpis[transport][location_string]

                    if(self.number_transport[transport]!=0):
                        self.summarized_kpis[transport][location_string] = self.summarized_kpis[transport][location_string] / \
                                                                       self.number_transport[transport]
                    else:
                        self.summarized_kpis[transport][location_string] = 0

                    count += self.number_transport[transport]
                if count!=0:
                    self.summarized_kpis['all'][location_string] = sum / count
                else:
                    self.summarized_kpis['all'][location_string] = 0

    def save_to_database(self):
        """
        save data to database
        :return:
        """

        if (self.isTimeLogging()):

            for key, value in self.time_kpis.items():
                if key != "time":

                    transporterDistributionTimeKPI = TransporterDistributionTimeKPI(name=key)

                    for i in range(0, len(self.time_kpis["time"])):

                        for k, v in self.time_kpis[key].items():

                            transporterDistributionTimeKPIvalue = TransporterDistributionTimeKPIValue(value=v[i], fromToLocation=k, time=self.time_kpis["time"][i])
                            transporterDistributionTimeKPI.transporterDistributionTimeKPIValue.append(transporterDistributionTimeKPIvalue)
                            self.logger.dataBase.session.add(transporterDistributionTimeKPIvalue)
                    self.logger.simulationRunDB.transporterDistributionTimeKPI.append(transporterDistributionTimeKPI)
                    self.logger.dataBase.session.add(transporterDistributionTimeKPI)


        if (self.isSummaryLogging()):

            for key, value in self.summarized_kpis.items():

                for k, v in self.summarized_kpis[key].items():

                    transporterDistributionKPI = TransporterDistributionKPI(name=key,fromToLocation=k,value = v)
                    self.logger.dataBase.session.add(transporterDistributionKPI)
                    self.logger.simulationRunDB.transporterDistributionKPI.append(transporterDistributionKPI)


        self.logger.dataBase.session.commit()