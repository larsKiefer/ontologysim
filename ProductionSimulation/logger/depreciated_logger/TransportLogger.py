import csv
import math

from ProductionSimulation.logger.depreciated_logger.Logger2 import Logger
from ProductionSimulation.sim.Enum import Label
import pandas as pd


class TransporterLogger(Logger):
    """

    """
    def __init__(self, transport,simCore):
        super().__init__(simCore)
        self.tranpsort =transport

        self.current_number = {}
        self.current_sum = {}
        #tod_0 distance
        self.current_distance = {}
        self.location_from_to_list = []
        self.number_transport={}


    def init_dict(self):
        """

        """
        transport_list = [transport for transport in
                      self.tranpsort.simCore.onto.search(type=self.tranpsort.simCore.central.transporter_class) ]
        #tod_o programm start queue len(queue.is_transp_queue_of)==0 and
        location_list = [queue.has_for_queue_location.__getitem__(0) for queue in self.tranpsort.simCore.central.queue_list   if len(queue.has_for_queue_location)>0]

        self.location_from_to_list=[]
        for location in location_list:
            for location1 in location_list:
                self.location_from_to_list.append(location.name + " --> " + location1.name)

        self.kpi_time_dict['time'] = []
        self.kpi_time_dict['all'] = {}
        self.kpi_dict['all'] = {}
        for location_string in self.location_from_to_list:
            self.kpi_dict['all'][location_string] = 0
            self.kpi_time_dict['all'][location_string] = []

        for transport in transport_list:

            transport_name = transport.name
            self.kpi_time_dict[transport_name] = {}
            self.kpi_dict[transport_name] = {}
            self.current_number[transport_name] = 0
            self.current_sum[transport_name] = {}
            self.number_transport[transport_name] =0

            for location_string in self.location_from_to_list:
                self.current_sum[transport_name][location_string]=0
                self.kpi_time_dict[transport_name][location_string] = []
                self.kpi_dict[transport_name][location_string]=0

    def add_element(self, transport_onto_name, time, from_name,to_name):
        """

        :param transport_onto_name:
        :param time:
        :param from_name:
        :param to_name:
        """
        if time >= self.last_time_intervall + self.time_intervall:
            self.evaluate(time)

        self.current_sum[transport_onto_name][from_name + " --> " + to_name]+=1
        self.current_number[transport_onto_name]+=1


    def evaluate(self, time):
        """

        :param time:
        """
        time_multiple = math.floor(time / self.time_intervall)
        self.kpi_time_dict['time'].append(time_multiple * self.time_intervall)

        for location_string in self.location_from_to_list:
            transport_sum = 0
            transport_count = 0
            for transport, location_dict in self.current_sum.items():

                if self.current_number[transport]!=0:
                    kpi_value=self.current_sum[transport][location_string]/self.current_number[transport]
                else:
                    kpi_value=0

                self.kpi_time_dict[transport][location_string].append(kpi_value)
                self.kpi_dict[transport][location_string]+=kpi_value
                self.current_sum[transport][location_string]=0
                self.number_transport[transport]+=self.current_number[transport]
                transport_sum+=kpi_value
                transport_count+=1

            self.kpi_time_dict['all'][location_string].append(transport_sum/transport_count)
            #self.kpi_dict['all'][location_string] = ((time_multiple - 1) * self.kpi_dict['all'][location_string] + transport_sum/transport_count) / time_multiple
        self.last_time_intervall += self.time_intervall
        for transport, location_dict in self.current_sum.items():
            self.current_number[transport] = 0

    def finale_evaluate(self,time):
        """

        :param time:
        """
        for location_string in self.location_from_to_list:
            sum = 0
            count = 0
            for transport, location_dict in self.current_sum.items():
                self.kpi_dict[transport][location_string] = self.kpi_dict[transport][location_string] / self.number_transport[transport]
                sum+=self.kpi_dict[transport][location_string]
                count+=self.number_transport[transport]
            self.kpi_dict['all'][location_string]=sum/count

    def save_to_csv(self, type):
        """

        :param type:
        """
        with open(self.path_csv, type, newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            header = ['time']
            header.extend(
                [str(transport) + " " + str(location) for transport, time_dict in self.kpi_dict.items() for location, time in
                 time_dict.items()])

            wr.writerow(header)
            erg_list = []
            for i in range(len(self.kpi_time_dict['time'])):
                erg = [self.kpi_time_dict['time'][i]]

                erg.extend([self.kpi_time_dict[transport][location][i] for transport, time_dict in self.kpi_dict.items() for
                            location, time in time_dict.items()])

                erg_list.append(erg)

            wr.writerows(erg_list)

    def save(self):
        """

        """
        if "database" in self.type:
            self.simCore.data_base.createSchema_log()
            self.simCore.data_base.createTable_TransportTimeLog()
            self.simCore.data_base.createTable_TransportLog()
            self.insert_db()
        if "csv" in self.type:
            self.save_to_csv("w")

    def insert_db(self):
        """

        """
        schema_name = "log"
        table_name = "transport"
        columns = "transportID,kpi_value,type,run_id"
        insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                        """ VALUES  """
        len_dict = len(self.kpi_dict)
        len_sub_dict = len(self.kpi_dict['all'])
        i = 0
        for k, v in self.kpi_dict.items():
            for k1, v1 in v.items():

                insert_string += "( " + "'" + k + "'" + ", " + str(v1) + ", " +"'" +  k1+"'"+", "+str(self.tranpsort.simCore.currentRunID)  + ")"
                if i != len_dict * len_sub_dict - 1:
                    insert_string += " , "
                    i += 1

        self.simCore.data_base.execute_querry(insert_string)

        schema_name = "log"
        table_name = "transport_time"
        columns = "transportID,kpi_value,time,type,run_id"

        b = 0
        number_of_time_slots = 4
        number_of_time_steps = len(self.kpi_time_dict['time'])
        run=True
        while run:
            start_b = b
            if b+number_of_time_slots<=number_of_time_steps:
                end_b=start_b + number_of_time_steps
            else:
                end_b = number_of_time_steps-1
                run=False
            for b in range(start_b, end_b):
                i = 0
                insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                                """ VALUES  """
                for k, v in self.kpi_dict.items():

                    for k1, v1 in self.kpi_time_dict[k].items():
                        insert_string += "( " + "'" + k + "'" + ", " + str(v1[b]) + ", " + str(
                            self.kpi_time_dict['time'][b]) + ", " + "'" +\
                            k1 + "'"+", "+str(self.tranpsort.simCore.currentRunID)  + ")"
                        if i != len_dict * len_sub_dict - 1 and b < start_b + number_of_time_steps:
                            insert_string += " , "
                            i += 1


            self.simCore.data_base.execute_querry(insert_string)
            b += 1



