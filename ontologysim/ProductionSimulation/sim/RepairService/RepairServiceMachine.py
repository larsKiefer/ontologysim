from ontologysim.ProductionSimulation.sim.Enum import Label, Evaluate_Enum, Machine_Enum
from ontologysim.ProductionSimulation.sim.RepairService.RepairService import RepairService


class RepairServiceMachine(RepairService):
    """
    repair service from machine, parent class is repair service
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        super().__init__(simCore)

    def initService(self):
        """
        saves the service onto as python instance
        :return:
        """
        self.service_onto = self.simCore.onto[Label.MachineService.value + "0"]

    def createService(self, number_of_repair):
        """
        creates a service

        :param number_of_repair: repair places
        :return: onto
        """
        service_onto = None
        if number_of_repair > 0:

            service_onto = self.simCore.central.machine_service_class(
                Label.MachineService.value + str(self.simCore.machine_service_id))

            self.simCore.machine_service_id += 1
            service_onto.has_for_wait_machine_service = []
            for i in range(number_of_repair):
                service_onto.has_for_machine_service_operator.append(self.createServiceOperator())
            service_onto.number_service_operator = number_of_repair
            service_onto.free_service_operator = number_of_repair

        return service_onto

    def createServiceOperator(self):
        """
        creates a service operator

        :return: service operator onto
        """
        service_operator = self.simCore.central.machine_service_operator_class(
            Label.MachineServiceOperator.value + str(self.simCore.machine_service_operator_id))
        self.simCore.machine_service_operator_id += 1
        service_operator.has_for_machine_service_operator_machine = []

        return service_operator

    def addDefectToService(self, object_onto):
        """
        adds a defect to a service in a waiting place

        :param object_onto:
        :return:
        """

        self.service_onto.has_for_wait_machine_service.append(object_onto)

    def getFreeServiceOperator(self, service_onto):
        """
        returns all free service operator

        :param service_onto: onto
        :return: [service operaor]
        """
        return [service_operator for service_operator in service_onto.has_for_machine_service_operator if
                len(service_operator.has_for_machine_service_operator_machine) == 0]

    def repair(self, event_onto):
        """
        repairs a machine

        :param event_onto:
        :return:
        """

        time = event_onto.time
        machine_onto = event_onto.has_for_machine_event[0]
        service_onto = event_onto.has_for_service_event[0]


        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'triggered_defect_time': machine_onto.next_defect_machine,
                                                    'repair_time': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'machine_name': machine_onto.name}])
        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        #self.simCore.event.store_event(event_onto)

        machine_onto.is_defect_machine = 0
        service_onto.free_service_operator += 1
        machine_onto.is_machine_service_operator_machine_of = []

        self.simCore.machine.setNextDefectTime(machine_onto, machine_onto.has_for_defect_machine[0])

        self.evaluateCreateEvent(service_onto, machine_onto)

    def evaluateCreateEvent(self, service_onto, machine_onto):
        """
        evaluates if the machine gets repaired, is defect or if normal evaluation
        creates the events

        :param service_onto:
        :param machine_onto:
        :return:
        """

        event_list = self.simCore.onto[Label.EventList.value + "0"].has_for_event

        number_of_events_service_onto = 0
        number_of_events_machine = 0
        for event in event_list:
            if event.type == Evaluate_Enum.MachineDefect.value:
                number_of_events_service_onto = 1
                break

        for event in event_list:

            if (event.type in [machine_enum.value for machine_enum in
                               Machine_Enum] or event.type == Evaluate_Enum.Machine.value):
                if event in machine_onto.is_machine_event_of:
                    number_of_events_machine = 1

        if number_of_events_service_onto == 0 and len(
                service_onto.has_for_wait_machine_service) > 0 and service_onto.free_service_operator > 0:
            event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(), Evaluate_Enum.MachineDefect,
                                                        0)
            self.simCore.event.add_service_to_event(event_onto, self.simCore.repair_service_machine.service_onto)

        if number_of_events_machine == 0:
            event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(), Evaluate_Enum.Machine, 0)
            self.simCore.event.add_machine_to_event(event_onto, machine_onto)
