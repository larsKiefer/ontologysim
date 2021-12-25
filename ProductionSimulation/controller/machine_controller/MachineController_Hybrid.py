import operator

from owlready2 import *
from itertools import islice

from ProductionSimulation.controller.machine_controller.MachineController import MachineController
from ProductionSimulation.sim.Enum import Label, Queue_Enum, Evaluate_Enum
from ProductionSimulation.sim.Machine import Machine
from ProductionSimulation.utilities.sub_class_utilities import SubClassUtility


class MachineController_Hybrid(MachineController):
    """
    the hybrid controller makes it possible to combine several machine controllers
    """

    def __init__(self):
        self.machine = None  # add it over machine.addMachineController
        self.controller_parameter_dict = {} #key: python class name, value: 0 < weight <1
        self.controller_instance_dict = {} #key: python class name, value: python instance

    def addControllerDict(self, controller_dict):
        """
        adding multiple controller

        :param controller_dict: {Python class:int [0:1]}
        """
        for python_class, v in controller_dict.items():

            if python_class in SubClassUtility.get_all_subclasses(
                    MachineController) or python_class == MachineController:
                if v > 1 or v < 0:
                    raise Exception(str(v) + " out of range")
                self.controller_parameter_dict[python_class.__name__] = v
                python_instance = python_class()
                python_instance.machine = self.machine
                self.controller_instance_dict[python_class.__name__] = python_instance
            else:
                raise Exception(str(python_class) + " not subclass of MachineController")

    def sort_products(self, machine_onto):
        """
        uses all defined controllers in the dictionaries and determines an optimal sequence

        :param machine_onto:
        :return:
        """
        erg_dict = {}
        product_dict = {}
        product_dict_value = {}
        erg_list = []
        for k, v in self.controller_instance_dict.items():
            if self.controller_parameter_dict[k] != 0:
                erg_dict[k] = v.sort_products(machine_onto)

                len_erg = len(erg_dict[k])

                if len_erg > 0:
                    value = 100 / len_erg
                    increment = value / len_erg
                    for erg in erg_dict[k]:
                        product_onto = erg[0]
                        if product_onto.name in product_dict.keys():
                            product_dict[product_onto.name] += value * self.controller_parameter_dict[k]
                        else:
                            product_dict[product_onto.name] = value * self.controller_parameter_dict[k]

                            product_dict_value[product_onto.name] = erg
                        value -= increment

        if len(product_dict) > 0:

            sorted_products = sorted(product_dict.items(), key=operator.itemgetter(1), reverse=True)

            for k, v in sorted_products:
                erg_list.append(product_dict_value[k])

        return erg_list
