import inspect
import os
import sys


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)



from ontologysim.Flask.FlaskApp import FlaskAppWrapper
#if not set as path variable
#owlready2.owlready2.JAVA_EXE = java path

#path to example

from ontologysim.ProductionSimulation.init.Initializer import Initializer;




def main():
    init = Initializer(current_dir)

    production_config_path = "/ontologysim/Flask/Assets/DefaultFiles/production_config_lvl3.ini"
    owl_config_path = "/ontologysim/Flask/Assets/DefaultFiles/owl_config.ini"
    controller_config_path = "/ontologysim/Flask/Assets/DefaultFiles/controller_config.ini"
    logger_config_path = "/ontologysim/Flask/Assets/DefaultFiles/logger_config_lvl3.ini"
    a = FlaskAppWrapper('wrap', init, {'production': production_config_path, 'owl': owl_config_path,
                                       'controller': controller_config_path, 'logger': logger_config_path})
    a.addSwaggerUI()
    a.run()

if( __name__ == "__main__"):
    main()

