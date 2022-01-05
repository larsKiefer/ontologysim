import inspect
import os
import sys
import owlready2


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from ontologysim.ProductionSimulation.analyse.TimeAnalyse import TimeAnalyse
from ontologysim.ProductionSimulation.init.Initializer import Initializer

#path to example
def main():
    init=Initializer(current_dir)
    init.initSimCore()
    production_config_path="/example/config/production_config_lvl3.ini"
    owl_config_path="/example/config/owl_config.ini"
    controller_config_path="/example/config/controller_config.ini"
    logger_config_path="/example/config/logger_config_lvl3.ini"

    #choose between load from owl or create from config
    init.createProduction(production_config_path,owl_config_path)
    #init.loadProductionFromOWL("ontologysim/example/owl/production_without_task_defect.owl")


    #add Tasks
    init.addTaskPathGiven(production_config_path)

    #(optional)
    init.addDefectPathGiven(production_config_path)


    #add Logger
    init.addLoggerAndDataBasePathGiven(logger_config_path)

    #set controller
    init.loadControllerPathGiven(controller_config_path)

    #init.set_save_time(400)

    #run Simulation
    init.run()

    #TimeAnalyse.save_dict_to_csv()

    init.s.destroyOnto()

if __name__ == "__main__":
    main()