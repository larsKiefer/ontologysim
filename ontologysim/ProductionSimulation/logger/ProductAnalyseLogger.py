import copy
import csv
import math

from ontologysim.ProductionSimulation.database.models.ProductKPI import ProductKPI, AllProducts, ProductTimeKPI, ProductTimeKPIValue
from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum, Logger_Type_Enum
from ontologysim.ProductionSimulation.logger import SubLogger
from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Queue_Enum, Evaluate_Enum, Label, OrderRelease_Enum
from ontologysim.ProductionSimulation.utilities import init_utilities
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest



class ProductAnalyseLogger(SubLogger.SubLogger):
    """
    calculates all product related kpi's
    """

    def __init__(self, logger):
        """

        :param logger:
        """
        super().__init__(logger)

        self.kpi_list = ["ProductType", "WIP", "ATTp", "AQMTp", "AUSTp", "APTp", "AUPTp", "AUSTnpp","PBTp", "AOET"]
        self.basic_kpi_list = ["TR","NrP"]
        self.last_value = {}
        self.number_of_product_types = 0
        self.number_of_instances = 1
        self.product_kpis = {}
        self.number_of_products = {}
        self.number_of_products_time = {}
        self.wip = {}
        # Actual unit transportation time (ATT)legino
        # Actual unit queue machine time (AQMT): Machine time

        # Actual unit processing time (AUPT): The time necessary for production and setup on a machine for an order.
        # Actual production time (APT): The actual time in which the machine is producing for an order, which only includes
        #       the value-adding functions.
        # Actual unit setup time (AUST): The time used for the preparation, i.e. setup, of an order on a machine.
        #   Thus, the following relationship is observed:
        # Actual unit setup time not production (AUSTnpp)

        # Actual unit order time (AOET)

    def initSubLogger(self, log_type_dict):
        """

        initializing of sub_logger, set up the time and summarized kpi dict

        :param dict_element: information from config
        """

        self.type = log_type_dict[Logger_Enum.ProductLogger.value]
        self.type_product= log_type_dict[Logger_Enum.AllProductsLogger.value]

        if (self.isNotLogging() and (self.type_product == Logger_Type_Enum.Not.value )):
            for key, value in self.logger.transform_event_type_in_log_type.items():
                if self in value:
                    self.logger.transform_event_type_in_log_type[key].remove(self)

            return


        product_type_list = [product_type for product_type in
                             self.logger.simCore.onto.search(type=self.logger.simCore.central.product_type_class)]


        self.number_of_product_types = len(product_type_list)

        self.number_of_products['all'] = 0
        self.number_of_products_time['all'] = []
        self.wip["all"] = {'start_time': [0], 'number_of_products': [0]}

        if(not self.isNotLogging() or (self.type_product != Logger_Type_Enum.Not.value )):
            self.summarized_kpis['all'] = {}

            for product_type in product_type_list:
                product_type_name = product_type.name
                self.summarized_kpis[product_type_name] = {}
                self.number_of_products[product_type_name] = 0
                self.number_of_products_time[product_type_name] = []

                self.wip[product_type_name] = {'start_time': [0], 'number_of_products': [0]}

                for kpi in self.kpi_list:
                    self.summarized_kpis[product_type_name][kpi] = 0
                for kpi in self.basic_kpi_list:
                    self.summarized_kpis[product_type_name][kpi] = 0

            for kpi in self.kpi_list:
                self.summarized_kpis['all'][kpi] = 0

            for kpi in self.basic_kpi_list:
                self.summarized_kpis['all'][kpi] = 0



        if(self.isTimeLogging()):
            self.time_kpis["time"] = []
            self.time_kpis["all"] = {}
            for product_type in product_type_list:
                product_type_name = product_type.name
                self.time_kpis[product_type_name] = {}
                for kpi in self.kpi_list:
                    self.time_kpis[product_type_name][kpi] = []
                for kpi in self.basic_kpi_list:
                    self.time_kpis[product_type_name][kpi] = []


            for kpi in self.kpi_list:
                self.time_kpis["all"][kpi] = []
            for kpi in self.basic_kpi_list:
                self.time_kpis["all"][kpi] = []



    def setLastWIP(self, time):
        """
        calculates the wpi to the given time and saves the value in the wip dict

        :param time: double
        """

        if(not self.isNotLogging() or (self.type_product != Logger_Type_Enum.Not.value )):


            for queue in self.logger.simCore.central.queue_list:

                if Label.EndQueue.value not in queue.name:
                    for position in queue.has_for_position:
                        if position.blockedSpace == 1 and len(position.has_for_product) > 0:
                            product = position.has_for_product[0]
                            product_type = product.has_for_product_type[0]
                            product_type_name = product_type.name
                            self.wip[product_type_name]['number_of_products'][0] += 1
                            self.wip["all"]['number_of_products'][0] += 1
            for k, v in self.wip.items():
                self.wip[k]['start_time'][0] = time



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
                product_type_list = [product_type.name for product_type in
                                     self.logger.simCore.onto.search(type=self.logger.simCore.central.product_type_class)]
                self.addNewTimeElement(product_type_list, self.kpi_list, time)
                self.addNewTimeElement(product_type_list, self.basic_kpi_list, time)
                time_multiple = math.floor(time / self.logger.time_intervall)

                time_len = len(self.time_kpis['time'])
                for i in range(time_index - time_len, -1, -1):
                    self.time_kpis["time"].append((time_multiple - i) * self.logger.time_intervall)

                if(time_index >0):

                    self.calculateWIP((time_multiple) * self.logger.time_intervall)

                for k, v in self.number_of_products_time.items():
                    self.number_of_products_time[k].append(0)

                self.update_list = [time_index - 1]
                self.update_basic_kpis()
                self.logger.simLogger.product_update = True
                self.logger.simLogger.update_basic_kpis()

        if event_type == Machine_Enum.Process.value:
            product_name_list = dict_element['product_name_list']
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            for product_name in product_name_list:
                self.check_product(product_name, time)
                time = dict_element["event_onto_time"]
                self.product_kpis[product_name]["APTp"] += time_diff
                self.product_kpis[product_name]["AUPTp"] += time_diff
                self.product_kpis[product_name]["PBTp"] += time_diff
                if(self.isTimeLogging()):
                    self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["APTp", "AUPTp","PBTp"], time, time_diff)
                self.last_value[product_name]["machine_queue_time"] = time

        elif event_type == Queue_Enum.StartProcess.value or event_type == Queue_Enum.StartProcessStayBlocked.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            product_name = self.check_product(dict_element['product_name'], time)

            time = dict_element["event_onto_time"]
            aqmt_time = time - self.last_value[product_name]["machine_queue_time"] - time_diff
            self.product_kpis[product_name]["AQMTp"] += time - self.last_value[product_name][
                "machine_queue_time"] - time_diff
            self.product_kpis[product_name]["AUSTp"] += time_diff
            self.product_kpis[product_name]["AUPTp"] += time_diff
            self.product_kpis[product_name]["PBTp"] += time_diff
            if(self.isTimeLogging()):
                self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["AUSTp", "AUPTp","PBTp"], time, time_diff)
                if aqmt_time > 0:
                    self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["AQMTp"], time,
                                        time - self.last_value[product_name]["machine_queue_time"] - time_diff)


        elif event_type == Queue_Enum.EndProcess.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            time = dict_element["event_onto_time"]
            product_name = self.check_product(dict_element['product_name'], time)
            self.last_value[product_name]["machine_queue_time"] = time
            self.product_kpis[product_name]["AUSTp"] += time_diff
            self.product_kpis[product_name]["AUPTp"] += time_diff
            self.product_kpis[product_name]["PBTp"] += time_diff
            if(self.isTimeLogging()):
                self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["AUSTp", "AUPTp","PBTp"], time, time_diff)

        elif event_type == Queue_Enum.AddToTransporter.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            time = dict_element["event_onto_time"]
            product_name = self.check_product(dict_element['product_name'], time)
            self.last_value[product_name]["transporter_queue_time"] = time
            self.product_kpis[product_name]['AUSTnpp'] += time_diff
            if time - self.last_value[product_name]["machine_queue_time"] - time_diff > 0:
                self.product_kpis[product_name]["AQMTp"] += time - self.last_value[product_name][
                    "machine_queue_time"] - time_diff
            if(self.isTimeLogging()):
                self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["AUSTnpp"], time,
                                    time_diff)
                if time - self.last_value[product_name]["machine_queue_time"] - time_diff > 0:
                    self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["AQMTp"], time,
                                        time - self.last_value[product_name]["machine_queue_time"] - time_diff)

        elif event_type == Queue_Enum.RemoveFromTransporter.value or event_type == Queue_Enum.RemoveFromTransporterDeadlock.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            time = dict_element["event_onto_time"]
            product_name = self.check_product(dict_element['product_name'], time)
            if time - self.last_value[product_name]["transporter_queue_time"] - time_diff > 0:
                self.product_kpis[product_name]['ATTp'] += time - self.last_value[product_name][
                    "transporter_queue_time"] - time_diff
            self.product_kpis[product_name]['AUSTnpp'] += time_diff
            self.last_value[product_name]['machine_queue_time'] = time
            if(self.isTimeLogging()):
                if time - self.last_value[product_name]["transporter_queue_time"] - time_diff > 0:
                    self.addTimeElement(self.product_kpis[product_name]["ProductType"], ["ATTp"], time,
                                        time - self.last_value[product_name]["transporter_queue_time"] - time_diff)
                self.addTimeElement(self.product_kpis[product_name]["ProductType"], ['AUSTnpp'], time,
                                    time_diff)

        elif event_type == Evaluate_Enum.ProductFinished.value:

            time = dict_element["event_onto_time"]
            product_name = self.check_product(dict_element['product_name'], time)

            number_of_products_before = self.wip[self.product_kpis[product_name]["ProductType"]]['number_of_products'][
                -1]

            self.summarized_kpis[self.product_kpis[product_name]["ProductType"]]["WIP"]+=number_of_products_before * (time-self.wip[self.product_kpis[product_name]["ProductType"]]['start_time'][-1])


            self.wip[self.product_kpis[product_name]["ProductType"]]['start_time'].append(time)
            self.wip[self.product_kpis[product_name]["ProductType"]]['number_of_products'].append(
                number_of_products_before - 1)
            number_of_products_before = self.wip['all']['number_of_products'][-1]



            self.wip['all']['number_of_products'].append(number_of_products_before - 1)
            self.wip['all']['start_time'].append(time)
            self.product_kpis[product_name]['start_time'] = dict_element["start_time"]
            self.product_kpis[product_name]['end_time'] = dict_element["end_time"]
            self.product_kpis[product_name]['AOET'] = dict_element["AOET"]
            # if time - dict_element["AOET"] < self.logger.start_time_logging:
            #    dict_element["AOET"] = time - self.logger.start_time_logging
            if (self.isTimeLogging()):
                self.addTimeElement(self.product_kpis[product_name]["ProductType"], ['AOET'], time, dict_element["AOET"])

                self.number_of_products_time[self.product_kpis[product_name]["ProductType"]][time_index] += 1
                self.number_of_products_time['all'][time_index] += 1


        elif event_type == Queue_Enum.Change.value or event_type == Queue_Enum.Default.value:
            raise Exception("warning")
        elif event_type == Queue_Enum.StartOfProduction.value:
            dict_element = self.checkStartTimeLogging(dict_element)
            time_diff = dict_element['time_diff']
            time = dict_element["event_onto_time"]
            product_name = self.check_product(dict_element['product_name'], time)
            self.last_value[product_name]["machine_queue_time"] = time

        elif event_type == OrderRelease_Enum.Release.value:
            time = dict_element["event_onto_time"]
            number_of_products = dict_element["number_of_products"]
            product_type_name = dict_element["product_type"]
            number_of_products_before = self.wip[product_type_name]['number_of_products'][-1]

            self.summarized_kpis[product_type_name]["WIP"] += number_of_products_before * (
                        time - self.wip[product_type_name]['start_time'][-1])

            self.wip[product_type_name]['start_time'].append(time)
            self.wip[product_type_name]['number_of_products'].append(
                number_of_products_before + number_of_products)
            number_of_products_before = self.wip['all']['number_of_products'][-1]

            self.summarized_kpis[product_type_name]["WIP"] += number_of_products_before * (
                    time - self.wip["all"]['start_time'][-1])
            self.wip['all']['number_of_products'].append(number_of_products_before + number_of_products)
            self.wip['all']['start_time'].append(time)

            # self.addTimeElement()

    def addTimeElement(self, object_name, kpi_key_list, time, time_diff):
        """
        override the add time element of Sub logger, because of the AOET KPI
        adds a new value to the time element (time intervall)

        :param object_name: label
        :param kpi_key_list: [KPI's name]
        :param time: double
        :param time_diff: double
        :return:
        """

        if time_diff == 0:
            return
        if time_diff < 0:

            raise Exception(kpi_key_list)

        split_time_dict = self.split_time(time, time_diff)

        for k, v in split_time_dict.items():

            number_of_instances = self.calculateWIPTimeDiff(v['time_diff'], v['end_time'], object_name)
            if self.number_of_product_types!=1:
                number_of_instances_all = self.calculateWIPTimeDiff(v['time_diff'], v['end_time'], 'all')
            else:
                number_of_instances_all=number_of_instances
            for kpi_key in kpi_key_list:
                if kpi_key == "AOET":
                    time_index = int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)
                    self.time_kpis[object_name]["AOET"][k] += v['time_diff']
                    self.time_kpis["all"]["AOET"][k] += v['time_diff']
                elif kpi_key=="NrP":
                    raise Exception("NrP update")
                else:

                    self.time_kpis[object_name][kpi_key][k] += v[
                                                                   'time_diff'] / self.logger.time_intervall / number_of_instances
                    self.time_kpis["all"][kpi_key][k] += v['time_diff'] / self.logger.time_intervall / number_of_instances_all



    def calculateWIPTimeDiff(self, time_diff, end_time, object_name):
        """
        calculate the WIP for a given time intervall

        :param time_diff:
        :param end_time:
        :param object_name:
        :return:
        """
        number_of_instances = 0
        current_time_element_instances = time_diff

        end_time_element_instances = end_time

        sum_time_elemnts=0
        for b in range(len(self.wip[object_name]['start_time']) - 1, -1, -1):
            if end_time_element_instances - self.wip[object_name]['start_time'][b] > 0:

                time_difference = end_time_element_instances - self.wip[object_name]['start_time'][b]
                if time_difference > current_time_element_instances:
                    time_difference = current_time_element_instances

                if current_time_element_instances > 0:
                    sum_time_elemnts+=time_difference

                    number_of_instances += self.wip[object_name]['number_of_products'][
                                               b] * time_difference / time_diff

                    end_time_element_instances = self.wip[object_name]['start_time'][b]

                    if b > 0:
                        if sum_time_elemnts>time_diff:
                            break
                current_time_element_instances -= time_difference

                if b!=len(self.wip[object_name]['start_time']) - 1 and time_difference==0:
                    break
            else:
                pass


        return number_of_instances

    def calculateWIP(self, end_time_intervall):
        """
        calculates the wip for one logging time intervall

        :param edn_time_intervall: edn of the time element
        :return:
        """

        if self.isTimeLogging():
            if(end_time_intervall % self.logger.time_intervall != 0):

                start_time_intervall = math.floor(end_time_intervall / self.logger.time_intervall) * self.logger.time_intervall
                index = int(start_time_intervall / self.logger.time_intervall - self.start_logging_multiple)
                for k, v in self.wip.items():
                    self.time_kpis[k]["WIP"][index] = self.calculateWIPTimeDiff(end_time_intervall-start_time_intervall,
                                                                                end_time_intervall, k)*(end_time_intervall-start_time_intervall)/self.logger.time_intervall

            else:
                start_time_intervall = end_time_intervall - self.logger.time_intervall

                index = int(start_time_intervall / self.logger.time_intervall - self.start_logging_multiple)

                for k, v in self.wip.items():
                    self.time_kpis[k]["WIP"][index] = self.calculateWIPTimeDiff(self.logger.time_intervall, end_time_intervall, k)


    def check_product(self, product_name, time, event_type=None, time_diff=0):
        """
        if the product has never been logged before than the last value is set,and the product type is saved in a dict for faster access

        :param product_name:
        :param time:
        :param event_type:
        :param time_diff:
        :return:
        """
        if product_name in self.product_kpis.keys():
            return product_name
        else:

            self.last_value[product_name] = {}
            self.last_value[product_name]["machine_queue_time"] = time
            self.last_value[product_name]["transporter_queue_time"] = time

            self.product_kpis[product_name] = {}
            for kpi in self.kpi_list:
                self.product_kpis[product_name][kpi] = 0

            self.product_kpis[product_name]["ProductType"] = \
                self.logger.simCore.onto[product_name].has_for_product_type[0].name

            return product_name

    def update_basic_kpis(self):
        """
        calculates the basic kpi's
        """
        if(self.isTimeLogging()):
            #print(len(self.number_of_products_time["all"]),self.number_of_products_time["all"],self.update_list)
            #print(len(self.time_kpis["all"]["NrP"]),self.time_kpis["all"]["NrP"])
            for update_index in self.update_list:
                for k, v in self.number_of_products_time.items():
                    if(len(self.number_of_products_time[k])<update_index):
                        for i in range(len(self.number_of_products_time[k])-1, update_index+1):
                            self.number_of_products_time[k].append(0)
                    #print(len(self.number_of_products_time[k]))
                    self.time_kpis[k]["NrP"][update_index] = self.number_of_products_time[k][update_index]
                    self.time_kpis[k]["TR"][update_index] = self.number_of_products_time[k][
                                                                update_index] / self.logger.time_intervall
                    if self.number_of_products_time[k][update_index] > 0:
                        self.time_kpis[k]["AOET"][update_index] = self.time_kpis[k]["AOET"][update_index] / \
                                                                  self.number_of_products_time[k][update_index]

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """

        last_time_element = int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)
        if(self.isTimeLogging()):

            if(len(self.time_kpis["time"])<=last_time_element):
                self.addNewTimeElement([machine.name for machine in
                                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                       self.kpi_list, time)
                self.addNewTimeElement([machine.name for machine in
                                        self.logger.simCore.onto.search(type=self.logger.simCore.central.machine_class)],
                                       self.basic_kpi_list, time)


        self.update_list = [last_time_element]
        self.update_basic_kpis()
        self.logger.simLogger.product_update = True
        self.logger.simLogger.update_basic_kpis()

        #self.calculateWIP(math.ceil(time / self.logger.time_intervall) * self.logger.time_intervall)
        self.calculateWIP(time)

        delete_product_list = []
        for k, v in self.product_kpis.items():
            if self.product_kpis[k]["AOET"] <= 0:
                delete_product_list.append(k)

        for product in delete_product_list:
            self.product_kpis.pop(product)

        number_of_products = len(self.product_kpis)
        logging_number_of_products = self.logger.simCore.product.logging_number_products

        if number_of_products > logging_number_of_products:
            product_kpis_keys = sorted(
                [int(str(product).replace(Label.Product.value, '')) for product in self.product_kpis.keys()])

            for i in range(number_of_products - logging_number_of_products):
                self.product_kpis.pop(Label.Product.value + str(product_kpis_keys[i]))

        for k, v in self.number_of_products.items():
            self.number_of_products[k] = 0

        if self.isSummaryLogging():
            for k, v in self.product_kpis.items():
                for k1, v1 in v.items():

                    if k1 !="start_time" and k1 !="end_time":
                        if k1 != "ProductType" and k1 != "AOET" and k1 != "WIP":
                            self.summarized_kpis[self.product_kpis[k]["ProductType"]][k1] += self.product_kpis[k][k1] / \
                                                                                             self.product_kpis[k]['AOET']
                        elif k1 == "AOET":
                            self.summarized_kpis[self.product_kpis[k]["ProductType"]][k1] += self.product_kpis[k]['AOET']


                self.number_of_products[self.product_kpis[k]["ProductType"]] += 1
                self.number_of_products['all'] += 1

            for product_type_name in [product_type.name for product_type in
                                      self.logger.simCore.onto.search(type=self.logger.simCore.central.product_type_class)]:

                for k, v in self.summarized_kpis[product_type_name].items():
                    if k == "WIP":

                        self.summarized_kpis[product_type_name]["WIP"] = self.summarized_kpis[product_type_name][
                                                                             "WIP"] / (time - self.logger.start_time_logging)
                        self.summarized_kpis["all"]["WIP"] += self.summarized_kpis[product_type_name]["WIP"]
                    elif k != "ProductType":
                        self.summarized_kpis['all'][k] += self.summarized_kpis[product_type_name][k] / \
                                                          self.number_of_products["all"]
                        if self.number_of_products[product_type_name] != 0:

                            self.summarized_kpis[product_type_name][k] = self.summarized_kpis[product_type_name][k] / \
                                                                         self.number_of_products[product_type_name]
                        else:
                            self.summarized_kpis[product_type_name][k] = 0

                    else:
                        self.summarized_kpis[product_type_name][k] = product_type_name


                self.summarized_kpis[product_type_name]["TR"] = self.number_of_products[product_type_name] / (
                        time - self.logger.start_time_logging)

                self.summarized_kpis[product_type_name]["NrP"] = self.number_of_products[product_type_name]
            self.summarized_kpis['all']["NrP"] = self.number_of_products['all']

            # all produces parts/time
            self.summarized_kpis['all']["TR"] = self.summarized_kpis['all']["NrP"] / (time - self.logger.start_time_logging)

            self.summarized_kpis['all']["ProductType"] = "all"



    def finale_evaluate_summary_api(self,time):
        """
        finale evaluate kpi for api usage
        :param time:
        :return:
        """

        delete_product_list = []
        for k, v in self.product_kpis.items():
            if self.product_kpis[k]["AOET"] <= 0:
                delete_product_list.append(k)

        for product in delete_product_list:
            self.product_kpis.pop(product)

        number_of_products = len(self.product_kpis)
        logging_number_of_products = self.logger.simCore.product.logging_number_products

        if number_of_products > logging_number_of_products:
            product_kpis_keys = sorted(
                [int(str(product).replace(Label.Product.value, '')) for product in self.product_kpis.keys()])

            for i in range(number_of_products - logging_number_of_products):
                self.product_kpis.pop(Label.Product.value + str(product_kpis_keys[i]))

        for k, v in self.number_of_products.items():
            self.number_of_products[k] = 0



        summarized_data = copy.deepcopy(self.summarized_kpis)


        for k, v in self.product_kpis.items():
            for k1, v1 in v.items():

                if k1 != "start_time" and k1 != "end_time":
                    if k1 != "ProductType" and k1 != "AOET" and k1 != "WIP":
                        summarized_data[self.product_kpis[k]["ProductType"]][k1] += self.product_kpis[k][k1] / \
                                                                                         self.product_kpis[k][
                                                                                             'AOET']
                    elif k1 == "AOET":
                        summarized_data[self.product_kpis[k]["ProductType"]][k1] += self.product_kpis[k][
                            'AOET']

            self.number_of_products[self.product_kpis[k]["ProductType"]] += 1
            self.number_of_products['all'] += 1

        for product_type_name in [product_type.name for product_type in
                                  self.logger.simCore.onto.search(
                                      type=self.logger.simCore.central.product_type_class)]:

            for k, v in summarized_data[product_type_name].items():
                if k == "WIP":

                    summarized_data[product_type_name]["WIP"] = summarized_data[product_type_name][
                                                                         "WIP"] / (
                                                                                 time - self.logger.start_time_logging)
                    summarized_data["all"]["WIP"] += summarized_data[product_type_name]["WIP"]
                elif k != "ProductType":
                    summarized_data['all'][k] += summarized_data[product_type_name][k] / \
                                                      self.number_of_products["all"]
                    if self.number_of_products[product_type_name] != 0:

                        summarized_data[product_type_name][k] = summarized_data[product_type_name][k] / \
                                                                     self.number_of_products[product_type_name]
                    else:
                        summarized_data[product_type_name][k] = 0

                else:
                    summarized_data[product_type_name][k] = product_type_name

            summarized_data[product_type_name]["TR"] = self.number_of_products[product_type_name] / (
                    time - self.logger.start_time_logging)

            summarized_data[product_type_name]["NrP"] = self.number_of_products[product_type_name]
        summarized_data['all']["NrP"] = self.number_of_products['all']

        # all produces parts/time
        summarized_data['all']["TR"] = summarized_data['all']["NrP"] / (
                    time - self.logger.start_time_logging)

        summarized_data['all']["ProductType"] = "all"


        return summarized_data



    def save_to_csv(self, path, folder_name, summarized_name):
        """
        save data to csv
        :param path:
        :param folder_name:
        :param summarized_name:
        :return:
        """
        if(self.type_product != Logger_Type_Enum.Not.value):
            with open(PathTest.check_dir_path(path + "/all_" + summarized_name + ".csv"), "w", newline='') as order_logger:
                wr = csv.writer(order_logger, delimiter=';', quoting=csv.QUOTE_ALL)

                erg_list=self.getProductList()
                wr.writerows(erg_list)

        if(self.isSummaryLogging()):
            with open(PathTest.check_dir_path(path + "/" + summarized_name + ".csv"), "w", newline='') as order_logger:
                wr = csv.writer(order_logger, delimiter=';', quoting=csv.QUOTE_ALL)

                erg_list = self.getSummaryList()
                wr.writerows(erg_list)

        if(self.isTimeLogging()):
            path_products = PathTest.create_new_folder(path, folder_name)

            for k, v in self.time_kpis.items():
                if k != "time":
                    with open(PathTest.check_dir_path(path_products + "/" + str(k) + "_logger" + ".csv"), "w",
                              newline='') as product_time_logger:
                        wr = csv.writer(product_time_logger, delimiter=';', quoting=csv.QUOTE_ALL)

                        erg_list=self.getTimeList(k)
                        wr.writerows(erg_list)

    def save_to_database(self):
        """
        save data to database
        :return:
        """
        if (self.isSummaryLogging()):

            for key, value in self.summarized_kpis.items():
                productKPI = ProductKPI(**self.summarized_kpis[key])
                self.logger.dataBase.session.add(productKPI)
                self.logger.simulationRunDB.productKPI.append(productKPI)

        if (self.type_product != Logger_Type_Enum.Not.value):

            for k, v in self.product_kpis.items():
                input = {}
                for k1, v1 in v.items():
                    if k1 != "WIP":
                        if k1 != "ProductType":
                            input[k1] = round(v1, 4)
                        else:
                            input[k1] = v1

                allProducts = AllProducts(**input,product_name = k)
                self.logger.simulationRunDB.allProducts.append(allProducts)
                self.logger.dataBase.session.add(allProducts)

        if (self.isTimeLogging()):
            for k, v in self.time_kpis.items():
                if k != "time":
                    productTimeKPI = ProductTimeKPI(name=k)
                    for i in range(len(self.time_kpis["time"])):
                        input={}
                        for k1, v1 in self.time_kpis[k].items():
                            if k1 != "ProductType":
                                input[k1] = v1[i]

                        productTimeKPIvalue = ProductTimeKPIValue(**input, time=self.time_kpis["time"][i])
                        productTimeKPI.productTimeKPIValue.append(productTimeKPIvalue)
                        self.logger.dataBase.session.add(productTimeKPIvalue)
                    self.logger.simulationRunDB.productTimeKPI.append(productTimeKPI)
                    self.logger.dataBase.session.add(productTimeKPI)

        self.logger.dataBase.session.commit()

    def getTimeList(self,object_key):
        """
        override
        :param object_key:
        :return:
        """
        erg_list=[]
        header = ["time"]

        header.extend([str(k) for k, v in self.summarized_kpis['all'].items()])
        header.remove("ProductType")
        erg_list.append(header)


        for i in range(len(self.time_kpis["time"])):
            erg = [self.time_kpis["time"][i]]

            for k1, v1 in self.time_kpis[object_key].items():
                if k1 != "ProductType":
                    erg.append(v1[i])
            erg_list.append(erg)
        return erg_list

    def getSummaryList(self):
        """

        :return:
        """
        erg_list = []
        header=[]
        header.extend([str(k) for k, v in self.summarized_kpis['all'].items()])

        erg_list.append(header)

        for k, v in self.summarized_kpis.items():
            erg = []

            for k1, v1 in v.items():
                if k1 != "ProductType":
                    erg.append(round(v1, 4))
                else:
                    erg.append(v1)
            erg_list.append(erg)
        return erg_list

    def getSummaryListAPI(self,summarized_data):

        erg_list = []
        header=[]
        header.extend([str(k) for k, v in summarized_data['all'].items()])

        erg_list.append(header)

        for k, v in summarized_data.items():
            erg = []

            for k1, v1 in v.items():
                if k1 != "ProductType":
                    erg.append(round(v1, 4))
                else:
                    erg.append(v1)
            erg_list.append(erg)
        return erg_list

    def getProductList(self):
        erg_list=[]
        header = ["product_name"]
        first_product = list(self.product_kpis.keys())[0]
        header.extend([str(k) for k, v in self.product_kpis[first_product].items()])
        header.remove("WIP")
        erg_list.append(header)

        for k, v in self.product_kpis.items():
            erg = []
            erg.append(k)

            for k1, v1 in v.items():
                if k1 != "WIP":
                    if k1 != "ProductType":
                        erg.append(round(v1, 4))
                    else:
                        erg.append(v1)

            erg_list.append(erg)

        return erg_list


    def test_object_name_all(self):
        object_list = list(self.summarized_kpis.keys())

        ini_path = "/ontologysim/ProductionSimulation/logger/plot/y_lookup_tabel.ini"
        config_path = PathTest.check_file_path(ini_path)

        # Read from Configuration File
        lookup_conf = init_utilities.Init(config_path)
        lookup_conf.read_ini_file()

        self.time_kpis_look_up = lookup_conf.configs['LookUp']['time']
        self.number_kpis_look_up = lookup_conf.configs['LookUp']['number']
        self.percentage_kpis_look_up = lookup_conf.configs['LookUp']['percentage']

        for i in range(len(self.time_kpis['time'])):
            # chek time
            for kpi_key in self.time_kpis['all'].keys():

                kpi = 0
                kpi_all = 0
                for object_name in object_list:

                    if object_name == "all":
                        kpi_all = self.time_kpis[object_name][kpi_key][i]
                    else:
                        kpi += self.time_kpis[object_name][kpi_key][i]

                    if self.time_kpis[object_name][kpi_key][i] < 0:
                        raise Exception("value negative")

                    if kpi_key in self.percentage_kpis_look_up and self.time_kpis[object_name][kpi_key][i] > 1:
                        print("kpi_error percentage", kpi_key, object_name, self.time_kpis[object_name][kpi_key][i])

                if round(kpi / self.number_of_instances, 6) != round(kpi_all, 6):
                    print("kpi_error", kpi_key, kpi, kpi_all)

        # chek summarized

        for kpi_key in self.summarized_kpis['all'].keys():
            kpi = 0
            kpi_all = 0
            if kpi_key != "ProductType":
                for object_name in object_list:

                    if object_name != "all":
                        kpi += self.summarized_kpis[object_name][kpi_key]
                    else:
                        kpi_all = self.summarized_kpis[object_name][kpi_key]

                    if kpi < 0:
                        raise Exception("value negative")

                if round(kpi / self.number_of_instances, 6) != round(kpi_all, 6):
                    print("kpi_error", kpi_key, kpi, kpi_all)
