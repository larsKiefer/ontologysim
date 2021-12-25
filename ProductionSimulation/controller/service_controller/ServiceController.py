from ProductionSimulation.sim.Enum import Machine_Enum, Transporter_Enum


class ServiceController:
    """
    service controller which controls the repair process
    """

    def __init__(self):
        self.repair_service = None

    def evaluateService(self, event_onto):
        """
        main class for the evaluation of service for machine and transporter

        :param event_onto:
        """
        pass


class ServiceControllerTransporter(ServiceController):
    """
    service controller for transporter
    """

    def evaluateService(self, event_onto):
        """
        distributes the open repairs to the possible service places

        :param event_onto:
        """
        time = event_onto.time

        service_onto = event_onto.has_for_service_event[0]
        transport_onto = service_onto.has_for_wait_transporter_service[0]

        #self.repair_service.simCore.event.store_event(event_onto)
        self.repair_service.simCore.event.remove_from_event_list(event_onto)
        self.repair_service.simCore.event.store_event(event_onto)

        if service_onto.free_service_operator > 0:
            service_operator = self.repair_service.getFreeServiceOperator(service_onto)

            service_operator[0].has_for_transporter_service_operator_transporter.append(transport_onto)
            service_onto.has_for_wait_transporter_service.remove(transport_onto)
            service_onto.free_service_operator -= 1

            sub_defect = \
            [sub_defect for sub_defect in transport_onto.has_for_defect_transporter[0].has_for_sub_defect if
             sub_defect.defect_type == transport_onto.defect_type_transporter][0]
            repair_distribution = sub_defect.has_for_repair_distribution[0]

            time = time + self.repair_service.simCore.distribution.getTimefromOnto(repair_distribution)

            event_onto = self.repair_service.simCore.event.createEvent(time, Transporter_Enum.Defect,
                                                                       time - transport_onto.next_defect_transporter)
            self.repair_service.simCore.event.add_transport_to_event(event_onto, transport_onto)
            self.repair_service.simCore.event.add_service_to_event(event_onto,
                                                                   self.repair_service.simCore.repair_service_transporter.service_onto)

        # self.repair_service.transporter_service


class ServiceControllerMachine(ServiceController):
    """
    service controller for machine
    """

    def evaluateService(self, event_onto):
        """
        distributes the open repairs to the possible service places

        :param event_onto:
        """
        time = event_onto.time

        service_onto = event_onto.has_for_service_event[0]
        machine_onto = service_onto.has_for_wait_machine_service[0]

        #self.repair_service.simCore.event.store_event(event_onto)
        self.repair_service.simCore.event.remove_from_event_list(event_onto)

        if service_onto.free_service_operator > 0:
            service_operator = self.repair_service.getFreeServiceOperator(service_onto)

            service_operator[0].has_for_machine_service_operator_machine.append(machine_onto)
            service_onto.has_for_wait_machine_service.remove(machine_onto)
            service_onto.free_service_operator -= 1

            sub_defect = [sub_defect for sub_defect in machine_onto.has_for_defect_machine[0].has_for_sub_defect if
                          sub_defect.defect_type == machine_onto.defect_type_machine][0]
            repair_distribution = sub_defect.has_for_repair_distribution[0]

            time = time + self.repair_service.simCore.distribution.getTimefromOnto(repair_distribution)

            event_onto = self.repair_service.simCore.event.createEvent(time, Machine_Enum.Defect,
                                                                       time - machine_onto.next_defect_machine)
            self.repair_service.simCore.event.add_machine_to_event(event_onto, machine_onto)
            self.repair_service.simCore.event.add_service_to_event(event_onto,
                                                                   self.repair_service.simCore.repair_service_machine.service_onto)
