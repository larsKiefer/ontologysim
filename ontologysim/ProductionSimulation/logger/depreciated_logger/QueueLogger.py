import csv
import math

from ontologysim.ProductionSimulation.logger.Logger import Logger
from ontologysim.ProductionSimulation.sim.Enum import Label


class QueueLogger(Logger):
    """

    """
    def __init__(self,queue,simCore):
        super().__init__(simCore)
        self.queue=queue
        self.current_size_blocked = {}
        self.current_time_blocked = {}


    def init_dict(self):
        """

        """
        queue_list=[queue for queue in self.queue.simCore.central.queue_list   if not Label.EndQueue.value in queue.name  ]
        self.kpi_time_dict['time'] = []
        self.kpi_time_dict['all'] = []
        self.kpi_dict['all'] = 0
        for queue in queue_list:
            queue_name=queue.name
            self.kpi_time_dict[queue_name]  =[]
            self.kpi_dict[queue_name]       =0
            self.current_size_blocked[queue_name] = 0
            self.current_time_blocked[queue_name] = 0
            self.kpi_current_time_slot_dict[queue_name]={}
            for i in range(queue.size+1):
                self.kpi_current_time_slot_dict[queue_name][i]=0
        
        

    def add_element(self,old_queue_onto_name,time,old_current_size,queue_onto_name,current_size):
        """

        :param old_queue_onto_name:
        :param time:
        :param old_current_size:
        :param queue_onto_name:
        :param current_size:
        """
        if not Label.EndQueue.value in queue_onto_name:
            if time>=self.last_time_intervall+self.time_intervall:
                self.evaluate(time)
            
            self.kpi_current_time_slot_dict[old_queue_onto_name][old_current_size+1]+=(time-self.current_time_blocked[old_queue_onto_name])/self.time_intervall
            self.kpi_current_time_slot_dict[queue_onto_name][current_size-1]+=(time-self.current_time_blocked[queue_onto_name])/self.time_intervall
            self.current_time_blocked[queue_onto_name]=time
            self.current_size_blocked[queue_onto_name]=current_size
            self.current_time_blocked[old_queue_onto_name]=time
            self.current_size_blocked[old_queue_onto_name]=old_current_size

    def evaluate(self,time):
        """

        :param time:
        """
        time_multiple= math.floor(time/self.time_intervall)
        self.kpi_time_dict['time'].append(time_multiple*self.time_intervall)
        count_queue=0
        sum_queue=0
        for queue, position_dict in self.kpi_current_time_slot_dict.items():
            time_diff=time_multiple*self.time_intervall-self.current_time_blocked[queue]
            self.current_time_blocked[queue]=time_multiple*self.time_intervall
            self.kpi_current_time_slot_dict[queue][self.current_size_blocked[queue]]+=time_diff/self.time_intervall*self.current_size_blocked[queue]
            count=0
            sum=0
            count_queue+=1
            for position_number, kpi_value in position_dict.items():
                count+=1
                sum+=kpi_value
                self.kpi_current_time_slot_dict[queue][position_number]=0

            self.kpi_time_dict[queue].append(sum/count)
            self.kpi_dict[queue]+=sum/count
            sum_queue+= sum/count
        self.kpi_time_dict['all'].append(sum_queue/count_queue)

        self.last_time_intervall+=self.time_intervall

    def finale_evaluate(self, time):
        """

        :param time:
        """
        for queue, position_dict in self.kpi_current_time_slot_dict.items():
            self.kpi_dict[queue] = self.kpi_dict[queue]/ math.ceil(time/self.time_intervall)
        self.kpi_dict['all'] = sum(self.kpi_dict.values())/len(self.kpi_dict.values())



    def save_to_csv(self,type):
        """

        :param type:
        """
        with open(self.path_csv, type, newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            header=[queue for queue, time_dict in self.kpi_time_dict.items()]
            wr.writerow(header)
            erg_list=[]
            for i in range(len(self.kpi_time_dict['time'])):
                erg_list.append([self.kpi_time_dict[element][i] for element in header]    )


            wr.writerows(erg_list)

    def save(self):
        """

        """
        if "database" in self.type:
            self.simCore.data_base.createSchema_log()
            self.simCore.data_base.createTable_QueueTimeLog()
            self.simCore.data_base.createTable_QueueLog()
            self.insert_db()
        if "csv" in self.type:
            self.save_to_csv("w")

    def insert_db(self):
        """

        """
        schema_name = "log"
        table_name = "queue"
        columns = "queueID,kpi_value,run_id"
        insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                        """ VALUES  """
        len_dict = len(self.kpi_dict)
        len_sub_dict = 1
        i = 0
        for k, v in self.kpi_dict.items():


            insert_string += "( " + "'" + k + "'" + ", " + str(v) +", "+str(self.queue.simCore.currentRunID)  + ")"
            if i != len_dict * len_sub_dict - 1:
                insert_string += " , "
                i += 1

        self.simCore.data_base.execute_querry(insert_string)

        schema_name = "log"
        table_name = "queue_time"
        columns = "queueID,kpi_value,time,run_id"

        b = 0
        number_of_time_slots = 4
        number_of_time_steps = len(self.kpi_time_dict['time'])
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
                    insert_string += "( " + "'" + k + "'" + ", " + str(self.kpi_time_dict[k][b]) + ", " + str(
                        self.kpi_time_dict['time'][b])+", "+str(self.queue.simCore.currentRunID)  +  ")"
                    if i != len_dict * len_sub_dict - 1 and b < start_b + number_of_time_steps:
                        insert_string += " , "
                        i += 1

            self.simCore.data_base.execute_querry(insert_string)
            b += 1

