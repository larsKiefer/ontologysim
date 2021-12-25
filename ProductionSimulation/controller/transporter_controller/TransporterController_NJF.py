import operator
from collections import defaultdict

from ProductionSimulation.controller.transporter_controller.TransporterController import TransporterController
from ProductionSimulation.controller.transporter_controller.TransporterController_Enum import Queue_Selection
from ProductionSimulation.sim.Enum import Queue_Enum, Label, Evaluate_Enum


class TransporterController_NJF(TransporterController):
    """
    select the product on the nearest job
    """
    def __init__(self):
        super().__init__()
        self.queue_selection=Queue_Selection.NJF.value

    def sort_products_on_transporter(self, transport_onto):
        """
        sort all products on transporter

        :return: [[product_name,time (int)]]
        """
        event_list = []
        location_transport_onto = transport_onto.has_for_transp_queue[0].has_for_queue_location[0]
        queue_list = transport_onto.has_for_transp_queue

        for queue in queue_list:
            for position in queue.has_for_position:
                for product in position.has_for_product:
                    if product.blocked_for_transporter == 0 and self.transport.end_queue_allowed(transport_onto,product):

                        # event_onto_list=self.transport.simCore.onto.search(has_for_position_event=position,is_event_logger_of=self.transport.simCore.onto[Label.Logger.value+"0"])
                        event_onto_list = [event for event in position.is_position_event_of if
                                           self.transport.simCore.onto[
                                               Label.ShortTermLogger.value + "0"] in event.is_event_short_term_logger_of]

                        process_id_list = self.transport.simCore.product.getNextProcess(product)
                        erg_list = []

                        if len(process_id_list) == 0:
                            queue_onto = self.transport.simCore.central.end_queue_list[0]

                            distance=self.transport.simCore.location.distance_dict[queue_onto.has_for_queue_location[0].name][location_transport_onto.name]
                            for event in event_onto_list:
                                if event.type == Queue_Enum.Change.value:
                                    event_list.append([product.name, event.time, distance, queue_onto])


                        else:
                            for process_id in process_id_list:
                                # [machine_onto,count, process_onto]
                                suitableMachine = self.transport.simCore.product.getSuitableAndAvailableMachine(
                                    process_id)
                                suitableMachine = self.transport.getAlowedMachine(transport_onto, suitableMachine)

                                if len(suitableMachine) > 0:
                                    erg_list.extend(suitableMachine)

                            if len(erg_list) > 0:
                                erg_list.sort(key=lambda x: x[1])
                                machine_is_correct=False
                                for erg in erg_list:

                                    machine_onto = erg[0]
                                    process_onto = erg[2]

                                    position_onto = None
                                    queue_onto = None
                                    for queue_onto in machine_onto.has_for_input_queue:
                                        positions = self.transport.simCore.queue.get_free_positions(queue_onto)

                                        if len(positions) > 0:
                                            # for event in event_onto_list:
                                            distance = self.transport.simCore.location.distance_dict[
                                                queue_onto.has_for_queue_location[0].name][location_transport_onto.name]

                                            for event in event_onto_list:
                                                if event.type == Queue_Enum.Change.value:
                                                    event_list.append([product.name, event.time, distance, queue_onto])
                                                    machine_is_correct=True
                                            break
                                    if machine_is_correct:
                                        break
        #Deadlock detection
        if(len(event_list) ==0):
            if(self.transport.getFreePosition(transport_onto) == None):
                currentTime = self.transport.simCore.getCurrentTimestep()
                for queue in queue_list:
                    for position in queue.has_for_position:
                        for product in position.has_for_product:
                            if product.blocked_for_transporter == 0:
                                event_list.append([product.name, currentTime, 0, None])

                #TODO add free position handling

        event_list.sort(key=lambda x: x[1])

        res = defaultdict(list)

        for k, v, w ,z in event_list: res[k].append([v, w ,z])

        products_on_transporter = [[k, v[-1][0], v[-1][1],v[-1][2]] for k, v in res.items()]

        #products_on_transporter = sorted(products_on_transporter, key=operator.itemgetter(1))
        #products_on_transporter = sorted(products_on_transporter, key=operator.itemgetter(2))

        return products_on_transporter


    def sort_products_not_on_transporter(self,transport_onto):
        """
        sort all products not on transporter

        :param transport_onto:
        :return: [[product_name,time (int)]]
        """

        location_transport_onto=transport_onto.has_for_transp_queue[0].has_for_queue_location[0]

        event_list = []

        for queue in self.transport.get_queue_transportation_allowed(transport_onto):
            if len(queue.has_for_queue_location)>0:
                queue_location=queue.has_for_queue_location[0]
                for position in queue.has_for_position:
                    for product in position.has_for_product:
                        if product.blocked_for_transporter == 0 and self.transport.end_queue_allowed(transport_onto,product):
                            event_onto_list = [event for event in position.is_position_event_of if
                                               self.transport.simCore.onto[
                                                   Label.ShortTermLogger.value + "0"] in event.is_event_short_term_logger_of]

                            for event in event_onto_list:
                                if event.type == Queue_Enum.Change.value:
                                    distance=self.transport.simCore.location.distance_dict[location_transport_onto.name][queue_location.name]
                                    event_list.append([product.name, event.time, distance,queue])

        event_list.sort(key=lambda x: x[1])

        res = defaultdict(list)

        for k, v, w, z in event_list: res[k].append([v, w, z])

        products_not_on_transporter = [[k, v[-1][0], v[-1][1], v[-1][2]] for k, v in res.items()]

        #products_not_on_transporter = sorted(products_not_on_transporter, key=operator.itemgetter(1))
        #products_not_on_transporter = sorted(products_not_on_transporter, key=operator.itemgetter(2))
        #print("NJF",products_not_on_transporter)
        return products_not_on_transporter

    def sort_products(self, products_on_transporter, products_not_on_transporter):
        """
        combines the sort on transporter and not on transporter with the sort product method

        :param products_on_transporter:
        :param products_not_on_transporter:
        """
        type_on = "on"
        type_not_on = "not_on"
        elements = products_on_transporter + products_not_on_transporter
        type_list = [type_on] * len(products_on_transporter) + [type_not_on] * len(products_not_on_transporter)

        for x, y in zip(elements, type_list):
            x.append(y)

        elements = sorted(elements, key=operator.itemgetter(1))
        elements = sorted(elements, key=operator.itemgetter(2))

        return elements


    def evaluateTransport(self, event_onto):
        """
        NJF has its on evaluate transporter start point, this is currently not really neccessary

        :param event_onto:
        """
        self.transport.simCore.event.remove_from_event_list(event_onto)
        time = self.transport.simCore.getCurrentTimestep()

        transport_onto = event_onto.has_for_transport_event.__getitem__(0)

        type_on = "on"
        type_not_on = "not_on"
        createEvaluation = False

        elements=self.combine_products(transport_onto)

        freePlace = 0
        queue_list = transport_onto.has_for_transp_queue

        for queue in queue_list:
            freePlace += self.transport.simCore.queue.get_number_of_free_positions(queue)
        # print("elements",elements)
        for element in elements:
            product_onto = self.transport.simCore.onto[element[0]]

            type = element[-1]
            queue_onto=element[-2]
            if type == type_on:
                if(queue_onto != None):
                    if queue_onto.name== self.transport.simCore.central.end_queue_list[0].name:
                        positions = self.transport.simCore.queue.get_free_positions(queue_onto)
                        position_onto = positions[0]
                        time = self.transport.createTransportation(transport_onto, queue_onto, time)
                        time = self.transport.simCore.queue.create_change(product_onto, position_onto, time,
                                                                          Queue_Enum.RemoveFromTransporter)

                        event_onto = self.transport.simCore.event.createEvent(time, Evaluate_Enum.ProductFinished, 0)
                        self.transport.simCore.event.add_product_to_event(event_onto, product_onto)
                        createEvaluation = True
                    else:

                        positions = self.transport.simCore.queue.get_free_positions(queue_onto)

                        if len(positions) > 0:
                            position_onto = positions[0]
                        else:
                            raise Exception(positions,"not declared (NJF controller)")

                        time = self.transport.createTransportation(transport_onto, queue_onto, time)
                        time = self.transport.simCore.queue.create_change(product_onto, position_onto, time,
                                                                          Queue_Enum.RemoveFromTransporter)

                        createEvaluation = True
                        break

            elif type == type_not_on and freePlace > 0:

                if not (self.transport.compare_location_product_transporter(product_onto, transport_onto)):
                    time = self.transport.createTransportation(
                        transport_onto,
                        product_onto.is_position_of[0].is_queue_of[0].has_for_queue_location[0]
                        , time)
                new_position_onto = self.transport.getFreePosition(transport_onto)
                time = self.transport.simCore.queue.create_change(product_onto, new_position_onto, time,Queue_Enum.AddToTransporter)

                createEvaluation = True
                break

        if not createEvaluation and len(elements) > 0:

            product_onto = None
            position_onto = None
            #print("elements",elements)
            for element in elements:

                type = element[-1]
                if type == type_on:
                    product_onto = self.transport.simCore.onto[element[0]]
                    break

            free_position_found = False
            for start_queue in self.transport.simCore.central.start_queue_list:
                positions = self.transport.simCore.queue.get_free_positions(start_queue)

                if len(positions) > 0:
                    time = self.transport.createTransportation(transport_onto, start_queue, time)
                    position_onto = positions[0]
                    free_position_found = True
                    break
            if not free_position_found:
                decide_deadlock_queue = []
                for deadlock_queue in self.transport.simCore.central.dead_lock_list:
                    positions = self.transport.simCore.queue.get_free_positions(deadlock_queue)
                    if len(positions) > 0:
                        distance = self.transport.simCore.location.calculateDistance(
                            transport_onto.has_for_transp_queue[0].has_for_queue_location[0],
                            deadlock_queue.has_for_queue_location[0])
                        decide_deadlock_queue.append([positions, distance, len(positions), deadlock_queue])

                # sort after distance
                decide_deadlock_queue = sorted(decide_deadlock_queue, key=operator.itemgetter(1, 2))

                if len(decide_deadlock_queue) > 0:
                    #print(decide_deadlock_queue[0])
                    time = self.transport.createTransportation(transport_onto, decide_deadlock_queue[0][3], time)
                    position_onto = decide_deadlock_queue[0][0][0]
                else:
                    raise Exception("Deadlock queue not found (NJF Controller)")

            if position_onto != None and product_onto != None:
                time = self.transport.simCore.queue.create_change(product_onto, position_onto, time,
                                                                  Queue_Enum.RemoveFromTransporterDeadlock)
            else:
                time = self.transport.createWait(transport_onto.transporter_waiting_time, time, transport_onto)
            createEvaluation = True

            # print("solve deadlock",product_onto,position_onto)
        elif not createEvaluation:

            number_of_events = [event for event in transport_onto.is_transport_event_of if
                                self.transport.simCore.onto[Label.EventList.value + "0"] in event.is_event_list_of]

            if len(number_of_events) == 0:
                time = self.transport.createWait(transport_onto.transporter_waiting_time, time, transport_onto)
            createEvaluation = True

        if createEvaluation:
            event_onto = self.transport.simCore.event.createEvent(time, Evaluate_Enum.Transporter, 0)
            self.transport.simCore.event.add_transport_to_event(event_onto, transport_onto)

    def combine_products(self,transport_onto):
        """
        arranges the products on the transporter, sorted by random

        :param products_on_transporter:
        :param products_not_on_transporter:
        :return: [[product_name,time,type]]
        """
        # parts on tranporter
        products_on_transporter = self.sort_products_on_transporter(transport_onto)

        # parts on not tranporter
        products_not_on_transporter = self.sort_products_not_on_transporter(transport_onto)

        # combine products on transporter and not on transporter
        elements = self.sort_products(products_on_transporter, products_not_on_transporter)

        return elements