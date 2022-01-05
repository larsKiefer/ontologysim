Example folder
===============

Structure
-----------

The example folder has the following sub folders:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - sub folder name
     - description
   * - analyse
     - all time analyse results were saved in this folder
   * - config
     - saves the pnml and ini files for creating a simulation
   * - controller
     - implementation of your own controller
   * - create_pnml
     - example of python files for creating a pnml-file
   * - log
     - location, where the logging results get saved
   * - owl
     -  location, where the owl files get saved


Main.py
-------------------

Starts the simulation. For further information view
:doc:`create a simulation <../tutorial/creating_a_simulation>`

MainPlot.py
-----------------------

**Introduction**

1. setting of the current dir

.. code-block:: python

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

    PathTest.current_main_dir=current_dir

2. plotting the log files

.. code-block:: python

    plot=Plot('/example/config/plot_log.ini')
    plot.plot()


**Complete code**

the complete code can be found under ``/example/MainPlot.py``

.. code-block:: python

    import inspect
    import os
    import sys

    from ontologysim.ProductionSimulation.plot.Log_plot import Plot
    from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)

    PathTest.current_main_dir=current_dir

    plot=Plot('/example/config/plot_log.ini')
    plot.plot()




