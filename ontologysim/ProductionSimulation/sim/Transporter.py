from ontologysim.ProductionSimulation.sim.Enum import Label, Transporter_Enum, Evaluate_Enum


class Transporter:
    """

    """

    def __init__(self, simCore):
        """
        allowed queue [queue_list, machine_input_list, end_queue_allowed]
        :param simCore:
        """
        self.simCore = simCore
        self.transportController = None
        # self.transport_logger = TransporterLogger(self, self.simCore)
        self.allowed_queues = {}

    def addTransportController(self, transportController):
        """
        combines transport controller with transporter class

        :param transportController:
        """
        self.transportController = transportController
        transportController.transport = self

    def createTransporter(self, setting_dict, location_onto):
        """
        creates a transporter in onto

        :param setting_dict: dict{}
        :param location_onto: onto
        """
        # INFO: only the queue of the transporter has a location

        transport_Instance = self.simCore.central.transporter_class(
            Label.Transporter.value + str(self.simCore.transport_id))
        transport_Instance.speed = setting_dict['speed']
        setting_dict["location_onto"] = location_onto.name

        transport_Instance.transporter_waiting_time = setting_dict['waiting_time']

        queueInstance = self.simCore.queue.createQueue(setting_dict, Label.Queue.value ,
                                                       self.simCore.queue_id)

        queueInstance.is_a = [self.simCore.central.transport_queue_class]
        self.simCore.transport_id += 1

        transport_Instance.has_for_transp_queue.append(queueInstance)
        event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(),
                                                    Evaluate_Enum.Transporter, 0)
        self.simCore.event.add_transport_to_event(event_onto, transport_Instance)

        transport_Instance.is_defect_transporter = 0
        transport_Instance.next_defect_transporter = 0
        transport_Instance.start_current_location = 0
        transport_Instance.defect_type_transporter = ""
        transport_Instance.route_type = setting_dict['route']['type']


        self.allowed_queues[transport_Instance.name] = setting_dict['route']

        self.addLocation(transport_Instance, location_onto)

    def get_queue_transportation_allowed(self,transport_onto):
        """
        get the allowed queue, where the transporter can drive

        :param transport_onto: onto
        :return: [queue onto]
        """
        if self.allowed_queues[transport_onto.name]['type']=="free":
            return self.simCore.central.queue_list_not_transport_end_process
        else:
            return self.allowed_queues[transport_onto.name]['queue_list']

    def end_queue_allowed(self,transport_onto,product_onto):
        """
        checks if the transporter is allowed to go to the end_queue

        :param transport_onto: onto
        :param product_onto: onto
        :return: bool
        """

        if self.allowed_queues[transport_onto.name]['end_queue_allowed'] :
            return True
        else:
            process_id_list = self.simCore.product.getNextProcess(product_onto)
            if len(process_id_list)==0:
                return False
            return True

    def getAlowedMachine(self,transport_onto,suitable_list):
        """
        gets the allowed machine for the transporter

        :param transport_onto: onto
        :param suitable_list: [machine_onto,number_free positions,process onto]
        :return: [machine_onto,number_free positions,process onto]
        """
        if self.allowed_queues[transport_onto.name]['type'] == "free":
            return suitable_list
        else:
            intersected_suitable_list=[]
            for setting_list in suitable_list:
                for allowed_machine in self.allowed_queues[transport_onto.name]['machine_input_list']:

                    if setting_list[0].name == allowed_machine.name:
                        intersected_suitable_list.append(setting_list)
                        break
            return intersected_suitable_list

    def initTransporterDict(self):
        """
        the transporter dict pre calculates which queues are available for the transporter, to provide faster simulation

        """

        for k, v in self.allowed_queues.items():

            if v['type'] != 'free':
                queue_list = [ id for id in v['queue_list']]
                queue_onto_list = []
                end_queue_allowed=False
                for queue_id in v['queue_list']:
                    for queue in self.simCore.central.start_queue_list:
                        if queue.name == Label.StartQueue.value + str(queue_id):
                            queue_onto_list.append(queue)
                            queue_list.remove(queue_id)
                            break

                    for queue in self.simCore.central.dead_lock_list:
                        if queue.name == Label.DeadlockQueue.value + str(queue_id):
                            queue_onto_list.append(queue)
                            queue_list.remove(queue_id)
                            break

                    for queue in self.simCore.central.end_queue_list:
                        if queue.name == Label.EndQueue.value + str(queue_id):
                            queue_onto_list.append(queue)
                            queue_list.remove(queue_id)
                            end_queue_allowed = True
                            break

                    for queue in self.simCore.central.queue_list_not_transport_end_process:
                        if queue.name == Label.Queue.value + str(queue_id):
                            queue_onto_list.append(queue)
                            queue_list.remove(queue_id)
                            break
                if len(queue_list)>0:
                    raise Exception(str(queue_list)+" ids not defined")

                machine_list=[]
                for queue in queue_onto_list:
                    machine_list.extend(queue.is_input_queue_of)
                machine_list=list(set(machine_list))

                self.allowed_queues[k]['queue_list']=queue_onto_list
                self.allowed_queues[k]['machine_input_list'] = machine_list
                self.allowed_queues[k]['end_queue_allowed'] = end_queue_allowed
            else:
                self.allowed_queues[k]['end_queue_allowed'] = True



    def addLocation(self, transport_onto, location_onto):
        """
        adds a location the queue of the transporter, currently only the queue of the transporter has a location

        :param transport_onto: onto
        :param location_onto: onto
        """
        queue_onto = transport_onto.has_for_transp_queue[0]
        queue_onto.has_for_queue_location.append(location_onto)

    def wait(self, event_onto):
        """
        lets the transporter wait for x seconds

        :param event_onto: onto
        """

        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'time_diff': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'transporter_name': event_onto.has_for_transport_event[0].name
                                                    }])

        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.store_event(event_onto)

    def createWait(self, waiting_time, time, transport_onto):
        """
        creates a waiting event

        :param waiting_time: double
        :param time: dobule
        :param transport_onto: onto
        :return: double
        """
        event_onto = self.simCore.event.createEvent(waiting_time + time, Transporter_Enum.Wait, waiting_time)
        self.simCore.event.add_transport_to_event(event_onto, transport_onto)
        event_onto.waiting_time = waiting_time
        return waiting_time + time

    def transport(self, event_onto):
        """
        the transporter drives from location a to location b

        :param event_onto: onto
        """
        new_location_onto = event_onto.has_for_location_event.__getitem__(0)
        transport_onto = event_onto.has_for_transport_event.__getitem__(0)
        old_location = transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.__getitem__(0)
        transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.clear()
        transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.append(new_location_onto)
        current_location_time = event_onto.time-transport_onto.start_current_location - event_onto.time_diff
        transport_onto.start_current_location=event_onto.time


        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'time_diff': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'transporter_name': transport_onto.name,
                                                    'old_location': old_location.name,
                                                    'new_location_name': new_location_onto.name,
                                                    'current_location_time': current_location_time
                                                    }])

        # self.transport_logger.add_element(transport_onto.name, event_onto.time, old_location.name,
        #                                 new_location_onto.name)
        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.store_event(event_onto)

    def createTransportation(self, transport_onto, new_location_onto, time):
        """
        creates a transportation event

        :param transport_onto: onto
        :param new_location_onto: onto, have not to be a location onto, queue, endqueue,inputqueue,transport queue are also suitable
        :param time: double
        :return:
        """
        old_location = transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.__getitem__(0)
        if ".Location" in str(type(new_location_onto)):
            new_location_onto = new_location_onto
        elif ".Queue" in str(type(new_location_onto)):

            new_location_onto = new_location_onto.has_for_queue_location.__getitem__(0)
        elif ".EndQueue" in str(type(new_location_onto)):

            new_location_onto = new_location_onto.has_for_queue_location.__getitem__(0)
        elif ".InputQueue" in str(new_location_onto.is_a) or ".OutputQueue" in str(new_location_onto.is_a):

            new_location_onto = new_location_onto.has_for_queue_location.__getitem__(0)
        elif ".TranspQueue" in str(type(new_location_onto)):

            new_location_onto = new_location_onto.has_for_queue_location.__getitem__(0)
        else:
            raise Exception('change location object not defined ' + str(new_location_onto.is_a))

        distance = self.simCore.location.calculateDistance(old_location, new_location_onto)

        travel_time = distance / transport_onto.speed
        time += travel_time

        event_onto = self.simCore.event.createEvent(time, Transporter_Enum.Transport, travel_time)

        self.simCore.event.add_location_to_event(event_onto, new_location_onto)
        self.simCore.event.add_transport_to_event(event_onto, transport_onto)
        return time

    def compare_location_product_transporter(self, product_onto, transport_onto):
        """
        compare if the location of the product onto is equl to the transporter location

        :param product_onto: onto
        :param transport_onto: onto
        :return:
        """
        location_product = product_onto.is_position_of.__getitem__(0).is_queue_of.__getitem__(
            0).has_for_queue_location.__getitem__(0)
        location_transport = transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.__getitem__(0)

        return location_product.x == location_transport.x and location_product.y == location_transport.y and location_product.z == location_transport.z

    def getFreePosition(self, transport_onto):
        """
        calculates all free position of transporter

        :param transport_onto: onto
        :return: [position onto]
        """

        queue_list = transport_onto.has_for_transp_queue
        position_list = []
        position=None
        for queue in queue_list:
            for position in queue.has_for_position:
                if position.blockedSpace == 0:
                    position_list.append(position)

        if len(position_list) != 0:
            position = position_list.__getitem__(0)
        else:
            position=None
        return position

    def evaluateDefect(self, event_onto):
        """
        checks if the transporter is defect, when yes then defect service is created, otherwise
        the given event onto is exectued in another method

        :param event_onto: onto
        :return: bool
        """
        if self.simCore.defect.transport_defect_possible:
            transport_onto = event_onto.has_for_transport_event.__getitem__(0)
            time = event_onto.time
            if transport_onto.next_defect_transporter <= time:
                transport_onto.next_defect_transporter = time
                transport_onto.is_defect_transporter = 1
                self.simCore.repair_service_transporter.addDefectToService(transport_onto)
                self.simCore.event.store_event(event_onto)
                self.simCore.event.remove_from_event_list(event_onto)
                event_onto = self.simCore.event.createEvent(time, Evaluate_Enum.TransporterDefect, 0)
                self.simCore.event.add_service_to_event(event_onto,
                                                        self.simCore.repair_service_transporter.service_onto)

                return True
            else:
                return False
        return False

    def add_defect(self, transporter_onto, defect_onto):
        """
        adds a defect to the transporter onto, this defect onto describes the defect behavior

        :param transporter_onto: onto
        :param defect_onto: onto
        """
        transporter_onto.has_for_defect_transporter.append(defect_onto)

    def setNextDefectTime(self, transporter_onto, defect_onto):
        """
        calculates next defect and adds this value to the transporter defect

        :param transporter_onto:
        :param defect_onto:
        """
        next_defect_time, defect_type = self.simCore.defect.getNextDefectTime(defect_onto)
        next_defect_time += self.simCore.getCurrentTimestep()
        transporter_onto.next_defect_transporter = next_defect_time
        transporter_onto.defect_type_transporter = defect_type

    def getAllTransporter(self):
        """
        get all transporter onto, for better performance use central class

        :return: [transporter onto]
        """
        return self.simCore.onto.search(type=self.simCore.central.transporter_class)

    #TODO
    def transformToDict(self,id):
        """
        transform the transporter onto to dit and saves the kpis

        :param id:
        :return:
        """
        transport_list=[]
        response_dict={}
        if(id=="all"):
            transport_list=[transport_onto for transport_onto  in self.simCore.onto.search(type=self.simCore.central.transporter_class)]
        else:
            transport_list=[self.simCore.onto[id]]
        if transport_list == [None]:
            return {'error':"id_not_found"}
        for transport_onto in transport_list:

            response_dict[transport_onto.name]={}


            response_dict[transport_onto.name]['queue'] = transport_onto.has_for_transp_queue[0].name
            response_dict[transport_onto.name]['location'] = self.simCore.location.transformToDict(transport_onto.has_for_transp_queue[0].has_for_queue_location[0].name)
            response_dict[transport_onto.name]['route_type'] = transport_onto.route_type
            response_dict[transport_onto.name]['speed'] = transport_onto.speed


        return response_dict


