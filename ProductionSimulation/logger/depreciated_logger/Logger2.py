import csv
import math
import os
from abc import abstractmethod

from ProductionSimulation.sim.Enum import Label, Machine_Enum
from ProductionSimulation.utilities.path_utilities import PathTest


class Logger:
    """

    """
    def __init__(self,simCore):
        self.simCore=simCore
        self.kpi_dict = {}
        self.kpi_time_dict = {}  # time overall q1
        self.kpi_current_time_slot_dict = {}
        self.current_event = {}
        self.current_time = {}
        self.time_intervall = 100
        self.last_time_intervall = 0
        self.type=""
        self.path_csv=""

    @abstractmethod
    def init_dict(self):
        """

        """
        pass

    def setSettings(self,dict_setting):
        """

        :param dict_setting:
        """
        self.type=dict_setting['type']
        if "csv" in self.type:
            self.path_csv=dict_setting['path_csv']
            self.path_csv=PathTest.check_dir_path(self.path_csv)
        if 'time_intervall' in dict_setting.keys():
            self.time_intervall=dict_setting['time_intervall']

    @abstractmethod
    def add_element(self):
        """

        """
        pass

    @abstractmethod
    def evaluate(self):
        """

        """
        pass

    @abstractmethod
    def save_to_csv(self):
        """

        """
        pass

    @abstractmethod
    def insert_db(self):
        """

        """
        pass

    @abstractmethod
    def save(self):
        """

        """
        pass