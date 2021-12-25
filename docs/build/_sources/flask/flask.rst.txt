Flask package
=============

Main documentation
--------------------------------------
The main documentation regarding the api calls is documented with swagger-UI. To access swagger-UI start Flask and open `http://localhost:5000/api/docs <http://localhost:5000/api/docs>`_

The following modules are used to document the python code


Main modules
----------------------

.. toctree::
   :maxdepth: 0

   main/Flask


Actions module
---------------------

============================   ================================
  path                              Action
============================   ================================
/nextEvent                      :ref:`EventAction`
/getIds                         :ref:`GetIdsAction`
/component                      :ref:`ComponentAction`
/component/id                   :ref:`ComponentIdAction`
/start                          :ref:`StartAction`
/startUntilTime                 :ref:`StartUntilTimeAction`
/process                        :ref:`ProcessAction`
/production                     :ref:`ProductionAction`
/load_files                     :ref:`FileLoadAction`
/simulation/download/owl        :ref:`OwlDownloadAction`
/runSimulation                  :ref:`RunSimulationAction`
/test                           :ref:`TestAction`
/kpi                            :ref:`KPIAction`
/kpiList                        :ref:`KPIListAction`
/reset_be                       :ref:`ResetBEAction`
/database/connect               :ref:`ConnectDataBaseAction`
/database/simulationrun         :ref:`GetSimulationRunAction`
============================   ================================

CheckProduction
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions.CheckProduction


CheckProductType
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions.CheckProductType

Simulation
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions.Simulation

DataBase
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions.DataBase

Other
^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions


Util module
--------------

.. toctree::
   :maxdepth: 0

   actions/Flask.Actions.UtilMethods

Assets module
-------------------

DefaultFiles
^^^^^^^^^^^^^^^^^^^^
Here is a default configuration that can be displayed in the frontend and is used to facilitate the operation of the backend. Important only one simulation may be stored there.

DefaultSaveFolder
^^^^^^^^^^^^^^^^^^^^
For some api calls the owl must be saved, this happens in this folder. This is e.g. the case when outputting the ontlogysim as string

static module
-----------------
Here is the swaggerUI Documentation located