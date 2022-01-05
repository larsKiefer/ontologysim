import csv
import math

from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Type_Enum
from ontologysim.ProductionSimulation.utilities import init_utilities
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


class SubLogger:
    """
    parent class for all kpi loggers,
    task: saving, calculation and handling of kpis
    """

    def __init__(self, logger):
        """

        :param logger:
        """

        self.summarized_kpis = {}
        self.time_kpis = {}
        self.logger = logger

        self.last_time_intervall = 0

        self.number_of_instances = 0
        self.start_logging_multiple = 0

        self.update_list = []

        self.time_kpis_look_up = []
        self.number_kpis_look_up = []
        self.percentage_kpis_look_up = []

        self.type = Logger_Type_Enum.Not

    def addElement(self, dict_element):
        """
        interface to the logger, all data from the simulation are provided through this class

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        """
        pass

    def finale_evaluate(self, time):
        """
        when the logging ends, a last evaluation must be calculated

        :param time:
        :return:
        """


    def checkStartTimeLogging(self,dict_element):
        """
        checks if the event has taken place before the starting time

        :param dict_element: {'type','time_diff','event_onto_time',...............}
        :return: dict element
        """
        time_diff = dict_element['time_diff']
        time = dict_element['event_onto_time']
        if time - time_diff <= self.logger.start_time_logging:
            dict_element['time_diff'] = time-self.logger.start_time_logging
        return dict_element

    def initSubLogger(self, dict_element):
        """
        initializing of sub_logger

        :param dict_element: information from config
        """
        pass

    def addTimeElement(self, object_name, kpi_key_list, time, time_diff):
        """
        adds a new value to the time element (time intervall)

        :param object_name: label
        :param kpi_key_list: [KPI's name]
        :param time: double
        :param time_diff: double
        :return:
        """

        split_time_dict = self.split_time(time, time_diff)
        self.update_list.extend(list(split_time_dict.keys()))

        for k, v in split_time_dict.items():
            for kpi_key in kpi_key_list:
                # if object_name=="m4" and kpi_key=="APT":
                #    print(interval_offset, len(self.time_kpis["time"]),self.time_kpis["time"][-(i+interval_offset+1)])
                #    print(time,time_diff,current_time_element,-(i+interval_offset+1),i)
                # print(current_time_element,time,time_diff,-(i+interval_offset+1),self.time_kpis[object_name][kpi_key])
                time_intervall_diff = v['time_diff']
                self.time_kpis[object_name][kpi_key][k] += time_intervall_diff / self.logger.time_intervall

                self.time_kpis["all"][kpi_key][
                    k] += time_intervall_diff / self.logger.time_intervall / self.number_of_instances

        """   
        for i in range(0,number_of_time_intervals+1):
            self.update_list.append(len(self.time_kpis["time"])-(i+interval_offset+1))
            if i!=number_of_time_intervals:
                current_time_element= later_time_element-time_multiple*self.logger.time_intervall
                remaining_time_diff=remaining_time_diff-current_time_element
                later_time_element= later_time_element-current_time_element
            else:
                current_time_element=remaining_time_diff


            for kpi_key in kpi_key_list:
                #if object_name=="m4" and kpi_key=="APT":
                #    print(interval_offset, len(self.time_kpis["time"]),self.time_kpis["time"][-(i+interval_offset+1)])
                #    print(time,time_diff,current_time_element,-(i+interval_offset+1),i)
                # print(current_time_element,time,time_diff,-(i+interval_offset+1),self.time_kpis[object_name][kpi_key])

                self.time_kpis[object_name][kpi_key][-(i+interval_offset+1)]+=current_time_element/self.logger.time_intervall

                self.time_kpis["all"][kpi_key][-(i+interval_offset+1)]+=current_time_element/self.logger.time_intervall/self.number_of_instances

            time_multiple-=1
        """

    def addNewTimeElement(self, object_list, kpi_list, time):
        """
        inserting a new time element (time intervall)

        :param object_list: [label list]
        :param kpi_list: [kpi name]
        :param time: double
        """
        time_index = int(math.floor(time / self.logger.time_intervall) - self.start_logging_multiple)

        time_len = len(self.time_kpis['time'])
        for i in range(time_index - time_len + 1):
            for object_name in object_list:
                for kpi in kpi_list:
                    self.time_kpis[object_name][kpi].append(0)

            for kpi in kpi_list:
                self.time_kpis["all"][kpi].append(0)

    def split_time(self, time, time_diff):
        """
        split the the given time into the different time intervalls

        :param time:
        :param time_diff:
        :return: {'start_time', 'end_time':, 'time_diff'}
        """

        erg = {}
        if time > self.logger.start_time_logging:

            end_time = time
            start_time = time - time_diff

            if time % self.logger.time_intervall != 0:
                next_intervall = math.floor((time) / self.logger.time_intervall) * self.logger.time_intervall
                number_of_time_intervals = math.floor((time) / self.logger.time_intervall) - math.floor(
                    (time - time_diff) / self.logger.time_intervall)
                if number_of_time_intervals != 0:
                    number_of_time_intervals += 1

            else:
                next_intervall = time - self.logger.time_intervall
                number_of_time_intervals = math.floor((time) / self.logger.time_intervall) - math.floor(
                    (time - time_diff) / self.logger.time_intervall)

                if time_diff < self.logger.time_intervall:
                    number_of_time_intervals -= 1
            current_time_diff = time_diff

            if number_of_time_intervals == 0:
                if start_time < self.logger.start_time_logging:
                    start_time = self.logger.start_time_logging
                    current_time_diff = end_time - start_time

                id = int(next_intervall / self.logger.time_intervall) - self.start_logging_multiple
                erg = {id: {'start_time': start_time, 'end_time': end_time, 'time_diff': current_time_diff}}

            else:
                end_logging = False
                for i in range(number_of_time_intervals):
                    id = int(next_intervall / self.logger.time_intervall) - self.start_logging_multiple
                    if i != number_of_time_intervals - 1:
                        current_time_diff = end_time - next_intervall
                    else:
                        current_time_diff = end_time - start_time

                    start_time = end_time - current_time_diff
                    if start_time < self.logger.start_time_logging:
                        start_time = self.logger.start_time_logging
                        current_time_diff = end_time - start_time
                        end_logging = True
                    erg[id] = {'start_time': start_time, 'end_time': end_time, 'time_diff': current_time_diff}

                    end_time = start_time
                    next_intervall -= self.logger.time_intervall
                    time_diff -= current_time_diff
                    start_time -= time_diff

                    if end_logging:
                        break

        return erg

    def update_basic_kpis(self):
        """
        calculates the basic kpi's
        """
        pass

    def addTimeSumElement(self, object_name, kpi_key_list, time, time_diff):
        """
        used when adding a number and not a time

        :param object_name: label
        :param kpi_key_list:  [kpi name]
        :param time: double
        :param time_diff: double
        :return:
        """

        split_time_dict = self.split_time(time, time_diff)

        for k, v in split_time_dict.items():
            for kpi_key in kpi_key_list:
                # if object_name=="m4" and kpi_key=="APT":
                #    print(interval_offset, len(self.time_kpis["time"]),self.time_kpis["time"][-(i+interval_offset+1)])
                #    print(time,time_diff,current_time_element,-(i+interval_offset+1),i)
                # print(current_time_element,time,time_diff,-(i+interval_offset+1),self.time_kpis[object_name][kpi_key])

                self.time_kpis[object_name][kpi_key][k] += 1/len(split_time_dict)

                self.time_kpis["all"][kpi_key][k] += 1 /len(split_time_dict) / self.number_of_instances

    def test_object_name_all(self):
        """
        test method which checks, if the objects calculated together are the equal to the all value
        checks that no kpi is ouf of bounds (negative, percentage<=1)
        needs to be included
        """
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

                    if kpi_key in self.percentage_kpis_look_up and round(self.time_kpis[object_name][kpi_key][i],
                                                                         4) > 1:
                        print("kpi_error percentage", kpi_key, object_name, self.time_kpis[object_name][kpi_key][i])

                if round(kpi / self.number_of_instances, 4) != round(kpi_all, 4):
                    print("kpi_error_time", kpi_key, kpi / self.number_of_instances, kpi_all, self.number_of_instances)

        # chek summarized

        for kpi_key in self.summarized_kpis['all'].keys():
            kpi = 0
            kpi_all = 0

            for object_name in object_list:

                if object_name != "all":
                    kpi += self.summarized_kpis[object_name][kpi_key]
                else:
                    kpi_all = self.summarized_kpis[object_name][kpi_key]

                if kpi < 0:
                    raise Exception("value negative")

                if kpi_key in self.percentage_kpis_look_up and round(self.summarized_kpis[object_name][kpi_key], 4) > 1:
                    print("kpi_error percentage", kpi_key, object_name, self.summarized_kpis[object_name][kpi_key])

            if round(kpi / self.number_of_instances, 4) != round(kpi_all, 4):
                print("kpi_error_sum", kpi_key, kpi / self.number_of_instances, kpi_all)

    def test_time_summary(self):
        """
        test if the time summary is calculated correctly, needs to be included
        """
        object_list = list(self.summarized_kpis.keys())
        for kpi_key in self.summarized_kpis['all'].keys():

            if isinstance(self.summarized_kpis['all'][kpi_key], (int, float, )):
                for object_name in object_list:
                    kpi = sum(self.time_kpis[object_name][kpi_key])
                    kpi_all = self.summarized_kpis[object_name][kpi_key]

                    if round(kpi/((self.logger.end_time_logging-self.logger.start_time_logging)/self.logger.time_intervall),4)!=round(kpi_all,4):
                        print("time and sum kpi are not equal",kpi_key,object_name,kpi/((self.logger.end_time_logging-self.logger.start_time_logging)/self.logger.time_intervall),kpi_all)


    def save(self, path, folder_name, summarized_name):
        """
        method which handles the saving of information to csv or database

        :param path:
        :param folder_name:
        :param summarized_name:
        :return:
        """

        if self.logger.save_config["csv"]:

            self.save_to_csv(path, folder_name, summarized_name)

        if self.logger.save_config["database"]:

            self.save_to_database()

    def save_to_csv(self, path, folder_name, summarized_name):
        """
        saves the time and summarized kpi's, for the time kpi's there is an extra folger created

        :param path: str
        :param folder_name: str
        :param summarized_name: str
        :return:
        """
        if(self.isTimeLogging()):
            path_folder = PathTest.create_new_folder(path, folder_name)

            for k, v in self.time_kpis.items():
                if k != "time":
                    with open(PathTest.check_dir_path(path_folder + "/" + str(k) + "_logger" + ".csv"), "w",
                              newline='') as time_logger:
                        wr = csv.writer(time_logger, delimiter=';',quoting=csv.QUOTE_ALL)

                        erg_list = self.getTimeList(k)
                        wr.writerows(erg_list)

        if (self.isSummaryLogging()):
            with open(PathTest.check_dir_path(path + "/" + summarized_name + ".csv"), "w", newline='') as sum_logger:
                wr = csv.writer(sum_logger, delimiter=';',  quoting=csv.QUOTE_ALL)

                erg_list = self.getSummaryList()
                wr.writerows(erg_list)



    def save_to_database(self):
        """
        save to database, abstract method
        :return:
        """
        pass


    def getTimeList(self,object_key):
        """
        get time list for object key
        :param object_key: string
        :return:
        """
        erg_list = []
        header = ["time"]

        header.extend([str(k) for k, v in self.summarized_kpis['all'].items()])
        erg_list.append(header)

        for i in range(len(self.time_kpis["time"])):
            erg = [self.time_kpis["time"][i]]
            for k1, v1 in self.time_kpis[object_key].items():
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

    def transformToDict(self,id,last_kpi):
        """
        transforms the kpi's to a dict element

        :param id: label
        :param last_kpi: bool, should the last kpi be saved in an extra sub dict
        :return:
        """

        response_dict={}
        for kpi in self.kpi_list:
            response_dict[kpi] = {}

            if len(self.time_kpis[id][kpi])>0:
                last_kpi_value=self.time_kpis[id][kpi][-1]
            else:
                last_kpi_value=0


            response_dict[kpi]['sum_kpi']=self.summarized_kpis[id][kpi]
            response_dict[kpi]['time_kpi']=self.time_kpis[id][kpi]
            if last_kpi:
                response_dict[kpi]['last_kpi']=last_kpi_value


        for kpi in self.basic_kpi_list:
            response_dict[kpi] = {}

            if len(self.time_kpis[id][kpi]) > 0 and last_kpi:
                last_kpi_value = self.time_kpis[id][kpi][-1]
                response_dict[kpi]['last_kpi'] = last_kpi_value

            response_dict[kpi]['sum_kpi'] = self.summarized_kpis[id][kpi]
            response_dict[kpi]['time_kpi'] = self.time_kpis[id][kpi]


        return response_dict

    def isTimeLogging(self):
        """
        chek if time data is logged
        :return:
        """
        if(Logger_Type_Enum.Time.value == self.type or Logger_Type_Enum.All.value == self.type):
            return True

        return False

    def isSummaryLogging(self):
        """
        check if summary data is logged
        :return:
        """
        if (Logger_Type_Enum.Summary.value == self.type or Logger_Type_Enum.All.value == self.type):
            return True

        return False

    def isNotLogging(self):
        """
        check if nothing is logged
        :return:
        """
        if(Logger_Type_Enum.Not.value == self.type):
            return True

        return False
