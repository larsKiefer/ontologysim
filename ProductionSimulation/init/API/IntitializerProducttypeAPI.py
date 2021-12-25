
import inspect
import os
import sys

from owlready2 import get_ontology

from ProductionSimulation.logger.EventLogger import EventLogger
from ProductionSimulation.sim.Defect import Defect
from ProductionSimulation.sim.Distribution import Distribution
from ProductionSimulation.sim.Event import Event
from ProductionSimulation.sim.Location import Location
from ProductionSimulation.sim.OrderRelease import OrderRelease
from ProductionSimulation.sim.Product import Product
from ProductionSimulation.sim.ProductType import ProductType
from ProductionSimulation.sim.Queue import Queue
from ProductionSimulation.sim.RepairService.RepairServiceMachine import RepairServiceMachine
from ProductionSimulation.sim.RepairService.RepairServiceTransporter import RepairServiceTransporter
from ProductionSimulation.sim.Task import Task
from ProductionSimulation.sim.Transporter import Transporter

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)



from ProductionSimulation.sim.Central import Central
from ProductionSimulation.sim.SimCore import SimCore
from ProductionSimulation.utilities.path_utilities import PathTest
from ProductionSimulation.init.TransformProductionIni import TransformProductionIni
from ProductionSimulation.init.TransformLoggerIni import TransformLoggerIni

from ProductionSimulation.logger.Logger import Logger
from ProductionSimulation.sim.Machine import Machine
from ProductionSimulation.sim.ProdProcess import ProdProcess
from ProductionSimulation.sim.ProductTypeNet.Process import Process, MergeProcess
from ProductionSimulation.sim.ProductTypeNet.State import State
from ProductionSimulation.utilities.event_utilities import EventUtilities


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



