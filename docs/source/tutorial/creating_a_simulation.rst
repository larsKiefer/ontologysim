Create a simulation
===================

For starting a simulation, the following files must be created:

* **Main.py**: starts simulation
* **production_config.ini**: initializes the production
* **controller_config.ini**: defines the controll strategie, e.g. routing, scheduling
* **logger_config.ini**: defines how the KPIs and events should be saved
* **owl_config.ini**: ontologysim path and save options
* **pnml-files**: defines the product types


First simulation run
-----------------------

For a quick start the required files are already build and could be found in the  ``/example`` folder.

**Go to the** ``/example/Main.py`` **and run this python file.**

This simulation exist of:

* 1 machine
* 1 transporter
* 1 product type



Adapting the simulation run
--------------------------------

Main.py
+++++++++++++

Explanation of the Main.py file

1. Initialize the initialization and set the current dir correctly

.. code-block:: python

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

.. code-block:: python

    init=Initilizer(current_dir)
    init.initSimCore()

2. define all needed config ini files

.. code-block:: python

    production_config_path="/example/config/production_config.ini"
    owl_config_path="/example/config/owl_config.ini"
    controller_config_path="/example/config/controller_config.ini"
    logger_config_path="/example/config/logger_config_simple.ini"

3. create production

    * either load from owl file or create vom production_config.ini

.. code-block:: python

    #choose between load from owl or create from config
    init.createProduction(production_config_path,owl_config_path)
    #init.loadProductionFromOWL("ontologysim/example/owl/production_without_task_defect.owl")

4. add task

.. code-block:: python

    init.addTask(production_config_path)

5. add defect (optional)

.. code-block:: python

    init.addDefect(production_config_path)

6. add logger

.. code-block:: python

    init.addLogger(logger_config_path)

7. load controller

.. code-block:: python

    init.loadController(controller_config_path)

8. set a additional save time for the ontology (option)

.. code-block:: python

    init.set_save_time(400)

9. run simulation

.. code-block:: python

    init.run()

Complete file
~~~~~~~~~~~~~~~~

The file can be found in ``/èxample/Main.py``

.. code-block:: python

    import inspect
    import os
    import sys
    import owlready2

    from ontologysim.ProductionSimulation.analyse.TimeAnalyse import TimeAnalyse

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)


    from ontologysim.ProductionSimulation.init.Initializer import Initializer
    from example.controller import MachineController_FIFO2

    #path to config
    init=Initializer(current_dir)
    init.initSimCore()
    production_config_path="/example/config/production_config2.ini"
    owl_config_path="/example/config/owl_config.ini"
    controller_config_path="/example/config/controller_config.ini"
    logger_config_path="/example/config/logger_config_simple.ini"


    #choose between load from owl or create from config
    init.createProduction(production_config_path,owl_config_path)
    #init.loadProductionFromOWL("ontologysim/example/owl/production_without_task_defect.owl")

    #add Tasks
    init.addTask(production_config_path)

    #(optional)
    init.addDefect(production_config_path)


    #add Logger
    init.addLogger(logger_config_path)

    #set controller
    init.loadController(controller_config_path)

    #init.set_save_time(400)

    #run Simulation
    init.run()



Production config
+++++++++++++++++++++

Defines the production, e.g. number of machines, transporter ..
For further infos view:
:doc:`production config <../configs/production/production_config>`


Controller config
+++++++++++++++++++++

Responsible for defining the used control strategies:
For further infos view:
:doc:`controller config <../configs/controller/controller_config>`

Logger config
+++++++++++++++++++++

Responsible for logging the kpis, events and allows to set a live plot
For further infos view:
:doc:`log config <../configs/logger/logger_config>`

PNML
+++++++++++++++++++++

Defines the product type, each product type has it's own pnml-file
For further infos view:
:doc:`pnml <../configs/pnml>`

OWL
+++++++++++++++++++++

Defines the java path and gives save options
For further infos view:
:doc:`owl config <../configs/owl/owl_config>`

