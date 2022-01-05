from ontologysim.ProductionSimulation.sim.Enum import Label, Evaluate_Enum, Machine_Enum


class Machine:
    """
    python instance which handles the machine onto
    """

    def __init__(self, simCore):
        """

        """
        self.simCore = simCore
        self.machineController = None

    def addMachineController(self, machineController):
        """
        connects machine instance with controller

        :param machineController: MachineController
        """
        self.machineController = machineController
        machineController.machine = self

    def createMachine(self, machine_dict, process_config_list):
        """
        creates a machine onto

        :param machine_dict: machine dict
        :param process_config_list: process dict
        :return: machine onto
        """
        # add id
        if "machine_id" in machine_dict.keys():
            id = machine_dict['machine_id']
        else:
            raise Exception("machine id not defined")
        machineInstance = self.simCore.central.machine_class(Label.Machine.value + str(machine_dict['machine_id']),
                                                             namespace=self.simCore.onto)
        machineInstance.is_defect_machine = 0
        machineInstance.next_defect_machine = 0
        machineInstance.defect_type_machine = ""

        machineInstance.machine_waiting_time = machine_dict['waiting_time']

        self.addProcess(machineInstance, machine_dict['process'])
        self.addSetup(machineInstance, machine_dict['set_up'])
        self.addProcessQueue(machineInstance, machine_dict['queue_process_id'])
        self.addQueue(machineInstance,machine_dict['queue_input_id'],machine_dict['queue_output_id'])
        self.simCore.machine_id += 1

        event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(), Evaluate_Enum.Machine, 0)
        event_onto.has_for_machine_event = [machineInstance]

        return machineInstance

    def addProcess(self, machineInstance, process_id_list):
        """
        adds a process to machine onto, creates process onto, each machine has it'S own process onto

        :param machineInstance: onto
        :param process_id_list: [process id]
        :param process_config_list: [dict{},]
        """

        for prod_process_dict in process_id_list:
            prod_processInstance = self.simCore.prod_process.createProdProces(prod_process_dict,machineInstance)
            machineInstance.has_for_prodprocess.append(prod_processInstance)

        machineInstance.has_for_last_process.append(machineInstance.has_for_prodprocess[0])


    def addSetup(self, machineInstance, set_up_dict):
        """
        adds setup to machine onto

        :param machineInstance: onto
        :param set_up_dict: dict{}
        """
        for set_up in set_up_dict:

            setUpInstance = self.simCore.central.setup_class(Label.SetUp.value + str(self.simCore.set_up_id))

            self.simCore.set_up_id += 1
            start_process = None
            end_process = None

            for process in machineInstance.has_for_prodprocess:
                process_id=self.simCore.prod_process.getID(process)
                if process_id == set_up["start"]:
                    start_process = process
                if process_id == set_up["end"]:
                    end_process = process

            assert (start_process != None or end_process != None)

            setUpInstance.has_for_start_process.append(start_process)
            setUpInstance.has_for_end_process.append(end_process)
            setUpInstance.has_for_set_up_distribution = [
                self.simCore.distribution.createDistribution(set_up, setUpInstance.name)]

    def addQueue(self, machineInstance, queue_input_id_list, queue_output_id_list):
        """
        adding queue to machine onto, queues must be already created, it does not create new queues

        :param machineInstance: onto
        :param queue_input_id_list: [id,...]
        :param queue_output_id_list: [id,..]
        """
        if(len(queue_input_id_list)== 0 or len(queue_output_id_list)== 0):
            raise Exception("empty queue")


        queue_standard_id_list = list(set(queue_input_id_list).intersection(set(queue_output_id_list)))
        queue_input_id_list = list(set(queue_input_id_list).difference(set(queue_standard_id_list)))
        queue_output_id_list = list(set(queue_output_id_list).difference(set(queue_standard_id_list)))

        for queue_input_id in queue_input_id_list:
            queueInstance = self.simCore.onto[Label.Queue.value + str(queue_input_id)]

            if queueInstance == None:
                raise Exception("queue id is not defined " + str(queue_input_id))
            queueInstance.is_a = [self.simCore.central.inputqueue_class]
            machineInstance.has_for_input_queue.append(queueInstance)

        for queue_output_id in queue_output_id_list:
            queueInstance = self.simCore.onto[Label.Queue.value + str(queue_output_id)]

            if queueInstance == None:
                raise Exception("queue id is not defined " + str(queue_input_id))
            queueInstance.is_a = [self.simCore.central.outputqueue_class]
            machineInstance.has_for_output_queue.append(queueInstance)

        for queue_standard_id in queue_standard_id_list:
            queueInstance = self.simCore.onto[Label.Queue.value + str(queue_standard_id)]

            if queueInstance == None:
                raise Exception("queue id is not defined " + str(queue_input_id))
            queueInstance.is_a = [self.simCore.central.inputqueue_class, self.simCore.central.outputqueue_class]
            machineInstance.has_for_output_queue.append(queueInstance)
            machineInstance.has_for_input_queue.append(queueInstance)


    def addProcessQueue(self, machineInstance, queue_process_id_list):
        """
        adds (not create) the process queue to machine onto, place where the part is processed

        :param machineInstance: onto
        :param queue_process_id_list: [id]
        """

        if len(queue_process_id_list) > 1:
            raise Exception("only one process queue allowed")
        queueInstance = self.simCore.onto[Label.Queue.value + str(queue_process_id_list[0])]
        if queueInstance == None:
            raise Exception("queue id is not defined " + str(queue_process_id_list))
        machineInstance.has_for_queue_process.append(queueInstance)
        queueInstance.is_a = [self.simCore.central.queue_class]
        machineInstance.has_for_machine_location = [
            machineInstance.has_for_queue_process[0].has_for_queue_location[0]]

    def transform_process_id_into_process(self, process_id, machine_onto):
        """
        given label finds the suitable process onto

        :param process_id: str, label
        :param machine_onto: onto
        :return: onto; prod_process
        """

        prod_process_list = machine_onto.has_for_prodprocess
        prod_process = [prod_process for prod_process in prod_process_list if int(self.simCore.prod_process.getID(prod_process)) == int(process_id)]

        return prod_process[0]

    def add_defect(self, machine_onto, defect_onto):
        """
        add a defect onto to machine onto

        :param machine_onto: onto
        :param defect_onto: onto
        """

        machine_onto.has_for_defect_machine.append(defect_onto)

    def setNextDefectTime(self, machine_onto, defect_onto):
        """
        sets the next defect time to the machine onto

        :param machine_onto: onto
        :param defect_onto: onto
        """
        next_defect_time, machine_defect_type = self.simCore.defect.getNextDefectTime(defect_onto)
        next_defect_time += self.simCore.getCurrentTimestep()
        machine_onto.next_defect_machine = next_defect_time
        machine_onto.defect_type_machine = machine_defect_type

    def getAllMachine(self):
        """
        list of all machines, better way would be to use the class central and save their machines

        :return: list of all machine onto
        """
        return self.simCore.onto.search(type=self.simCore.central.machine_class)

    def evaluateDefect(self, event_onto):
        """
        checks if the machine is defect, than the machine service event is created, otherwise,
        the given event will be processed

        :param event_onto: onto
        :return: bool
        """

        if self.simCore.defect.machine_defect_possible:
            machine_onto = event_onto.has_for_machine_event.__getitem__(0)
            time = event_onto.time

            if machine_onto.next_defect_machine <= time:
                machine_onto.is_defect_machine = 1
                machine_onto.next_defect_machine = time
                self.simCore.repair_service_machine.addDefectToService(machine_onto)
                self.simCore.event.store_event(event_onto)
                self.simCore.event.remove_from_event_list(event_onto)
                event_onto = self.simCore.event.createEvent(time, Evaluate_Enum.MachineDefect, 0)
                self.simCore.event.add_machine_to_event(event_onto, machine_onto)
                self.simCore.event.add_service_to_event(event_onto, self.simCore.repair_service_machine.service_onto)

                return True
            else:
                return False
        return False

    def create_set_up(self, process_onto, time):
        """

        :param process_onto:
        :param time:
        :return:
        """
        machine_onto = process_onto.is_prodprocess_of.__getitem__(0)
        last_process_onto = machine_onto.has_for_last_process.__getitem__(0)

        distribution = None
        set_up_list = [set_up for set_up in process_onto.is_end_process_of if
                       last_process_onto in set_up.has_for_start_process]

        for set_up in set_up_list:
            distribution = set_up.has_for_set_up_distribution.__getitem__(0)

        if distribution != None:
            time_diff = self.simCore.distribution.getTimefromOnto(distribution)
            time = time + time_diff
            event_onto = self.simCore.event.createEvent(time, Machine_Enum.SetUp, time_diff)
            self.simCore.event.add_process_to_event(event_onto, process_onto)

        return time

    def set_up(self, event_onto):
        """

        :param event_onto:
        """
        process_onto = event_onto.has_for_process_event.__getitem__(0)
        machine_onto = process_onto.is_prodprocess_of.__getitem__(0)
        machine_onto.has_for_last_process.clear()
        machine_onto.has_for_last_process.append(process_onto)

        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'time_diff': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'machine_name': machine_onto.name}])
        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.store_event(event_onto)

    def create_process(self, product_onto_list, process_onto, time):
        """

        :param product_onto_list:
        :param process_onto:
        :param time:
        :return:
        """
        distributionInstance = process_onto.has_for_prod_distribution.__getitem__(0)
        time_diff = self.simCore.distribution.getTimefromOnto(distributionInstance)
        time = time + time_diff
        event_onto = self.simCore.event.createEvent(time, Machine_Enum.Process, time_diff)
        # position_onto.blockedSpace = 1

        for product_onto in product_onto_list:
            product_onto.blocked_for_machine = 1
            product_onto.blocked_for_transporter = 1
            self.simCore.event.add_product_to_event(event_onto, product_onto)

        self.simCore.event.add_process_to_event(event_onto, process_onto)

        return time

    def wait(self, event_onto):
        """

        :param event_onto:
        """
        machine_onto = event_onto.has_for_machine_event.__getitem__(0)
        input_queue_current_size = sum([queue.current_size for queue in machine_onto.has_for_input_queue])
        output_queue_current_size = sum(
            [self.simCore.queue.get_number_of_free_positions(queue) / queue.size for queue in
             machine_onto.has_for_output_queue])

        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'time_diff': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'machine_name': machine_onto.name,
                                                    'input_queue_current_size': input_queue_current_size,
                                                    'output_queue_current_size': output_queue_current_size}])

        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.store_event(event_onto)

    def createWait(self, waiting_time, time, machine_onto):
        """

        :param waiting_time:
        :param time:
        :param machine_onto:
        :return:
        """
        time_diff = waiting_time
        event_onto = self.simCore.event.createEvent(time_diff + time, Machine_Enum.Wait, time_diff)
        self.simCore.event.add_machine_to_event(event_onto, machine_onto)
        event_onto.waiting_time = waiting_time
        return waiting_time + time

    def process(self, event_onto):
        """

        :param event_onto:
        """
        product_onto_list = event_onto.has_for_product_event
        process_onto = event_onto.has_for_process_event.__getitem__(0)

        if(process_onto.is_prodprocess_of_process[0].combine_process == False):

            self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                        'time_diff': event_onto.time_diff,
                                                        'event_onto_time': event_onto.time,
                                                        'machine_name': process_onto.is_prodprocess_of[0].name,
                                                        'product_name_list': [product_onto.name for product_onto in
                                                                              product_onto_list],
                                                        'meanProcessTime':self.simCore.prod_process.meanProcessTimeDict[process_onto.name]}])

            product_onto = product_onto_list[0]
            product_Type = product_onto_list[0].has_for_product_type.__getitem__(0)

            state_onto = product_onto.has_for_product_state[0]
            product_type_process_onto = state_onto.has_for_prod_type_process_state[0]
            new_state_onto = product_type_process_onto.is_prod_type_process_of_state[0]
            product_onto.has_for_product_state = [new_state_onto]
            #print(new_state_onto,product_type_process_onto,state_onto)
            """
            
            deprecatide (pm4py)
            net = self.simCore.product_type.dict[product_Type.name]
            initial_marking = Marking()
            current_marking_list = [p.marking for p in product_onto_list]

            for c in current_marking_list:
                for p in list(net.places):
                    if str(p) == c:
                        initial_marking[p] = 1
            transitions = semantics.enabled_transitions(net, initial_marking)

            if len(transitions) >= 1:
                for t in transitions:

                    if len(t.in_arcs) == 1 and len(t.out_arcs) == 1:

                        if (str(process_onto.id) == t.label):
                            new_marking = semantics.execute(t, net, initial_marking)

                            product_onto_list.__getitem__(0).marking = str([p for p in new_marking][0])

                            # print(product_onto_list[0].marking)
                        else:
                            pass
                            # raise Exception("wrong set up")
                    else:
                        raise Exception("not implemented, product is combined or disassemble")
            else:
                raise Exception("not implemented, product is finished")
            """


            self.simCore.event.add_to_logger(event_onto)
            self.simCore.event.remove_from_event_list(event_onto)
            self.simCore.event.store_event(event_onto)

        else:
            # TODO need change if combine

            self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                        'time_diff': event_onto.time_diff,
                                                        'event_onto_time': event_onto.time,
                                                        'machine_name': process_onto.is_prodprocess_of[0].name,
                                                        'product_name_list': [product_onto.name for product_onto in
                                                                              product_onto_list],
                                                        'meanProcessTime': self.simCore.prod_process.meanProcessTimeDict[
                                                            process_onto.name]}])



            self.simCore.event.add_to_logger(event_onto)
            self.simCore.event.remove_from_event_list(event_onto)
            self.simCore.event.store_event(event_onto)

    def transformToDict(self,id ):
        """
        transform to dict of one machine, or all
        :param id: label string
        :return:
        """

        response_dict={}
        if(id=="all"):
            machine_list=[machine_onto for machine_onto  in self.simCore.onto.search(type=self.simCore.central.machine_class)]
        else:
            machine_list=[self.simCore.onto[id]]
        if machine_list==[None]:
            return {'error':"id_not_found"}
        for machine_onto in machine_list:

            response_dict[machine_onto.name]={}
            response_dict[machine_onto.name]['input_queue']=[queue_onto.name for queue_onto in machine_onto.has_for_input_queue ]
            response_dict[machine_onto.name]['output_queue']=[queue_onto.name for queue_onto in machine_onto.has_for_output_queue ]
            response_dict[machine_onto.name]['process_queue']=[queue_onto.name for queue_onto in machine_onto.has_for_queue_process ]
            response_dict[machine_onto.name]['location'] = self.simCore.location.transformToDict(machine_onto.has_for_machine_location[0].name)
            response_dict[machine_onto.name]['prod_process']={}
            for prod_process in machine_onto.has_for_prodprocess:

                distribution_dict=self.simCore.distribution.transformToDict(prod_process.has_for_prod_distribution[0].name)
                del(distribution_dict['label'])

                response_dict[machine_onto.name]['prod_process'][prod_process.name]={'label':prod_process.name,**distribution_dict}


        return response_dict
