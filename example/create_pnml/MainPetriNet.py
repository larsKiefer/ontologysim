"""depreciated


import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_parent_dir)


from ProductionSimulation.init.petrinet_generator import create_petrinet
from ProductionSimulation.utilities.path_utilities import PathTest
PathTest.current_main_dir = parent_dir

create_petrinet(10,[[1,2],[2,1]],"/example/create_pnml/",True)

"""