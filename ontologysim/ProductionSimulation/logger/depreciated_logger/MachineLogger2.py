import csv
import math

from ontologysim.ProductionSimulation.logger.Logger import Logger
from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum
import pandas as pd

class MachineLogger(Logger):
    """

    """
    def __init__(self, machine,simCore):
        super().__init__(simCore)
        self.machine = machine


    def init_dict(self):
        """

        """
        machine_list = [machine for machine in
                      self.machine.simCore.onto.search(type=self.machine.simCore.central.machine_class)]
        self.kpi_time_dict['time'] = []
        self.kpi_time_dict['all'] = {}
        self.kpi_dict['all'] = {}
        for e in Machine_Enum:
            self.kpi_dict['all'][e.value]=0
            self.kpi_time_dict['all'][e.value] = []
        for machine in machine_list:
            machine_name = machine.name
            self.kpi_time_dict[machine_name] = {}
            self.kpi_dict[machine_name] = {}
            self.current_event[machine_name] = Machine_Enum.Wait.value
            self.current_time[machine_name] = 0
            self.kpi_current_time_slot_dict[machine_name] = {}
            for e in Machine_Enum:
                self.kpi_current_time_slot_dict[machine_name][e.value] = 0
                self.kpi_time_dict[machine_name][e.value] = []
                self.kpi_dict[machine_name][e.value]=0

    def add_element(self, machine_onto_name, time, new_event_name):
        """

        :param machine_onto_name:
        :param time:
        :param new_event_name:
        """
        old_event=self.current_event[machine_onto_name]
        if time >= self.last_time_intervall + self.time_intervall:
            self.evaluate(time)

        self.kpi_current_time_slot_dict[machine_onto_name][old_event] += (time -
                                                                                       self.current_time[
                                                                                           machine_onto_name]) / self.time_intervall
        self.current_time[machine_onto_name] = time
        self.current_event[machine_onto_name] = new_event_name



    def evaluate(self, time):
        """

        :param time:
        """
        time_multiple = math.floor(time / self.time_intervall)
        self.kpi_time_dict['time'].append(time_multiple * self.time_intervall)

        for event in Machine_Enum:
            count_machine = 0
            sum_machine = 0
            for machine, event_dict in self.kpi_current_time_slot_dict.items():
                time_diff = time_multiple*self.time_intervall - self.current_time[machine]
                self.current_time[machine] = time_multiple * self.time_intervall
                self.kpi_current_time_slot_dict[machine][self.current_event[machine]]+=time_diff/self.time_intervall

                count_machine+=1
                kpi_value=self.kpi_current_time_slot_dict[machine][event.value]
                sum_machine+=kpi_value
                self.kpi_time_dict[machine][event.value].append(kpi_value)

                self.kpi_dict[machine][event.value]=time_diff
                self.kpi_current_time_slot_dict[machine][event.value] = 0


            self.kpi_time_dict['all'][event.value].append(sum_machine / count_machine)

        self.last_time_intervall += self.time_intervall

    def finale_evaluate(self,time):
        """

        :param time:
        """
        for event in Machine_Enum:
            sum = 0
            count = 0
            for machine, event_dict in self.kpi_current_time_slot_dict.items():

                self.kpi_dict[machine][event.value]=self.kpi_dict[machine][event.value]/time
                sum+=self.kpi_dict[machine][event.value]
                count+=1
            self.kpi_dict['all'][event.value]=sum/count


    def save_to_csv(self, type):
        """

        :param type:
        """
        with open(self.path_csv, type, newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            header=['time']

            header.extend([str(machine) +" "+ str(event) for machine, time_dict in self.kpi_dict.items() for event, time   in time_dict.items()])

            wr.writerow(header)
            erg_list = []
            for i in range(len(self.kpi_time_dict['time'])):
                erg=[self.kpi_time_dict['time'][i]]

                erg.extend([self.kpi_time_dict[machine][event][i] for machine, time_dict in self.kpi_dict.items() for event, time   in time_dict.items()])

                erg_list.append(erg)

            wr.writerows(erg_list)

    def save(self):
        """

        """
        if "database" in self.type:
            self.simCore.data_base.createSchema_enum()
            self.simCore.data_base.createSchema_log()
            self.simCore.data_base.createTable_MachineEnum()
            self.simCore.data_base.insertTable_MachineEnum()
            self.simCore.data_base.createTable_MachineTimeLog()
            self.simCore.data_base.createTable_MachineLog()
            self.insert_db()
        if "csv" in self.type:
            self.save_to_csv("w")


    def insert_db(self):
        """

        """
        schema_name = "enum"
        table_name = "machine"
        sql_query = pd.read_sql_query("""SELECT * FROM """ + schema_name + "." + table_name, self.simCore.data_base.cnxn)
        machine_enum_dict={}
        for index, rows in sql_query.iterrows():
            # Create list for the current row
            machine_enum_dict[rows.machine_enum]=rows.id

        schema_name = "log"
        table_name = "machine"
        columns = "machineID,kpi_value,type, run_id"
        insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                         """ VALUES  """
        len_dict=len(self.kpi_dict)
        len_sub_dict=len(self.kpi_dict['all'])
        i=0
        for k,v in self.kpi_dict.items():
            for k1,v1 in v.items():

                insert_string+="( "+"'"+k + "'"+", "+ str(v1)  +", "+str(machine_enum_dict[k1])+", "+str(self.machine.simCore.currentRunID) +")"
                if i!=len_dict*len_sub_dict-1:
                    insert_string+=" , "
                    i+=1


        self.simCore.data_base.execute_querry(insert_string)

        schema_name = "log"
        table_name = "machine_time"
        columns = "machineID,kpi_value,time,type, run_id"

        b=0
        number_of_time_slots=4
        number_of_time_steps=len(self.kpi_time_dict['time'])


        run = True
        while run:
            start_b = b
            if b + number_of_time_slots <= number_of_time_steps:
                end_b = start_b + number_of_time_steps
            else:
                end_b = number_of_time_steps-1
                run = False

            for b in range(start_b, end_b):
                i = 0
                insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                                """ VALUES  """
                for k, v in self.kpi_dict.items():

                    for k1, v1 in self.kpi_time_dict[k].items():

                        insert_string += "( " + "'" + k + "'" + ", " +  str(v1[b])  + ", "+str(self.kpi_time_dict['time'][b]) +", " + \
                            str(machine_enum_dict[k1])+", "+str(self.machine.simCore.currentRunID) + ")"
                        if i != len_dict * len_sub_dict - 1 and b<start_b+number_of_time_steps:
                            insert_string += " , "
                            i += 1


            self.simCore.data_base.execute_querry(insert_string)
            b+=1





