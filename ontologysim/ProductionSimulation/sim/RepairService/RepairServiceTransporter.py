from ontologysim.ProductionSimulation.sim.Enum import Label, Evaluate_Enum, Transporter_Enum
from ontologysim.ProductionSimulation.sim.RepairService.RepairService import RepairService


class RepairServiceTransporter(RepairService):
    """
    repair service from machine, parent class is repair service
    """

    def __init__(self, simCore):
        """

       :param simCore:
       """
        super(RepairServiceTransporter,self).__init__(simCore)

    def initService(self):
        """
        saves the service onto as python instance
        :return:
        """
        self.service_onto = self.simCore.onto[Label.TransporterService.value + "0"]

    def createService(self,number_of_repair):
        """
        creates a service

        :param number_of_repair: repair places
        :return: onto
        """
        service_onto = self.simCore.central.transporter_service_class(
            Label.TransporterService.value + str(self.simCore.transporter_service_id))
        if number_of_repair > 0:
            service_onto.number_service_operator = number_of_repair
            service_onto.free_service_operator = 0
            self.simCore.transporter_service_id += 1
            service_onto.has_for_wait_transporter_service = []
            for i in range(number_of_repair):
                service_onto.has_for_transporter_service_operator.append(self.createServiceOperator())
            service_onto.number_service_operator = number_of_repair
            service_onto.free_service_operator = number_of_repair

    def createServiceOperator(self):
        """
        creates a service operator

        :return: service operator onto
        """
        service_operator = self.simCore.central.transporter_service_operator_class(
            Label.TransporterServiceOperator.value + str(self.simCore.transporter_service_operator_id))
        self.simCore.transporter_service_operator_id += 1
        service_operator.has_for_transporter_service_operator_transporter = []

        return service_operator

    def addDefectToService(self, object_onto):
        """
       adds a defect to a service in a waiting place

       :param object_onto:
       :return:
       """
        self.service_onto.has_for_wait_transporter_service.append(object_onto)

    def getFreeServiceOperator(self, service_onto):
        """
        returns all free service operator

        :param service_onto: onto
        :return: [service operaor]
        """
        return [service_operator for service_operator in service_onto.has_for_transporter_service_operator if
                len(service_operator.has_for_transporter_service_operator_transporter) == 0]

    def repair(self,event_onto):
        """
        repairs a transporter

        :param event_onto:
        :return:
        """
        time=event_onto.time
        transport_onto = event_onto.has_for_transport_event[0]
        service_onto = event_onto.has_for_service_event[0]

        self.simCore.logger.evaluatedInformations([{'type': event_onto.type,
                                                    'triggered_defect_time': transport_onto.next_defect_transporter,
                                                    'repair_time': event_onto.time_diff,
                                                    'event_onto_time': event_onto.time,
                                                    'transporter_name': transport_onto.name}])


        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        #self.simCore.event.store_event(event_onto)

        transport_onto.is_defect_transporter=0
        service_onto.free_service_operator+=1
        transport_onto.is_transporter_service_operator_transporter_of=[]

        self.simCore.transport.setNextDefectTime(transport_onto,transport_onto.has_for_defect_transporter[0])

        self.evaluateCreateEvent(service_onto,transport_onto)


    def evaluateCreateEvent(self,service_onto,transport_onto):
        """
        evaluates if the transporter gets repaired, is defect or if normal evaluation
        creates the events

        :param service_onto:
        :param transport_onto:
        :return:
        """

        event_list = self.simCore.onto[Label.EventList.value + "0"].has_for_event

        number_of_events_service_onto = 0
        number_of_events_transporter =0
        for event in event_list:
            if event.type == Evaluate_Enum.TransporterDefect.value:
                number_of_events_service_onto = 1
                break

        for event in event_list:

            if (event.type in [transport_enum.value for transport_enum in Transporter_Enum] or event.type == Evaluate_Enum.Transporter.value):
                if event in transport_onto.is_transport_event_of:
                    number_of_events_transporter=1

        if number_of_events_service_onto==0 and len(service_onto.has_for_wait_transporter_service)>0 and service_onto.free_service_operator>0:
            event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(), Evaluate_Enum.TransporterDefect, 0)
            self.simCore.event.add_service_to_event(event_onto, self.simCore.repair_service_transporter.service_onto)

        if number_of_events_transporter==0:
            event_onto = self.simCore.event.createEvent(self.simCore.getCurrentTimestep(), Evaluate_Enum.Transporter, 0)
            self.simCore.event.add_transport_to_event(event_onto,transport_onto)






