
from numpy.random import MT19937
from numpy.random import RandomState


from owlready2 import *
from itertools import islice
from ProductionSimulation.sim.Enum import Label, Queue_Enum, Evaluate_Enum
from ProductionSimulation.sim.Machine import Machine


class MachineController:
    """
    the main class for the machine controller
    """

    def __init__(self):
        self.machine = None  # add it over machine.addMachineController

    def addControllerDict(self, controller_dict):
        """
        only used for Hybrid controller, allowes the use of multiple machine controller

        :param controller_dict: dictionary with python_classes
        """
        pass

    def evaluateMachine(self, event_onto):
        """
        entry point into the machine controller

        :param event_onto:
        """
        self.machine.simCore.event.remove_from_event_list(event_onto)

        time = event_onto.time
        machine_onto = event_onto.has_for_machine_event.__getitem__(0)

        self.machine.simCore.event.store_event(event_onto)

        #returns all products on the machine queue in defined order
        erg = self.sort_products(machine_onto)

        process_list = machine_onto.has_for_prodprocess

        machine_process_id_list = [self.machine.simCore.prod_process.getID(process) for process in process_list]
        nothingDone = True

        i=0
        for product in erg:
            product_onto = product[0]

            #get the next processes of the product
            process_id_list = self.machine.simCore.product.getNextProcess(product_onto)
            intersection_list = list(set.intersection(set(process_id_list),
                                                      *islice([set(process_id_list), set(machine_process_id_list)], 1,
                                                              None)))
            if len(intersection_list) > 0:

                process_id = intersection_list[0]
                prod_process_onto = self.machine.transform_process_id_into_process(process_id, machine_onto)

                process_onto = prod_process_onto.is_prodprocess_of_process[0]



                if(process_onto.combine_process and len(erg)>1):

                    output_combine_list = process_onto.has_for_output_combine
                    output_number = sum([output_combine.number_state for output_combine in output_combine_list])
                    input_number = sum([input_combine.number_state for input_combine in process_onto.has_for_input_combine])

                    if(output_number >= sum([self.machine.simCore.queue.get_number_of_free_positions(queue) / queue.size for queue in
                        machine_onto.has_for_output_queue]) and i+input_number<=len(erg)):

                        combine_process_data_list = process_onto.has_for_input_combine
                        config_input_combine = []
                        for combine_process_data_onto in combine_process_data_list:
                            config_input_combine.append({"number": combine_process_data_onto.number_state, "state":combine_process_data_onto.has_for_state_combine_process_data[0]})
                            #print(combine_process_data_onto,combine_process_data_onto.number_state,combine_process_data_onto.has_for_state_combine_process_data)

                        product_list = self.find_suitable_merge_product(erg,i,config_input_combine)

                        if (len(product_list) == 0):
                            #print(product_list)

                            nothingDone = False
                            break

                        #print("combine_process_data_onto",[(combine_process_data_onto,combine_process_data_onto.has_for_state_combine_process_data) for combine_process_data_onto in combine_process_data_list])
                        #print(process_onto,prod_process_onto)
                        #print([(product_element[0] ,product_element[0].has_for_product_type[0] ) for product_element in erg])
                        #print(erg)
                        #nothingDone = False

                    #break
                elif not process_onto.combine_process:

                    old_position_onto = product_onto.is_position_of.__getitem__(0)
                    queue_list = machine_onto.has_for_queue_process
                    position_onto = None
                    for queue in queue_list:
                        position_onto_list = self.machine.simCore.queue.get_free_positions(queue)
                        if len(position_onto_list) > 0:
                            position_onto = position_onto_list.__getitem__(0)
                    if position_onto == None:
                        raise Exception(str(queue) + ", " + str(
                            [(position, position.has_for_product) for position in queue.has_for_position]) + ", " + str(
                            self.machine.simCore.queue.get_free_positions(queue)) )
                    # TODO only for station standard
                    new_position_onto=self.selectOutputQueue(machine_onto,old_position_onto)

                    if old_position_onto.name == new_position_onto.name:
                        time = self.machine.simCore.queue.create_change(product_onto, position_onto, time,
                                                                        Queue_Enum.StartProcessStayBlocked)
                    else:
                        time = self.machine.simCore.queue.create_change(product_onto, position_onto, time,
                                                                        Queue_Enum.StartProcess)
                    time = self.machine.create_set_up(prod_process_onto, time)
                    time = self.machine.create_process([product_onto], prod_process_onto, time)
                    time = self.machine.simCore.queue.create_change(product_onto, new_position_onto, time,
                                                                    Queue_Enum.EndProcess)
                    nothingDone = False
                    break
            i+=1

        if nothingDone:
            time = self.machine.createWait(machine_onto.machine_waiting_time, time, machine_onto)

        event_onto = self.machine.simCore.event.createEvent(time, Evaluate_Enum.Machine, 0)
        event_onto.has_for_machine_event = [machine_onto]

    def find_suitable_merge_product(self, product_erg_list,current_index,combine_input_list):
        """
        TODO currently not needed
        :param product_erg_list:
        :param current_index:
        :param combine_input_list:
        :return:
        """
        product_list=[]
        index_list = [i for i in range(current_index,len(product_erg_list))]
        for combine_element in combine_input_list:
            state_found = False
            for b in index_list:
                product_onto = product_erg_list[b][0]
                state_onto = product_onto.has_for_product_state[0]
                if state_onto.name == combine_element["state"].name:
                    index_list.remove(b)
                    state_found =True
                    product_list.append([b, product_onto])
                    break

            if not state_found:
                return []

        return product_list


    def sort_products(self, machine_onto):
        """
        output of all products in the machine queue
        in the machine controller class, the output is randomly scheduled

        :param machine_onto:
        :return: [[product_onto,time (int)]]
        """
        erg_queue = machine_onto.has_for_input_queue
        erg = []
        for queue in erg_queue:
            position_list = queue.has_for_position
            for position in position_list:
                for product in position.has_for_product:
                    if product.blocked_for_machine == 0 and product.has_for_product_state[0].state_name != "sink":
                        event_list = position.is_position_event_of
                        for event in event_list:
                            if event.type == Queue_Enum.Change.value:
                                erg.append([product, event.time])
        random_state = RandomState(MT19937(1))

        random_state.shuffle(erg)

        return erg

    def selectOutputQueue(self,machineInstance,old_position_onto):
        """
        an output queue n of the machine is determined

        :param machineInstance: onto
        :param old_position_onto: onto
        :return:
        """
        position_onto=None
        queue_list= machineInstance.has_for_output_queue
        if len(queue_list)==1:
            position_onto=old_position_onto
        else:
            erg_list=[] #queue,standard,free_position
            for queue in queue_list:
                isStandard=False
                if len(queue.is_a)==2:
                    isStandard =True

                free_position_list=self.machine.simCore.queue.get_free_positions(queue)
                if len(free_position_list)>0:
                    erg_list.append([queue,isStandard,len(free_position_list),free_position_list])
            erg_list.sort(key=lambda x: x[1])
            erg_list.sort(key=lambda x: x[2],reverse=True)
            if len(erg_list)>0:
                position_onto=erg_list[0][3][0]

            else:
                position_onto = old_position_onto

        return position_onto