import owlready2

from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Queue_Enum, Transporter_Enum, OrderRelease_Enum


class EventUtilities:
    """
    transform on event onto to dict or provides additionally info to position
    """
    def __init__(self,simCore):
        self.position_dict = {}
        self.process_dict = {}
        self.simCore = simCore
        self.event_key_list=['name','time', 'time_diff', 'type_logger', 'additional_type', 'product',
                'position', 'position_info', 'machine', 'transport', 'process_id', 'location', 'task',
                'number_of_parts']

    def calc_position_dict(self):
        """
        gets additional information (queueing) to a position, these information are saved in the position dict
        """
        position_instances = self.simCore.onto.search(type=self.simCore.central.position_class)

        for position in position_instances:
            queue = position.is_queue_of.__getitem__(0)
            ref_string = ""
            if len(queue.is_input_queue_of) > 0:
                ref_string += queue.is_input_queue_of.__getitem__(0).name
                ref_string += " "
            if len(queue.is_output_queue_of) > 0:
                ref_string += queue.is_output_queue_of.__getitem__(0).name
            if len(queue.is_transp_queue_of) > 0:
                ref_string += queue.is_transp_queue_of.__getitem__(0).name

            if ref_string == "":
                ref_string = queue.name
            self.position_dict[position.name] = ref_string

    def calc_process_dict(self):
        """
         gets additional information (machine) to a process, these information are saved in the process dict
        """
        process_instances = self.simCore.onto.search(type=self.simCore.onto.search(iri="*#ProdProcess"))

        for process in process_instances:

            machine_name = process.is_prodprocess_of.__getitem__(0).name
            self.process_dict[process.name] = machine_name

    def transfromEventOntoToList(self,event_onto):
        """


        :param event_onto: onto: event_logger (not normal event)
        :return:
        """
        
        position_name = ""
        position_info_name = ""
        machine_name = ""
        transport_name = ""
        process_id = ""
        product_name = ""
        task_name = ""
        number_of_parts = ""
        location_name = ""
        additional_type = ""

        if Machine_Enum.Defect.value == event_onto.type:
            machine_name = event_onto.has_for_machine_event.__getitem__(0).name
        elif Machine_Enum.SetUp.value == event_onto.type:
            process_id = event_onto.has_for_process_event.__getitem__(0).process_id
            process_name = event_onto.has_for_process_event.__getitem__(0).name
            machine_name = self.process_dict[process_name]
        elif Machine_Enum.Wait.value == event_onto.type:
            machine_name = event_onto.has_for_machine_event.__getitem__(0).name
        elif Machine_Enum.Process.value == event_onto.type:
            process_id = event_onto.has_for_process_event.__getitem__(0).process_id
            process_name = event_onto.has_for_process_event.__getitem__(0).name
            machine_name = self.process_dict[process_name]
            # TODO change if combine
            product_name = event_onto.has_for_product_event.__getitem__(0).name

        elif Queue_Enum.Change.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            #print(self.simCore.product.getNextProcess(event_onto.has_for_product_event.__getitem__(0)))
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.AddToTransporter.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.RemoveFromTransporter.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.StartProcess.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.StartProcessStayBlocked.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.EndProcess.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.Default.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.RemoveFromTransporterDeadlock.value == event_onto.type:
            position_name = event_onto.has_for_position_event.__getitem__(0).name
            product_name = event_onto.has_for_product_event.__getitem__(0).name
            position_info_name = self.position_dict[position_name]

        elif Transporter_Enum.Defect.value == event_onto.type:
            transport_name = event_onto.has_for_transport_event.__getitem__(0).name
        elif Transporter_Enum.Wait.value == event_onto.type:
            transport_name = event_onto.has_for_transport_event.__getitem__(0).name
        elif Transporter_Enum.Transport.value == event_onto.type:
            transport_name = event_onto.has_for_transport_event.__getitem__(0).name
            location_name = event_onto.has_for_location_event.__getitem__(0).name

        elif OrderRelease_Enum.Release.value == event_onto.type:
            task_name = event_onto.has_for_task_event.__getitem__(0).name
            number_of_parts = event_onto.number_of_products

        if event_onto.additional_type == None:
            additional_type = ""
        else:
            additional_type = event_onto.additional_type

        return [event_onto.name,event_onto.time, event_onto.time_diff, event_onto.type, additional_type, product_name,
                position_name, position_info_name, machine_name, transport_name, process_id, location_name, task_name,
                number_of_parts]

    def transformEventOntoToFullDict(self,event_onto):
        """
        saves an event_onto to a dict, also the empty values are saved

        :param onto: event_logger (not normal event)
        :return: dict
        """
        event_dict = {}
        event_list = self.transfromEventOntoToList(event_onto)
        i = 0
        for event_feature in event_list:

            event_dict[self.event_key_list[i]] = event_feature

            i += 1

        return event_dict

    def transformEventOntoToDict(self, event_onto):
        """
        saves an event_onto to a dict, the empty values are not saved

        :param onto: event_logger (not normal event)
        :return: dict
        """
        event_dict ={}
        event_list = self.transfromEventOntoToList(event_onto)
        i=0
        for event_feature in event_list:
            if event_feature!="":
                event_dict[self.event_key_list[i]]=event_feature

            i+=1

        return event_dict

    def transformEventListToDict(self,event_list):
        """
        transform event_list to a dict, empty values are not saved

        :param event_list: [vent_name, time, ......]
        :return: dict
        """
        event_dict={}
        i = 0
        for event_feature in event_list:
            if event_feature != "":
                event_dict[self.event_key_list[i]] = event_feature

            i += 1

        return event_dict

    def transformEventListToFullDict(self,event_list):
        """
        transform event_list to a dict, empty values are saved

        :param event_list: [event_name, time, ......]
        :return: dict
        """
        event_dict={}
        i = 0
        for event_feature in event_list:

            event_dict[self.event_key_list[i]] = event_feature

            i += 1

        return event_dict

    def transformEventLoggerOntoToList(self, event_onto):
        """
        transform an event logger onto to a list

        :param event_onto: onto: event_logger (not normal event)
        :return: [event_name, time, ......]
        """
        position_name = ""
        position_info_name = ""
        machine_name = ""
        transport_name = ""
        process_id = ""
        product_name = ""
        task_name = ""
        number_of_parts = ""
        location_name = ""
        additional_type = ""

        if Machine_Enum.Defect.value == event_onto.type_logger:
            machine_name = event_onto.has_for_machine_event_of_logger.__getitem__(0).name
        elif Machine_Enum.SetUp.value == event_onto.type_logger:
            process_id = event_onto.has_for_process_event_of_logger.__getitem__(0).process_id
            process_name = event_onto.has_for_process_event_of_logger.__getitem__(0).name
            machine_name = self.process_dict[process_name]
        elif Machine_Enum.Wait.value == event_onto.type_logger:
            machine_name = event_onto.has_for_machine_event_of_logger.__getitem__(0).name
        elif Machine_Enum.Process.value == event_onto.type_logger:
            process_id = event_onto.has_for_process_event_of_logger.__getitem__(0).process_id
            process_name = event_onto.has_for_process_event_of_logger.__getitem__(0).name
            machine_name = self.process_dict[process_name]
            # TODO change if combine
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name

        elif Queue_Enum.Change.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.AddToTransporter.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.RemoveFromTransporter.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.StartProcess.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.StartProcessStayBlocked.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.EndProcess.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.Default.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]
        elif Queue_Enum.RemoveFromTransporterDeadlock.value == event_onto.type_logger:
            position_name = event_onto.has_for_position_event_of_logger.__getitem__(0).name
            product_name = event_onto.has_for_product_event_of_logger.__getitem__(0).name
            position_info_name = self.position_dict[position_name]

        elif Transporter_Enum.Defect.value == event_onto.type_logger:
            transport_name = event_onto.has_for_transport_event_of_logger.__getitem__(0).name
        elif Transporter_Enum.Wait.value == event_onto.type_logger:
            transport_name = event_onto.has_for_transport_event_of_logger.__getitem__(0).name
        elif Transporter_Enum.Transport.value == event_onto.type_logger:
            transport_name = event_onto.has_for_transport_event_of_logger.__getitem__(0).name
            location_name = event_onto.has_for_location_event_of_logger.__getitem__(0).name

        elif OrderRelease_Enum.Release.value == event_onto.type_logger:
            task_name = event_onto.has_for_task_event_of_logger.__getitem__(0).name
            number_of_parts = event_onto.number_of_products_logger

        if event_onto.additional_type_logger == None:
            additional_type = ""
        else:
            additional_type = event_onto.additional_type_logger

        return [event_onto.name, event_onto.time_logger, event_onto.time_diff_logger, event_onto.type_logger,
                additional_type, product_name,
                position_name, position_info_name, machine_name, transport_name, process_id, location_name, task_name,
                number_of_parts]