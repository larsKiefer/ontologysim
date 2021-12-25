from owlready2 import *

from ProductionSimulation.logger.depreciated_logger.QueueLogger import QueueLogger
from ProductionSimulation.sim.Enum import Label, Queue_Enum, Machine_Enum, Product_Enum
from ProductionSimulation.sim.Machine import Machine
import time


class Queue:
    """
    handles the onto queue
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore
        self.deadlockWaitingTime=1

    def createQueue(self,setting_dict,label,id=-1):
        """
        creates a queue in onto

        :param setting_dict: {dict}
        :param label: str (from enum no number)
        :param id: int, number
        :return: queue onto
        """
        label_id=""
        if  "queue_id" in setting_dict.keys():
            id = setting_dict['queue_id']
            if self.simCore.queue_id<=id:
                self.simCore.queue_id=id+1
        elif id == -1:
            raise Exception("no valid id found")
        else:
            self.simCore.queue_id += 1
        label_id=label+str(id)


        queueInstance = self.simCore.central.queue_class(label_id)


        number_of_postion=setting_dict['number_of_positions']
        distribution_add_dict=setting_dict['add_time']
        distribution_remove_dict=setting_dict['remove_time']

        self.addPositions(queueInstance,number_of_postion)

        distribution_add_onto = self.simCore.distribution.createDistribution(distribution_add_dict,
                                                                             "add_queue" + str(id))
        distribution_remove_onto = self.simCore.distribution.createDistribution(distribution_remove_dict,
                                                                                "remove_queue" + str(
                                                                                    id))

        queueInstance.has_for_add_time.append(distribution_add_onto)
        queueInstance.has_for_remove_time.append(distribution_remove_onto)
        queueInstance.current_size = 0

        queueInstance.size = number_of_postion

        if "location" in setting_dict.keys():
            location_list=setting_dict['location']
            location_onto = self.simCore.location.createLocation(location_list)
        elif "location_onto" in setting_dict.keys():
            location_onto=self.simCore.onto[setting_dict['location_onto']]
        else:
            raise Exception("location not created")

        queueInstance.has_for_queue_location.append(location_onto)

        return queueInstance

    def addPositions(self, queueInstance, number_of_positions):
        """
        adds position onto to queue, creates the positions

        :param queueInstance: onto
        :param number_of_positions: double
        """
        for i in range(number_of_positions):
            positionInstance = self.simCore.position.createPosition()
            queueInstance.has_for_position.append(positionInstance)

    def change(self, event_onto):
        """
        moves product form one position to another (betweent queues)
        when having only one machine queue, the current position gets blocked, when processing

        :param event_onto: onto
        """
        new_position_onto = event_onto.has_for_position_event.__getitem__(0)
        product_onto = event_onto.has_for_product_event.__getitem__(0)
        oldPosition = product_onto.is_position_of.__getitem__(0)
        oldPosition.blockedSpace = 0
        old_queue = oldPosition.is_queue_of.__getitem__(0)
        #print(new_position_onto,product_onto,oldPosition,old_queue)
        if event_onto.additional_type == Queue_Enum.StartProcessStayBlocked.value:
            oldPosition.blockedSpace = 1
        else:
            oldPosition.blockedSpace = 0

        product_onto.blocked_for_machine = 0

        product_onto.is_position_of = []
        new_position_onto.has_for_product.append(product_onto)
        queue = new_position_onto.is_queue_of.__getitem__(0)

        old_queue.current_size -= 1
        queue.current_size += 1
        oldPosition.has_for_product = []

        if event_onto.additional_type == Queue_Enum.RemoveFromTransporter.value:
            product_onto.blocked_for_transporter = 1

        elif event_onto.additional_type == Queue_Enum.AddToTransporter.value:
            product_onto.blocked_for_transporter = 0

        elif event_onto.additional_type == Queue_Enum.EndProcess.value:
            product_onto.blocked_for_transporter = 0

        elif event_onto.additional_type == Queue_Enum.StartProcess.value:
            product_onto.blocked_for_transporter = 1
        elif event_onto.additional_type == Queue_Enum.Default.value:
            product_onto.blocked_for_transporter = 0
        elif event_onto.additional_type == Queue_Enum.StartProcessStayBlocked.value:
            product_onto.blocked_for_transporter = 1
        elif event_onto.additional_type == Queue_Enum.RemoveFromTransporterDeadlock.value:
            product_onto.blocked_for_transporter = 1

            block_event_onto= self.simCore.event.createEvent(event_onto.time+self.deadlockWaitingTime, Product_Enum.EndBlockForTransporter, self.deadlockWaitingTime)
            self.simCore.event.add_product_to_event(block_event_onto,product_onto)


        self.evaluateAddRemove(new_position_onto, oldPosition, event_onto)
        self.simCore.logger.evaluatedInformations([{'type': event_onto.additional_type,
                                                    'old_queue_name': old_queue.name,
                                                    'event_onto_time': event_onto.time,
                                                    'old_queue_current_size': old_queue.current_size,
                                                    'queue_name': queue.name,
                                                    'queue_current_size': queue.current_size,
                                                    'time_diff': event_onto.time_diff,
                                                    'product_name': product_onto.name}])


        self.simCore.event.add_to_logger(event_onto)
        if not (
                event_onto.additional_type == Queue_Enum.RemoveFromTransporter.value and product_onto.has_for_product_state[0].state_name == "sink"):
            self.simCore.event.add_to_short_term_logger(event_onto, new_position_onto)
            self.simCore.event.remove_from_event_list(event_onto)
        else:
            self.simCore.event.remove_from_event_list(event_onto)
            self.simCore.event.store_event(event_onto)

    def create_change(self, part_onto, new_position_onto, time, event_type=Queue_Enum.Default):
        """
        creates event for changing position

        :param part_onto: onto
        :param new_position_onto: onto
        :param time: double
        :param event_type: Queue_Enum type
        :return: double
        """

        queue_onto = new_position_onto.is_queue_of.__getitem__(0)
        add_distribution = queue_onto.has_for_add_time.__getitem__(0)
        remove_distribution = (
            (part_onto.is_position_of.__getitem__(0)).is_queue_of.__getitem__(0)).has_for_remove_time.__getitem__(0)
        add_time = self.simCore.distribution.getTimefromOnto(add_distribution)
        remove_time = self.simCore.distribution.getTimefromOnto(remove_distribution)
        time_diff = round(add_time + remove_time,6)
        time = time_diff + time

        event_onto = self.simCore.event.createEvent(time, Queue_Enum.Change, time_diff)
        self.simCore.event.add_position_to_event(event_onto, new_position_onto)
        self.simCore.event.add_product_to_event(event_onto, part_onto)
        event_onto.additional_type = event_type.value

        new_position_onto.blockedSpace = 1
        part_onto.blocked_for_machine = 1
        part_onto.blocked_for_transporter = 1
        part_onto.queue_input_time = time

        return time

    def create_change_for_start_queue(self, part_onto, new_position_onto, time, transportation_onto=None):
        """
        when starting a new production of a part, creating a change event

        :param part_onto: onto
        :param new_position_onto: onto
        :param time: double
        :param transportation_onto: onto
        """
        event_onto = self.simCore.event.createEvent(time, Queue_Enum.Change, 0)
        event_onto.additional_type = Queue_Enum.StartOfProduction.value
        self.simCore.event.add_position_to_event(event_onto, new_position_onto)
        self.simCore.event.add_product_to_event(event_onto, part_onto)
        self.simCore.product.setStartTime(part_onto, time)
        new_position_onto.blockedSpace = 1
        part_onto.blocked_for_machine = 0
        part_onto.blocked_for_transporter = 0
        new_position_onto.is_queue_of.__getitem__(0).current_size += 1

        self.simCore.logger.evaluatedInformations([{'type': event_onto.additional_type,
                                                    'event_onto_time': event_onto.time,
                                                    'time_diff': event_onto.time_diff,
                                                    'product_name': part_onto.name}])

        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.add_to_short_term_logger(event_onto, new_position_onto)
        self.simCore.event.remove_from_event_list(event_onto)


    def get_free_positions(self, queue_onto):
        """
        get all not blocked positions, blockedSpace == 0

        :param queue_onto: onto
        :return: [position_onto]
        """

        position_list = self.simCore.onto[queue_onto.name].has_for_position
        positions = [position for position in position_list if position.blockedSpace == 0]

        return positions

    def get_number_of_free_positions(self, queue_onto):
        """
        number of not blocked positions, blockedSpace == 0

        :param queue_onto: onto
        :return: double
        """
        position_list = self.simCore.onto[queue_onto.name].has_for_position
        number = len([position for position in position_list if position.blockedSpace == 0])
        return number

    def evaluateAddRemove(self, new_position_onto, oldPosition, event_onto):
        """
        currently the waiting time of machine is set to 10s, when now a part is removed or added to the machine queue,
        the waiting machine gets woken up

        :param new_position_onto: onto
        :param oldPosition: onto
        :param event_onto: onto
        """
        position_label = ""
        position_onto = None
        if event_onto.additional_type == Queue_Enum.AddToTransporter.value:

            position_onto = oldPosition
        elif event_onto.additional_type == Queue_Enum.RemoveFromTransporter.value:

            position_onto = new_position_onto
        else:
            return

        time = event_onto.time
        queue = position_onto.is_queue_of.__getitem__(0)
        if len(queue.is_input_queue_of) > 0:
            machine_list = queue.is_input_queue_of
        elif len(queue.is_output_queue_of) > 0:
            machine_list  = queue.is_output_queue_of
        else:
            machine_list = []

        for machine_onto in machine_list:

            event_list = [event for event in machine_onto.is_machine_event_of if
                          self.simCore.onto[Label.EventList.value + "0"] in event.is_event_list_of]
            #print([(event.name,event.type) for event in machine_onto.is_machine_event_of])
            if len(event_list) == 2:
                if(event_list[0].type==Machine_Enum.Wait.value):
                    wait_event_onto = event_list[0]
                    evaluate_event_onto = event_list[1]
                else:
                    wait_event_onto = event_list[1]
                    evaluate_event_onto = event_list[0]
                old_event_time = wait_event_onto.time
                wait_event_onto.time_diff = wait_event_onto.waiting_time + (time - old_event_time)

                wait_event_onto.time = time
                evaluate_event_onto.time = time

                input_queue_current_size = sum([queue.current_size for queue in machine_onto.has_for_input_queue])
                output_queue_current_size = sum(
                    [self.simCore.queue.get_number_of_free_positions(queue) / queue.size for queue in
                     machine_onto.has_for_output_queue])

                self.simCore.logger.evaluatedInformations([{'type': wait_event_onto.type,
                                                            'time_diff': wait_event_onto.time_diff,
                                                            'event_onto_time': wait_event_onto.time,
                                                            'machine_name': machine_onto.name,
                                                            'input_queue_current_size': input_queue_current_size,
                                                            'output_queue_current_size': output_queue_current_size}])

                self.simCore.event.add_to_logger(wait_event_onto)
                self.simCore.event.remove_from_event_list(wait_event_onto)
                self.simCore.event.store_event(wait_event_onto)


    def transformToDict(self,id):
        """
        transform the onto and the kpis into dict

        :param id: str, label
        :return: {}
        """

        response_dict={}
        if(id=="all"):
            id_list=[queue_onto.name for queue_onto  in self.simCore.onto.search(type=self.simCore.central.queue_class)]
        else:
            id_list=[id]

        for id in id_list:
            queue_onto = self.simCore.onto[id]

            response_dict[queue_onto.name] = {}
            response_dict[queue_onto.name]['size'] = queue_onto.size
            response_dict[queue_onto.name]['current_size'] = queue_onto.current_size
            response_dict[queue_onto.name]["positions"] = [position.name for position in queue_onto.has_for_position]

        return response_dict