
from numpy.random.mt19937 import MT19937
from numpy.random.mtrand import RandomState


class Generator(object):
    """
    parent class for all generator
    """

    def __init__(self,seedParameter=None):
        """

        :param seedParameter: int
        """

        self.randomDistribution =  RandomState(MT19937(seedParameter))

    def createConfigDict(self):
        """
        abstract method for main entry point of config generation
        :return:
        """
        pass

    def addType(self,lvl):
        """
        creates lvl dict
        :param lvl: string
        :return: dict
        """

        config= {}
        config["type"] = lvl
        return config