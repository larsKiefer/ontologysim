from owlready2 import *

from ProductionSimulation.analyse.TimeAnalyse import TimeAnalyse
from ProductionSimulation.logger.depreciated_logger.ProductFinishedLogger import ProductFinishedLogger
from ProductionSimulation.sim.Enum import Label
import datetime

class SubProduct:
    """
    handles the product onto
    """
    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

    def createSubProduct(self,part_type_onto):
        """
        creates product in onto

        :param part_type_onto: onto
        :return: product onto
        """

        subProductInstance = self.simCore.central.sub_product_class(Label.SubProduct.value+ str(self.simCore.sub_product_id))
        self.simCore.sub_product_id += 1

        return subProductInstance

    
