from ontologysim.ProductionSimulation.utilities import init_utilities
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


class TransformProductionIni:
    """
    there are multiple config structures available,
    currently lvl2 and lvl1
    lvl1 is the most detailed, all config-files are getting converted to lvl1

    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

    def transform_ini(self, production_ini={}):
        """
        main method, which transform the config-file

        :param production_ini:
        :return:
        """
        output_ini = {}
        type = production_ini['Type']['type']

        if(str(type) != "lvl1" and str(type) != "lvl2" and str(type) != "lvl3"):
            raise Exception("type not defined",type)

        defaultValuesConfig={}
        default_value_path = PathTest.check_file_path_libary("/ProductionSimulation/init/defaultValue.ini")

        defaultValuesConf = init_utilities.Init(default_value_path)
        defaultValuesConf.read_ini_file()
        defaultValuesConfig = defaultValuesConf.configs


        if(type == "lvl3"):

            changeConifg= production_ini["ChangeTime"]

            output_ini['Machine'] = self.transform_machine(type, production_ini['Machine'],defaultValuesConfig,production_ini["ChangeTime"])
            output_ini['Start_Queue'] = self.transform_start_queue(type, {}, defaultValuesConfig["Start_Queue"])
            output_ini['End_Queue'] = self.transform_end_queue(type, {}, defaultValuesConfig["End_Queue"])
            output_ini['DeadLock_Queue'] = self.transform_deadlock_queue(type, {},
                                                                         defaultValuesConfig["DeadLock_Queue"])
            output_ini['ProductType'] = self.transform_product_type(type, production_ini['ProductType'])
            output_ini['Transporter'] = self.transform_transporter(type, production_ini['Transporter'],defaultValuesConfig,production_ini['ChangeTime'])

        else:

            output_ini['Machine'] = self.transform_machine(type, production_ini['Machine'],defaultValuesConfig)
            output_ini['Start_Queue'] = self.transform_start_queue(type, production_ini["Start_Queue"])
            output_ini['End_Queue'] = self.transform_end_queue(type, production_ini["End_Queue"])
            output_ini['DeadLock_Queue'] = self.transform_deadlock_queue(type, production_ini["DeadLock_Queue"],defaultValuesConfig["DeadLock_Queue"])
            output_ini['ProductType'] = self.transform_product_type(type, production_ini['ProductType'])
            output_ini['Transporter'] = self.transform_transporter(type, production_ini['Transporter'],defaultValuesConfig)

        output_ini['Tpye'] = {'type': 'lvl1'}
        output_ini['Task'] = self.transform_task(type, production_ini['Task'])
        output_ini['Process'] = self.transform_process(type, production_ini['Process'])
        output_ini['Defect'] = self.transform_defect(type, production_ini['Defect'],defaultValuesConfig["Distribution"])

        output_ini['Repair'] = self.transform_repair(type, production_ini['Repair'])
        output_ini['RandomSeed'] = self.transform_random_seed(type, production_ini['RandomSeed'])
        return output_ini

    def transform_machine(self, type="lvl2", old_machine_ini_dict={},defaultValues={},changeTime={}):
        """
        transforms the machine input

        :param type:
        :param old_machine_ini_dict:
        :return:
        """
        machine_dict_list = []
        queue_dict_list = []
        queue_process_dict_list = []

        if type == "lvl2":

            old_machine_dict_list = old_machine_ini_dict['settings']
            for old_machine_dict in old_machine_dict_list:

                machine_dict = {}
                queue_dict = {}
                queue_process_dict = {}

                machine_id = self.simCore.machine_id
                queue_id = self.simCore.queue_id
                self.simCore.machine_id += 1
                self.simCore.queue_id += 1
                queue_process_id = self.simCore.queue_id
                self.simCore.queue_id += 1

                machine_dict['machine_id'] = machine_id
                machine_dict['queue_input_id'] = [queue_id]
                machine_dict['queue_output_id'] = [queue_id]
                machine_dict['queue_process_id'] = [queue_process_id]
                machine_dict['process'] = old_machine_dict['process']
                machine_dict['set_up'] = old_machine_dict['set_up']

                if "waiting_time" not in old_machine_dict.keys():
                    machine_dict["waiting_time"] = defaultValues["Machine"]["waiting_time"]
                else:
                    machine_dict['waiting_time'] = old_machine_dict['waiting_time']

                queue_dict['queue_id'] = queue_id
                queue_dict['number_of_positions'] = old_machine_dict['number_of_positions']
                queue_dict['location'] = old_machine_dict['location']
                queue_dict['add_time'] = old_machine_dict['add_time']
                queue_dict['remove_time'] = old_machine_dict['remove_time']

                queue_process_dict['queue_id'] = queue_process_id
                queue_process_dict['number_of_positions'] = 1
                queue_process_dict['location'] = old_machine_dict['location']
                queue_process_dict['add_time'] = old_machine_dict['add_time']
                queue_process_dict['remove_time'] = old_machine_dict['remove_time']

                machine_dict_list.append(machine_dict)
                queue_dict_list.append(queue_dict)
                queue_process_dict_list.append(queue_process_dict)

            self.checkWaitingTimeMachine(machineList = machine_dict_list)
            return {'machine_dict': machine_dict_list, 'queue_process_dict': queue_process_dict_list,
                    'queue_dict': queue_dict_list}
        elif type == "lvl3":


            old_machine_dict_list = old_machine_ini_dict['settings']
            for old_machine_dict in old_machine_dict_list:
                machine_dict = {}
                queue_dict = {}
                queue_process_dict = {}

                machine_id = self.simCore.machine_id
                queue_id = self.simCore.queue_id
                self.simCore.machine_id += 1
                self.simCore.queue_id += 1
                queue_process_id = self.simCore.queue_id
                self.simCore.queue_id += 1

                machine_dict['machine_id'] = machine_id
                machine_dict['queue_input_id'] = [queue_id]
                machine_dict['queue_output_id'] = [queue_id]
                machine_dict['queue_process_id'] = [queue_process_id]
                machine_dict['process'] = old_machine_dict['process']

                process_list = old_machine_dict['process']
                set_up_list=[]
                for process_1 in process_list:
                    for process_2 in process_list:
                        if(process_1 != process_2):
                            set_up_list.append({
                                 "start":process_1,"end":process_2,"mean": changeTime["set_up_time"],"deviation":changeTime["deviation"],"type":defaultValues["Distribution"]["type"]
                                } )

                machine_dict['set_up'] = set_up_list
                machine_dict['waiting_time'] = defaultValues["Machine"]['waiting_time']

                queue_dict['queue_id'] = queue_id
                queue_dict['number_of_positions'] = old_machine_dict['number_of_positions']
                queue_dict['location'] = old_machine_dict['location']

                queue_dict['add_time']= {"mean": changeTime["add_time"], "deviation": changeTime["deviation"],
                             "type": defaultValues["Distribution"]["type"]}
                queue_dict['remove_time'] = {"mean": changeTime["remove_time"], "deviation": changeTime["deviation"],
                                "type": defaultValues["Distribution"]["type"]}


                queue_process_dict['queue_id'] = queue_process_id
                queue_process_dict['number_of_positions'] = 1
                queue_process_dict['location'] = old_machine_dict['location']
                queue_process_dict['add_time'] ={"mean": changeTime["add_time"], "deviation": changeTime["deviation"],
                             "type": defaultValues["Distribution"]["type"]}
                queue_process_dict['remove_time'] = {"mean": changeTime["remove_time"], "deviation": changeTime["deviation"],
                                "type": defaultValues["Distribution"]["type"]}

                machine_dict_list.append(machine_dict)
                queue_dict_list.append(queue_dict)
                queue_process_dict_list.append(queue_process_dict)

            self.checkWaitingTimeMachine(machineList=machine_dict_list)
            return {'machine_dict': machine_dict_list, 'queue_process_dict': queue_process_dict_list,
                    'queue_dict': queue_dict_list}


        elif type == "lvl1":

            self.checkWaitingTimeMachine(machineList=old_machine_ini_dict["machine_dict"])
            return old_machine_ini_dict



    def transform_process(self, type="lvl2", old_process_ini_dict={}):
        """
        transform the process input

        :param type:
        :param old_process_ini_dict:
        :return:
        """
        process_dict = []
        if type == "lvl2" or type == "lvl3":
            old_process_dict = old_process_ini_dict['settings']
            for process in old_process_dict:
                process_dict.append({'id': process['id'],
                                     'default': {'mean': process['mean'], 'deviation': process['deviation'],
                                                 'type': process['type']}})
            return {'settings': process_dict}
        elif type == "lvl1":
            return old_process_ini_dict


    def transform_start_queue(self, type="lvl2", old_start_queue_ini_dict={},default_value_config={}):
        """
        transforms the start queue input

        :param type:
        :param old_start_queue_ini_dict:
        :return:
        """

        if type == "lvl2":
            return old_start_queue_ini_dict
        elif type == "lvl1":
            for setting in old_start_queue_ini_dict["settings"]:
                if(not "queue_id" in setting.keys()):
                    raise Exception(str(setting)+ " not correct defined")
            return old_start_queue_ini_dict
        elif type == "lvl3":
            return default_value_config

    def transform_end_queue(self, type="lvl2", old_end_queue_ini_dict={},default_value_config={}):
        """
        transforms the end queue input

        :param type:
        :param old_end_queue_ini_dict:
        :return:
        """
        if type == "lvl2":
            return old_end_queue_ini_dict
        elif type == "lvl1":
            for setting in old_end_queue_ini_dict["settings"]:
                if(not "queue_id" in setting.keys()):
                    raise Exception(str(setting)+ " not correct defined")
            return old_end_queue_ini_dict
        elif type == "lvl3":
            return default_value_config

    def transform_deadlock_queue(self, type="lvl2", old_deadlock_queue_ini_dict={},default_value_config={}):
        """
        transforms the deadlock queue input

        :param type:
        :param old_deadlock_queue_ini_dict:
        :return:
        """

        if type == "lvl2":
            if(len(old_deadlock_queue_ini_dict.keys())==0):
                new_deadlock_queue_ini_dict = default_value_config
            else:
                if("deadlock_waiting_time" not in old_deadlock_queue_ini_dict.keys()):
                    new_deadlock_queue_ini_dict = old_deadlock_queue_ini_dict
                    new_deadlock_queue_ini_dict['deadlock_waiting_time'] = default_value_config['deadlock_waiting_time']
                else:
                    new_deadlock_queue_ini_dict = old_deadlock_queue_ini_dict
            return new_deadlock_queue_ini_dict
        elif type == "lvl1":
            return old_deadlock_queue_ini_dict
        elif type == "lvl3":
            if (len(old_deadlock_queue_ini_dict.keys()) == 0):
                new_deadlock_queue_ini_dict = default_value_config
            else:
                if ("deadlock_waiting_time" not in old_deadlock_queue_ini_dict.keys()):

                    new_deadlock_queue_ini_dict = old_deadlock_queue_ini_dict
                    new_deadlock_queue_ini_dict['deadlock_waiting_time'] = default_value_config['deadlock_waiting_time']
                else:
                    new_deadlock_queue_ini_dict = old_deadlock_queue_ini_dict


            return new_deadlock_queue_ini_dict

    def transform_product_type(self, type="lvl2", old_product_type_ini_dict={}):
        """
        transforms the product type input

        :param type:
        :param old_product_type_ini_dict:
        :return:
        """
        product_type_dict = {}


        if type == "lvl2":
            return old_product_type_ini_dict
        elif type == "lvl1":
            return old_product_type_ini_dict
        elif type == "lvl3":
            new_product_type_ini_dict={}
            new_product_type_ini_dict["settings"]=old_product_type_ini_dict["settings"]


            return new_product_type_ini_dict


    def transform_transporter(self, type="lvl2", old_transporter_ini_dict={},defaultValues={},changeTime={}):
        """
        transforms the transpoter input

        :param type:
        :param old_transporter_ini_dict:
        :return:
        """
        if type == "lvl2":

            new_transporter_ini_dict = old_transporter_ini_dict
            for setting_dict in new_transporter_ini_dict['settings']:
                if "waiting_time" not in setting_dict.keys():

                    setting_dict["waiting_time"] = defaultValues["Transporter"]["waiting_time"]
                setting_dict['route'] = {'type': 'free'}
            self.checkWaitingTimeTransporter(new_transporter_ini_dict)
            return new_transporter_ini_dict
        elif type == "lvl1":
            self.checkWaitingTimeTransporter(old_transporter_ini_dict)
            return old_transporter_ini_dict

        elif type == "lvl3":
            new_transporter_ini_dict=old_transporter_ini_dict

            new_transporter_ini_dict["start_location"] = defaultValues["Transporter"]["start_location"]

            setting_dict = {"number_of_positions": old_transporter_ini_dict["settings"]["number_of_positions"],
                            "location_id": defaultValues["Transporter"]["start_location"][0]["id"],
                            'route': {'type': 'free'}, "speed": old_transporter_ini_dict["settings"]["speed"],
                            "waiting_time":  defaultValues["Transporter"]["waiting_time"],
                            "add_time": {"mean": changeTime["add_time"], "deviation": changeTime["deviation"],
                                         "type": defaultValues["Distribution"]["type"]},
                            "remove_time": {"mean": changeTime["remove_time"], "deviation": changeTime["deviation"],
                                            "type": defaultValues["Distribution"]["type"]}
                            }
            new_transporter_ini_dict["settings"]=[]
            for i in range(old_transporter_ini_dict["number_of_transporter"]):

                new_transporter_ini_dict["settings"].append(setting_dict)

            self.checkWaitingTimeTransporter(new_transporter_ini_dict)
            return new_transporter_ini_dict

    def checkWaitingTimeTransporter(self,old_transporter_ini_dict):
        """
        test if waiting time >0
        :param old_transporter_ini_dict: dict
        :return:
        """

        for transporterDict in old_transporter_ini_dict["settings"]:
            if(transporterDict["waiting_time"] == 0):
                raise Exception("waiting time is 0")

    def checkWaitingTimeMachine(self,machineList ):
        """
        test if waiting time >0
        :param machineList: list[{},...]
        :return:
        """
        for machineDict in machineList:
            if (machineDict["waiting_time"] == 0):
                raise Exception("waiting time is 0")


    def transform_task(self, type="lvl2", old_task_ini_dict={}):
        """
        transforms the task input

        :param type:
        :param old_task_ini_dict:
        :return:
        """

        task_dict = {}
        if type == "lvl2":
            return old_task_ini_dict
        elif type == "lvl1":
            return old_task_ini_dict
        elif type == "lvl3":
            return old_task_ini_dict

    def transform_defect(self, type="lvl2", old_defect_ini_dict={},default_value_dict={}):
        """
        transforms the defect input

        :param type:
        :param old_defect_ini_dict:
        :return:
        """
        if type == "lvl2":
            return old_defect_ini_dict
        elif type == "lvl1":
            return old_defect_ini_dict

        elif type == "lvl3":

            new_defect_ini_dict = old_defect_ini_dict
            old_defect_ini_dict["transporter_normal"]['defect_type']='standard'
            old_defect_ini_dict["machine_normal"]['defect_type'] = 'standard'
            new_defect_ini_dict["transporter_normal"] = [old_defect_ini_dict["transporter_normal"]]
            new_defect_ini_dict["transporter_random"] = default_value_dict["defect_random"]

            new_defect_ini_dict["machine_normal"] = [old_defect_ini_dict["machine_normal"]]
            new_defect_ini_dict["machine_random"] = default_value_dict["defect_random"]

            return new_defect_ini_dict

    def transform_repair(self, type="lvl2", old_repair_ini_dict={}):
        """
        transforms the repair input

        :param type:
        :param old_repair_ini_dict:
        :return:
        """
        if type == "lvl2":
            return old_repair_ini_dict
        elif type == "lvl1":
            return old_repair_ini_dict
        elif type == "lvl3":
            return old_repair_ini_dict

    def transform_random_seed(self, type="lvl2", old_random_seed_ini_dict={}):
        """
        transforms the random seed

        :param type:
        :param old_random_seed_ini_dict:
        :return:
        """
        if type == "lvl2":
            return old_random_seed_ini_dict
        elif type == "lvl1":
            return old_random_seed_ini_dict
        elif type == "lvl3":
            return old_random_seed_ini_dict