import csv
import math
import os
import sys
import owlready2

from ProductionSimulation.sim.Enum import Label, Machine_Enum, Queue_Enum, Transporter_Enum, OrderRelease_Enum

from ProductionSimulation.utilities import init_utilities
from ProductionSimulation.utilities.path_utilities import PathTest


class EventLogger:
    """
    saves all events in logger onto
    """

    def __init__(self, simCore):

        self.simCore = simCore
        self.simCore.event_logger = self
        self.type = "csv"
        self.logger_onto = self.simCore.onto[Label.Logger.value + "1"]

        self.path_csv=""
        self.is_activated=True




    def save_to_csv(self, type):
        """
        saves logger-onto events to csv

        :param type: if overwrite or add
        """

        if(self.is_activated):
            with open(self.path_csv, type, newline='') as order_logger:
                wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)

                erg_list=self.getEventList()
                wr.writerows(erg_list)

    def getEventList(self):
        """
        return event list with all data for the event logger
        :return:
        """
        erg_list=[]
        for event in self.simCore.onto[Label.Logger.value + "1"].has_for_event_of_logger:
            erg_list.append(self.simCore.event_utilities.transformEventLoggerOntoToList(event))

        return erg_list



