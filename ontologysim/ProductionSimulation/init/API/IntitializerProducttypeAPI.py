
import inspect
import os
import sys

from ontologysim.ProductionSimulation.sim.ProductType import ProductType

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)



from ontologysim.ProductionSimulation.sim.Central import Central
from ontologysim.ProductionSimulation.sim.SimCore import SimCore

from ontologysim.ProductionSimulation.sim.ProductTypeNet.Process import Process


class InitializerProducttypeAPI:
    """
    initialize all needed objects to create procudttype
    """

    def __init__(self):
        """

        """
        self.s = SimCore()


        self.s.central = Central(self.s)
        self.s.product_type = ProductType(self.s)
        self.s.process = Process(self.s)

        self.s.createOWLStructure()
        self.s.central.init_class()



