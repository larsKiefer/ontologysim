from abc import abstractmethod

from ontologysim.ProductionSimulation.sim.Enum import Label, Evaluate_Enum


class RepairService:
    """
    main class of the repair service, abstract
    """

    def __init__(self,simCore):
        """

        :param simCore:
        """
        self.simCore=simCore

        self.service_onto=None
        self.serviceController=None

    @abstractmethod
    def initServiceMachine(self):
        pass

    def addRepairServiceController(self,serviceController):
        """
        adds a repair service controller to a repair service

        :param serviceController:
        :return:
        """
        self.serviceController=serviceController
        serviceController.repair_service=self

    @abstractmethod
    def getFreeServiceOperator(self,service_onto):
        """
        get free service operator

        :param service_onto:
        :return: [service]
        """
        pass

    @abstractmethod
    def createService(self,number_of_repair):
        """


        :param number_of_repair:
        :return:
        """
        pass

    @abstractmethod
    def createServiceOperator(self):
        """
        create service operator, abstract method
        :return:
        """
        pass

    @abstractmethod
    def addDefectToService(self,object_onto):
        """
        add defect onto to service onto, abstract method
        :param object_onto: onto
        :return:
        """
        pass

    @abstractmethod
    def repair(self,event_onto):
        """
        add repair
        :param event_onto: onto
        :return:
        """
        pass

    @abstractmethod
    def evaluateCreateEvent(self, service_onto, object_onto):
        """
        evaluate if a defect event is created
        :param service_onto:
        :param object_onto:
        :return:
        """
        pass

