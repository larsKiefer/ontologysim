import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ProductionSimulation.plot.Log_plot import Plot
from ProductionSimulation.utilities.path_utilities import PathTest

def mainPlot():
    PathTest.current_main_dir = current_dir
    plot = Plot('/example/config/plot_log.ini')
    plot.plot()





if __name__ == "__main__":
    mainPlot()