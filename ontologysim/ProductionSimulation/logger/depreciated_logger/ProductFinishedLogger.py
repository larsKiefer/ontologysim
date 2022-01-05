import csv
import math

from ontologysim.ProductionSimulation.logger.Logger import Logger


class ProductFinishedLogger(Logger):
    """

    """
    def __init__(self,simCore):
        super().__init__(simCore)
        self.product_list=[]
        self.kpi_dict = {}
        self.kpi_time_dict = {}  # time overall q1
        self.kpi_current_time_slot_dict = {}
        self.number_current_time_slot_dict={}
        self.number_dict={}
        self.time_intervall = 100


    def add_product(self,product_name,start_time,finished_time,product_type,time_diff):
        """

        :param product_name:
        :param start_time:
        :param finished_time:
        :param product_type:
        :param time_diff:
        """
        self.product_list.append([product_name,start_time,finished_time,product_type.name,time_diff])

    def save_to_csv(self,type):
        """

        :param type:
        """
        with open(self.path_csv, type, newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            wr.writerows(self.product_list)

        with open(self.path_csv[:-4]+"_dict.csv", type, newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            header = ['time']
            header.extend(
                [str(elements) for elements, time_dict in self.kpi_dict.items()])

            wr.writerow(header)
            erg_list = []

            for i in range(len(self.kpi_time_dict['time'])):
                erg = [self.kpi_time_dict['time'][i]]

                erg.extend([self.kpi_time_dict[product_type][i] for product_type, time_dict in self.kpi_dict.items() ])

                erg_list.append(erg)

            wr.writerows(erg_list)

    def init_dict(self):
        """

        """
        product_type_list = [product_type for product_type in
                      self.simCore.onto.search(type= self.simCore.central.product_type_class) ]
        self.kpi_time_dict['time'] = []
        self.kpi_time_dict['all'] = []
        self.kpi_dict['all'] = 0
        for product_type in product_type_list:
            product_type_name = product_type.name
            self.kpi_time_dict[product_type_name] = []
            self.kpi_dict[product_type_name] = 0
            self.kpi_current_time_slot_dict[product_type_name] = 0
            self.number_current_time_slot_dict[product_type_name] = 0
            self.number_dict[product_type_name]=0

    def add_element(self,product_type ,time,time_diff):
        """

        :param product_type:
        :param time:
        :param time_diff:
        """
        product_type_name=product_type.name
        if time >= self.last_time_intervall + self.time_intervall:
            self.evaluate(time)

        self.kpi_current_time_slot_dict[product_type_name] += time_diff
        self.number_current_time_slot_dict[product_type_name] += 1
        self.number_dict[product_type_name] +=1


    def evaluate(self, time):
        """

        :param time:
        """
        time_multiple = math.floor(time / self.time_intervall)
        self.kpi_time_dict['time'].append(time_multiple * self.time_intervall)
        sum_time_product_type=0
        count_time_product_type=0
        for product_type, kpi in self.kpi_current_time_slot_dict.items():

            kpi_value=0
            if self.number_current_time_slot_dict[product_type]>0:
                kpi_value=self.kpi_current_time_slot_dict[product_type]/self.number_current_time_slot_dict[product_type]
            if kpi_value>0:
                count_time_product_type+=1
                sum_time_product_type+=kpi_value
            self.kpi_time_dict[product_type].append(kpi_value)
            self.kpi_current_time_slot_dict[product_type]=0
            self.number_current_time_slot_dict[product_type]=0
            self.kpi_dict[product_type]+= kpi_value

        self.kpi_time_dict['all'].append(sum_time_product_type / count_time_product_type)
        self.last_time_intervall += self.time_intervall

    def finale_evaluate(self, time):
        """

        :param time:
        """
        for product_type, kpi in self.number_dict.items():
            if self.kpi_dict[product_type]!=0:
                self.kpi_dict[product_type]=self.kpi_dict[product_type]/self.number_dict[product_type]
            else:
                self.kpi_dict[product_type] =0
        self.kpi_dict['all'] = sum(self.kpi_dict.values())/sum(self.number_dict.values())

    def save(self):
        """

        """
        if "database" in self.type:
            self.simCore.data_base.createSchema_log()
            self.simCore.data_base.createTable_AllProductFinishedLog()
            self.simCore.data_base.createTable_ProductFinishedLog()
            self.simCore.data_base.createTable_ProductFinishedTimeLog()
            self.insert_db()
        if "csv" in self.type:
            self.save_to_csv("w")

    def insert_db(self):
        """

        """
        schema_name = "log"
        table_name = "all_product_finished"
        columns = "product_id, start_time, finished_time, product_type, production_time, run_id"

        i=0
        step_size=25
        product_finished_len=len(self.product_list)
        run=True
        while run and i+1!=product_finished_len:
            insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                            """ VALUES  """

            if i + step_size < product_finished_len:
                end_i=i + step_size-1
            else:
                end_i=product_finished_len-1
                run=False

            for product_element in self.product_list[i:end_i]:
                product_element.append(str(self.simCore.currentRunID))

                insert_string += str(tuple(product_element)) + ","

            self.product_list[end_i].append(str(self.simCore.currentRunID))

            insert_string += str(
                tuple(self.product_list[end_i]))

            self.simCore.data_base.execute_querry(insert_string)
            i += step_size

        schema_name = "log"
        table_name = "product_finished"
        columns = "product_type_id, kpi_value, run_id"
        insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                        """ VALUES  """
        len_dict = len(self.kpi_dict)
        len_sub_dict = 1
        i = 0
        for k, v in self.kpi_dict.items():

            insert_string += "( " + "'" + k + "'" + ", " + str(v) +", "+str(self.simCore.currentRunID)+ ")"
            if i != len_dict * len_sub_dict - 1:
                insert_string += " , "
                i += 1

        self.simCore.data_base.execute_querry(insert_string)

        schema_name = "log"
        table_name = "product_finished_time"
        columns = "product_type_id, kpi_value,time,run_id"

        b = 0
        number_of_time_slots = 4
        number_of_time_steps = len(self.kpi_time_dict['time'])
        run = True
        while run:
            start_b = b
            if b + number_of_time_slots <= number_of_time_steps:
                end_b = start_b + number_of_time_steps
            else:
                end_b = number_of_time_steps - b
                run = False
            for b in range(start_b, end_b):

                i = 0
                insert_string = """ INSERT INTO """ + schema_name + "." + table_name + " ( " + columns + " ) " + \
                                """ VALUES  """
                for k, v in self.kpi_dict.items():
                    insert_string += "( " + "'" + k + "'" + ", " + str(self.kpi_time_dict[k][b]) + ", " + str(
                        self.kpi_time_dict['time'][b])+", "+str(self.simCore.currentRunID) + ")"
                    if i != len_dict * len_sub_dict - 1 and b < start_b + number_of_time_steps:
                        insert_string += " , "
                        i += 1

            self.simCore.data_base.execute_querry(insert_string)
            b += 1
