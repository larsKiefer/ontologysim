import math

from numpy.random import MT19937
from numpy.random import RandomState


from owlready2 import *

from ontologysim.ProductionSimulation.sim.Enum import Label
from ontologysim.ProductionSimulation.sim.Machine import Machine
import time
import numpy as np


class Distribution:
    """
    managing and creation of distribution onto
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore
        self.distribution_dict = {}

    def ini_dict(self):
        """
        every distribution onto has it's local RandomState, which is saved in the dict

        :return:
        """
        for distribution in self.simCore.onto.search(type=self.simCore.central.distribution_class):
            self.distribution_dict[distribution.name] = RandomState(MT19937(distribution.seed))

    def add_distribution_dict(self, distribution):
        """
        adding a distribution onto to the distribution dict

        :param distribution: onto
        :return:
        """
        self.distribution_dict[distribution.name] = RandomState(MT19937(distribution.seed))

    def getTimefromLabel(self, distribution_label):
        """
        calculates value from distribution function

        :param distribution_label: str
        :return: time (float)
        """
        distribution_onto = self.simCore.onto[distribution_label]
        mean = distribution_onto.mean
        deviate = distribution_onto.deviation

        return abs(round(self.distribution_dict[distribution_onto.name].normal(mean, deviate, 1)[0].item(), 4))

    def getTimefromOnto(self, distribution_onto):
        """
        calculates value from distribution function

        :param distribution_onto: onto
        :return: time (float)
        """
        mean = distribution_onto.mean
        deviate = distribution_onto.deviation
        float_value = abs(round(self.distribution_dict[distribution_onto.name].normal(mean, deviate, 1)[0].item(), 4))
        # print(float_value,distribution_onto)
        return float_value

    def getRandomTimefromOnto(self, random_distribution_onto):
        """
        calculates value from distribution function

        :param random_distribution_onto: onto
        :return: time (float)
        """
        min_value = random_distribution_onto.min_value
        max_value = random_distribution_onto.max_value
        if(min_value==max_value):
            return min_value
        int_value = int(self.distribution_dict[random_distribution_onto.name].randint(min_value, max_value, 1)[0])

        return int_value

    def getSumTimefromOnto(self, distribution_onto):
        """
        calculates value from distribution function and adds current simulation time

        :param distribution_onto: normal distribution onto
        :return: time (float)
        """
        mean = distribution_onto.mean
        deviate = distribution_onto.deviation

        return abs(round(self.distribution_dict[distribution_onto.name].normal(mean, deviate, 1)[0].item()),
                   4) + self.simCore.getCurrentTimestep()

    def createDistribution(self, distribution_dict, onto_name):
        """
        creates distribution for ontologysim, currently only normal and random distribution possible

        :param type: str
        :param mean: for normal; min value for random
        :param distribution: for normal; max value for random
        :return:
        """
        distributionInstance = None
        if distribution_dict['type'] == "normal":

            distributionInstance = self.simCore.central.normal_distribution_class(
                Label.NormalDistribution.value + str(self.simCore.distribution_id))

            distributionInstance.mean = distribution_dict['mean']
            distributionInstance.deviation = distribution_dict['deviation']
        elif distribution_dict['type'] == "random":

            min = distribution_dict['min']
            max = distribution_dict['max']

            distributionInstance = self.simCore.central.random_distribution_class(
                Label.RandomDistribution.value + str(self.simCore.distribution_id))

            distributionInstance.max_value = max
            distributionInstance.min_value = min


        if distributionInstance == None:
            raise Exception("normal error")
        distributionInstance.distribution_type = distribution_dict['type']
        distributionInstance.seed = self.transform_name_to_int(onto_name)
        self.add_distribution_dict(distributionInstance)
        self.simCore.distribution_id += 1

        return distributionInstance

    def transform_name_to_int(self, name):
        """
        transforms a string to a number, each onto instance has it's own defined distribution and random state

        :param name: str
        :return: int
        """
        return sum([ord(char) for char in name]) + self.simCore.random_seed_add_value

    def transformToDict(self,id):
        """
        transforms a onto-instance to dict

        :param id: onto name
        :return: dict{}
        """

        response_dict={}
        distribution_onto=self.simCore.onto[id]
        response_dict['label']=distribution_onto.name
        response_dict['type']=distribution_onto.distribution_type
        if distribution_onto.distribution_type=="normal":
            response_dict['mean']=distribution_onto.mean
            response_dict['deviation']=distribution_onto.deviation
        elif distribution_onto.distribution_type=="random":
            response_dict['max_value']=distribution_onto.max_value
            response_dict['min_value']=distribution_onto.min_value
        elif distribution_onto.distribution_type == "steady":
            response_dict['value'] = distribution_onto.value
        else:
            raise Exception("not defined")
        return response_dict