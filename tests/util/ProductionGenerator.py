import ast
import configparser
import math

from tests.util.Generator import Generator


class ProductionGenerator(Generator):
    """
    Production generator
    """
    def __init__(self, seedParameter):
        """

        :param seedParameter: int
        """
        super().__init__(seedParameter)
        self.queue_id=0

    def createConfigDict(self,lvl=""):
        """
        main entry point for creating config data

        :param lvl: string: optional
        :return: configparser object
        """

        production_config = configparser.ConfigParser()
        if lvl == "":
            lvl = "lvl" + str(round(self.randomDistribution.random() * 10) % 3 + 1)


        production_config["Type"] = self.addType(lvl)
        production_config["Process"] = self.addProcess(lvl)
        production_config["ProductType"] = self.addProductType(lvl, ast.literal_eval(
            production_config["Process"]["settings"]))
        machineDict = self.addMachine(lvl, ast.literal_eval(production_config["Process"]["settings"]))
        production_config["Machine"] = machineDict

        production_config["Task"] = self.addTask(lvl, ast.literal_eval(production_config["ProductType"]["settings"]))
        if(lvl=="lvl1"):
            production_config["Transporter"] = self.addTransporter(lvl,machineDict["queue_dict"])
            production_config["Process"] = self.adjustProcess(production_config["Machine"], production_config["Process"])

        else:
            production_config["Transporter"] = self.addTransporter(lvl)
        production_config["Defect"] = self.addDefect(lvl)
        production_config["Repair"] = self.addRepair(lvl)
        production_config["Start_Queue"] = self.addSpecialQueue(lvl, "Start_Queue")
        production_config["End_Queue"] = self.addSpecialQueue(lvl, "End_Queue")
        production_config["DeadLock_Queue"] = self.addSpecialQueue(lvl, "DeadLock_Queue")
        production_config["ChangeTime"] = self.addChangeTime(lvl)
        production_config["RandomSeed"] = self.addRandomSeed(lvl)

        return production_config


    def addProcess(self, lvl):
        """
        defines process data

        :param lvl: string
        :return: dict
        """

        config = {}
        config["settings"] = []

        if(lvl=="lvl1"):
            numberOfProcesses = self.randomDistribution.randint(3, 7)
            for i in range(numberOfProcesses):
                mean = round(self.randomDistribution.random() * 10, 2)
                deviation = self.randomDistribution.randint(0, 5)

                config["settings"].append({"id": i, 'default':{"mean": mean, "deviation": deviation, "type": "normal"}}
                                           )
        else:
            numberOfProcesses = self.randomDistribution.randint(3, 7)
            for i in range(numberOfProcesses):
                mean = round(self.randomDistribution.random() * 10, 2)
                deviation = self.randomDistribution.randint(0, 5)
                config["settings"].append({"id": i, "mean": mean, "deviation": deviation, "type": "normal"})

        return config

    def addProductType(self, lvl, processConfigList):
        """
        define product type data

        :param lvl: string
        :param processConfigList: list
        :return: dict
        """
        config = {}
        config["settings"] = []
        numberOfProductType = self.randomDistribution.randint(1, 4)

        for i in range(0, numberOfProductType):

            productTypeList = []
            numberOfPaths = self.randomDistribution.randint(1, 3)
            for b in range(numberOfPaths):
                productTypeList.append([self.randomDistribution.randint(0, len(processConfigList) - 1) for b in
                                        range(self.randomDistribution.randint(2, 5))])
            config["settings"].append({"id": i, "config": productTypeList})

        return config

    def addMachine(self, lvl, flatProcessList):
        """
        define machine data

        :param lvl: string
        :param flatProcessList: list of process id
        :return: dict
        """
        config = {}
        number_of_machines = self.randomDistribution.randint(2, 10)
        config["number_of_machines"] = number_of_machines
        config["settings"] = []

        distributeProcess = []
        for i in range(number_of_machines):
            distributeProcess.append([])

        #distribute Processes to machines randomly
        i = 0
        for b in range(math.ceil(number_of_machines / len(flatProcessList)) + 1):
            for process_id in range(len(flatProcessList)):
                distributeProcess[i % number_of_machines].append(process_id)
                i += 1

        # number of additional processes
        for i in range(self.randomDistribution.randint(1, 4)):
            for process_id in range(len(flatProcessList)):
                if (self.randomDistribution.random() > 0.5):
                    distributeProcess[math.floor(self.randomDistribution.random() * number_of_machines)].append(
                        process_id)

        for i, processList in enumerate(distributeProcess):
            distributeProcess[i] = list(set(processList))


        if (lvl == "lvl1"):

            location_x = 0
            location_y = 0

            queue_process_dict = []
            machine_dict = []
            queue_dict = []

            numberOfQueues = (int)(abs(self.randomDistribution.normal(number_of_machines, 2))) + 3
            for b in range(numberOfQueues):
                queueConfig = {"queue_id": self.queue_id, "number_of_positions": self.randomDistribution.randint(1, 5),
                               'location': [self.randomDistribution.randint(0, 10), 5, 0]}
                queueConfig["add_time"] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                           'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'}
                queueConfig["remove_time"] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                              'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'}
                queue_dict.append(queueConfig)
                self.queue_id += 1


            for i in range(number_of_machines):

                queue_process_id = self.queue_id
                queue_process_dict.append({
                    "queue_id": queue_process_id, "number_of_positions": 1, "location": [location_x, location_y, 0],
                    "add_time": {'mean': round(self.randomDistribution.random() * 2, 2),
                                 'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'},
                    "remove_time": {'mean': round(self.randomDistribution.random() * 2, 2),
                                    'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'}
                })

                self.queue_id += 1

                machineConfig = {
                    "machine_id": i, "waiting_time": self.randomDistribution.randint(1, 5),
                    "queue_process_id": [queue_process_id],
                    "process": distributeProcess[i], "location": [location_x, location_y, 0]
                }

                machineConfig["set_up"] = []
                for from_process in distributeProcess[i]:
                    for to_process in distributeProcess[i]:

                        if (from_process == to_process):
                            machineConfig["set_up"].append({'start': from_process, 'end': to_process,
                                                            'mean': round(self.randomDistribution.random(), 1),
                                                            'deviation': round(self.randomDistribution.random(), 1),
                                                            'type': 'normal'})
                            machineConfig["set_up"].append({'start': to_process, 'end': from_process,
                                                            'mean': round(self.randomDistribution.random(), 1),
                                                            'deviation': round(self.randomDistribution.random(), 1),
                                                            'type': 'normal'})

                numberOfInputQueues = int(abs(self.randomDistribution.normal(0, 0.5)))+1
                numberOfOutputQueues = int(abs(self.randomDistribution.normal(0, 0.5)))+1
                machineConfig["queue_output_id"] = []
                machineConfig["queue_input_id"] = []
                for input in range(numberOfInputQueues):
                    machineConfig["queue_input_id"].append(
                        queue_dict[self.randomDistribution.randint(0, numberOfQueues - 1)]["queue_id"])
                for output in range(numberOfOutputQueues):
                    machineConfig["queue_output_id"].append(
                        queue_dict[self.randomDistribution.randint(0, numberOfQueues - 1)]["queue_id"])

                machineConfig["queue_output_id"] = list(set(machineConfig["queue_output_id"]))
                machineConfig["queue_input_id"] = list(set(machineConfig["queue_input_id"]))

                if ((i + 1) % int(math.sqrt(number_of_machines)) == 0):
                    location_y += 10
                else:
                    location_x += 10

                machine_dict.append(machineConfig)

            config["machine_dict"] = machine_dict
            config["queue_dict"] = queue_dict
            config["queue_process_dict"] = queue_process_dict


        elif (lvl == "lvl2"):
            location_x = 0
            location_y = 0
            for i in range(number_of_machines):
                machineDict = {"number_of_positions": self.randomDistribution.randint(1, 6),
                               "process": distributeProcess[i],
                               "location": [location_x, location_y, 0]}
                if ((i + 1) % int(math.sqrt(number_of_machines)) == 0):
                    location_y += 10
                else:
                    location_x += 10

                machineDict["set_up"] = []
                for from_process in distributeProcess[i]:
                    for to_process in distributeProcess[i]:

                        if (from_process == to_process):
                            machineDict["set_up"].append({'start': from_process, 'end': to_process,
                                                          'mean': round(self.randomDistribution.random(), 1),
                                                          'deviation': round(self.randomDistribution.random(), 1),
                                                          'type': 'normal'})
                            machineDict["set_up"].append({'start': to_process, 'end': from_process,
                                                          'mean': round(self.randomDistribution.random(), 1),
                                                          'deviation': round(self.randomDistribution.random(), 1),
                                                          'type': 'normal'})

                machineDict["add_time"] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                           'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'}
                machineDict["remove_time"] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                              'deviation': round(self.randomDistribution.random(), 2), 'type': 'normal'}

                machineDict['queue_type'] = "standard"
                machineDict['number_of_queue'] = 1

                config["settings"].append(machineDict)

        elif (lvl == "lvl3"):
            location_x = 0
            location_y = 0
            for i in range(number_of_machines):
                config["settings"].append(
                    {"number_of_positions": self.randomDistribution.randint(1, 6), "process": distributeProcess[i],
                     "location": [location_x, location_y, 0]})
                if ((i + 1) % int(math.sqrt(number_of_machines)) == 0):
                    location_y += 10
                else:
                    location_x += 10

        return config

    def adjustProcess(self,machineDict,processDict):
        """
        adjust process for lvl1 config files

        :param machineDict: string: dict of machine data
        :param processDict: string dict of process data
        :return: dict
        """
        processList = ast.literal_eval(processDict["settings"])

        machineList = ast.literal_eval(machineDict["machine_dict"])

        for machine in machineList:

            machineId = machine["machine_id"]
            processMachineList = machine["process"]

            for processMachineID in processMachineList:
                i=0
                if(self.randomDistribution.random()>0.5):
                    for process in processList:
                        if(process["id"] == processMachineID):
                            if(processList[i].keys() != "adjusted"):
                                processList[i]["adjusted"] = []
                            adjustedMachine={}
                            adjustedMachine["machine_id"] = machineId
                            mean = processList[i]["default"]["mean"]*(10+self.randomDistribution.random())/10
                            deviation = processList[i]["default"]["deviation"]*(10+self.randomDistribution.random())/10
                            adjustedMachine["mean"] = mean
                            adjustedMachine["deviation"] = deviation
                            adjustedMachine["type"] = "normal"
                            processList[i]["adjusted"].append(adjustedMachine)

                        i+=1
        processDict = {"settings":processList}
        return processDict

    def addTask(self, lvl, productTypeList):
        """
        define task
        :param lvl: string
        :param productTypeList: list
        :return: dict
        """
        config = {}
        config["settings"] = []

        for productType in productTypeList:
            for type in ["start", "logging", "end"]:
                if (type == "start" or type == "end"):
                    config["settings"].append({'product_type': productType["id"], 'number_of_parts': 10, "type": type})
                else:
                    config["settings"].append({'product_type': productType["id"],
                                               'number_of_parts': self.randomDistribution.randint(10, 15) * 10,
                                               "type": type})

        return config

    def addTransporter(self, lvl,machine_queue_list=None):
        """
        define transporter

        :param lvl: string
        :param machine_queue_list: list
        :return: dict
        """
        config = {}
        numberOfTransporter = self.randomDistribution.randint(2, 7)
        config["number_of_transporter"] = numberOfTransporter
        if lvl == "lvl3":
            config["settings"] = {'number_of_positions': self.randomDistribution.randint(1, 5),
                                  'speed': self.randomDistribution.randint(2, 5)}
        elif lvl == "lvl2" :
            numberStartPositions = self.randomDistribution.randint(1, 3)
            config["start_location"] = [{"id": i, "location": [i * 10, 0, 0]} for i in range(numberStartPositions)]
            config["settings"] = []
            for i in range(numberOfTransporter):
                transporterSetting = {}
                transporterSetting["number_of_positions"] = int((self.randomDistribution.random() * 5 + 1))
                transporterSetting["location_id"] = math.ceil(
                    self.randomDistribution.random() * numberStartPositions) % numberStartPositions
                transporterSetting['speed'] = self.randomDistribution.randint(2, 5)
                transporterSetting['add_time'] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                                  'deviation': round(self.randomDistribution.random(), 2),
                                                  'type': 'normal'}
                transporterSetting['remove_time'] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                                     'deviation': round(self.randomDistribution.random(), 2),
                                                     'type': 'normal'}

                config["settings"].append(transporterSetting)
        elif lvl == "lvl1":
            numberStartPositions = self.randomDistribution.randint(1, 3)
            config["start_location"] = [{"id": i, "location": [i * 10, 0, 0]} for i in range(numberStartPositions)]
            config["settings"] = []
            for i in range(numberOfTransporter):
                transporterSetting = {}
                transporterSetting["number_of_positions"] = int((self.randomDistribution.random() * 5 + 1))
                transporterSetting["location_id"] = math.ceil(
                    self.randomDistribution.random() * numberStartPositions) % numberStartPositions
                transporterSetting['speed'] = self.randomDistribution.randint(2, 5)
                transporterSetting['waiting_time'] = self.randomDistribution.randint(1,5)
                transporterSetting['add_time'] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                                  'deviation': round(self.randomDistribution.random(), 2),
                                                  'type': 'normal'}
                transporterSetting['remove_time'] = {'mean': round(self.randomDistribution.random() * 2, 2),
                                                     'deviation': round(self.randomDistribution.random(), 2),
                                                     'type': 'normal'}


                routeType = self.randomDistribution.randint(0,2)
                if routeType==0 or i == 0:
                    transporterSetting['route'] = {'type': 'free'}
                elif routeType==1:
                    numberOfQueues = int(abs(self.randomDistribution.normal(2,len(machine_queue_list))))
                    queueList = []
                    for b in range(numberOfQueues):
                        queuePosition = self.randomDistribution.randint(0,len(machine_queue_list)) % len(machine_queue_list)
                        queueList.append(machine_queue_list[queuePosition]["queue_id"])
                    queueList = list(set(queueList))
                    transporterSetting['route'] = {'type': 'restricted', 'queue_list': queueList}
                else:
                    numberOfQueues = self.randomDistribution.randint(2, len(machine_queue_list))
                    queueList = []
                    for b in range(numberOfQueues):
                        queueList.append(machine_queue_list[
                                             self.randomDistribution.randint(0, len(machine_queue_list) - 1) % len(
                                                 machine_queue_list)]["queue_id"])
                    transporterSetting['route'] = {'type': 'restricted', 'queue_list': queueList}


                config["settings"].append(transporterSetting)


        return config

    def addSpecialQueue(self, lvl, queue_type):
        """
        define special queues: start queue, end queue, deadlock queue

        :param lvl: string
        :param queue_type: string: either Start_Queue, End_Queue, Deadlock_Queue
        :return:
        """
        config = {}
        if lvl == "lvl3":
            pass

        else:
            config["number_of_queue"] = 1


            if queue_type == "Start_Queue":
                numberOfPositions = self.randomDistribution.randint(2, 5)
                config["settings"] = [{'location': [0, 0, 0], 'number_of_positions': numberOfPositions,
                                       'add_time': {'mean': round(self.randomDistribution.random(), 2),
                                                    'deviation': round(self.randomDistribution.random(), 2),
                                                    'type': 'normal'},
                                       'remove_time': {'mean': round(self.randomDistribution.random(), 2),
                                                       'deviation': round(self.randomDistribution.random(), 2),
                                                       'type': 'normal'}}]
            elif queue_type == "End_Queue":
                config["settings"] = [{'location': [0, 0, 0],
                                       'add_time': {'mean': round(self.randomDistribution.random(), 2),
                                                    'deviation': round(self.randomDistribution.random(), 2),
                                                    'type': 'normal'},
                                       'remove_time': {'mean': round(self.randomDistribution.random(), 2),
                                                       'deviation': round(self.randomDistribution.random(), 2),
                                                       'type': 'normal'}}]

            elif queue_type == "DeadLock_Queue":
                numberOfPositions = self.randomDistribution.randint(1, 5)
                config["settings"] = [{'location': [0, 0, 0], 'number_of_positions': numberOfPositions,
                                       'add_time': {'mean': round(self.randomDistribution.random(), 2),
                                                    'deviation': round(self.randomDistribution.random(), 2),
                                                    'type': 'normal'},
                                       'remove_time': {'mean': round(self.randomDistribution.random(), 2),
                                                       'deviation': round(self.randomDistribution.random(), 2),
                                                       'type': 'normal'}}]
                config["deadlock_waiting_time"] = self.randomDistribution.randint(5, 10)

            if lvl == "lvl1" and queue_type != "DeadLock_Queue":
                config["settings"][0]["queue_id"] = self.queue_id
                self.queue_id+=1

        return config

    def addChangeTime(self, lvl):
        """
        define change time (default time for all machines and transporter, only lvl 3

        :param lvl: string
        :return: dict
        """
        config = {}
        if lvl == "lvl3":
            config["set_up_time"] = round(self.randomDistribution.random() / 2, 1)
            config["add_time"] = round(self.randomDistribution.random() / 2, 1)
            config["remove_time"] = round(self.randomDistribution.random() / 2, 1)
            config["deviation"] = round(self.randomDistribution.random(), 1)
        else:
            pass

        return config

    def addDefect(self, lvl):
        """
        define defect

        :param lvl: string
        :return: dict
        """
        config = {}

        if lvl == "lvl3":
            transporter_defect_possible = bool(round(self.randomDistribution.random() + 0.2))
            machine_defect_possible = bool(round(self.randomDistribution.random() + 0.2))
            config["transporter_defect_possible"] = transporter_defect_possible
            config["machine_defect_possible"] = machine_defect_possible

            config["transporter_normal"] = {
                'defect': {'type': "normal", 'mean': self.randomDistribution.randint(0, 3) * 500,
                           'deviation': self.randomDistribution.randint(0, 5) * 50},
                'repair': {'mean': self.randomDistribution.randint(0, 3) * 10,
                           'deviation': int(self.randomDistribution.random() * 10), 'type': "normal"}}
            config["machine_normal"] = {
                'defect': {'type': "normal", 'mean': self.randomDistribution.randint(0, 3) * 500,
                           'deviation': self.randomDistribution.randint(0, 5) * 50},
                'repair': {'mean': self.randomDistribution.randint(0, 3) * 10,
                           'deviation': int(self.randomDistribution.random() * 10), 'type': "normal"}}
        elif lvl == "lvl2" or lvl == "lvl1":
            transporter_defect_possible = bool(round(self.randomDistribution.random() + 0.3))
            machine_defect_possible = bool(round(self.randomDistribution.random() + 0.3))
            config["transporter_defect_possible"] = transporter_defect_possible
            config["machine_defect_possible"] = machine_defect_possible
            numberTransporterDefects = self.randomDistribution.randint(1, 3)
            config["transporter_random"] = {'type': "random", 'min': 0, 'max': numberTransporterDefects - 1}
            transporter_normal = []
            for i in range(numberTransporterDefects):
                transporter_normal.append({'defect_type': str(i), 'defect': {'type': "normal",
                                                                             'mean': self.randomDistribution.randint(0,
                                                                                                                     3) * 500,
                                                                             'deviation': self.randomDistribution.randint(
                                                                                 0, 5) * 50},
                                           'repair': {'mean': self.randomDistribution.randint(0, 3) * 10,
                                                      'deviation': int(self.randomDistribution.random() * 10),
                                                      'type': "normal"}})
            config["transporter_normal"] = transporter_normal

            numberMachineDefects = self.randomDistribution.randint(1, 3)
            config["machine_random"] = {'type': "random", 'min': 0, 'max': numberMachineDefects - 1}
            machine_normal = []
            for i in range(numberMachineDefects):
                machine_normal.append({'defect_type': str(i), 'defect': {'type': "normal",
                                                                         'mean': self.randomDistribution.randint(
                                                                             0, 3) * 500,
                                                                         'deviation': self.randomDistribution.randint(
                                                                             0, 5) * 50},
                                       'repair': {'mean': self.randomDistribution.randint(0, 3) * 10,
                                                  'deviation': int(self.randomDistribution.random() * 10),
                                                  'type': "normal"}})
            config["machine_normal"] = machine_normal

        return config

    def addRepair(self, lvl):
        """
        define repair

        :param lvl: string
        :return: dict
        """
        config = {}
        config["machine_repair"] = self.randomDistribution.randint(1, 3)
        config["transporter_repair"] = self.randomDistribution.randint(1, 3)

        return config

    def addRandomSeed(self, lvl):
        """
        define random seed

        :param lvl: string
        :return: dict
        """
        config = {}
        config["AppendValue"] = self.randomDistribution.randint(1, 10)
        return config
