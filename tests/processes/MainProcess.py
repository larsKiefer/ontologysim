

# path to example
import ast
import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, parent_parent_dir)

from ontologysim.ProductionSimulation.init.Initializer import Initializer


def main():
    """
    proiding method for running the min.py method with args argument, needed for terminal call in the test environment
    :return:
    """
    args = sys.argv[1:]
    print(args)
    listConfig = ast.literal_eval(args[0])
    production_config_path = listConfig["production"]
    owl_config_path = listConfig["config"]
    controller_config_path = listConfig["controller"]
    logger_config_path = listConfig["logger"]

    init = Initializer(current_dir)
    init.initSimCore()

    # choose between load from owl or create from config
    init.createProduction(production_config_path, owl_config_path)
    # init.loadProductionFromOWL("ontologysim/example/owl/production_without_task_defect.owl")

    # add Tasks
    init.addTaskPathGiven(production_config_path)

    # (optional)
    init.addDefectPathGiven(production_config_path)

    # add Logger
    init.addLoggerAndDataBasePathGiven(logger_config_path)

    # set controller
    init.loadControllerPathGiven(controller_config_path)

    # init.set_save_time(400)
    # run Simulation
    init.run()

if __name__ == "__main__":
    main()