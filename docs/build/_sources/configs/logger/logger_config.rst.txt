Logger ini
==============

The logger ini is used to store the events, KPIs. In addition, this ini is used to set the attributes for the live plot
There are three different complexity levels available for creating a production. Lvl1 is the most complex production.
The level is saved in the section Type.

**type**: defines the lvl: *'lvl1'*, *'lvl2'* or *'lvl3'*

.. code-block::

    [Type]
    type = 'lvl2'

Lvl3 - Basic
--------------

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - log_events
     - bool: True or False, defines if all events should be saved
   * - time_interval
     - defines time interval for the calculation of the kpis over time
   * - log_summary
     - defines, which kpis should be logged for a summary report: bool (True or False)
   * - log_time
     - defines, which kpis should be logged over time intervals: bool (True or Flase)

the storage folder depends on the path defined for KPIs

**Example**

.. code-block:: JSON

    [KPIs]
    time_interval=100
    log_summary=True
    log_time=True
    log_events=False

ConfigIni
+++++++++++++

This section copies all data from the specified folder if desired and saves it to the logger folder ``_ini``. The main purpose is to store the conifg files (ini-file) at the KPIs.

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - addIni
     - bool: True or False
   * - path
     - relative path to the config path

the storage folder depends on the path defined for KPIs

**Example**

.. code-block:: JSON

    [ConfigIni]
    addIni=True
    path="/example/config/"

Plot
++++++++++++++

it is possible to display live KPIs in a graph

.. figure:: live_plot.PNG
   :align: center

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - plot
     - bool: True or False
   * - number_of_points_x
     - defines how many data points are shown at once, until the graph overflows
   * - data
     - list of dicts, which defines the kpi
        [ {'object_name': label or 'all','kpi': str,'type': str}]

the following types are defined: machine, transporter, queue, product, transporter_distribution, simulation

**Example**

.. code-block:: JSON

    [Plot]
    plot=False
    number_of_points_x=15
    #max 3 values
    data=[{'object_name':'all','kpi':'AE','type':'machine'},{'object_name':'all','kpi':'AUIT','type':'transporter'},{'object_name':'all','kpi':'AOET','type':'product'}]


Save
++++++++++


**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - csv
     - bool: True or False
   * - database
     - bool: True or False
   * - path
     - path for csv output
   * - sql_alchemy_database_uri
     - only needed if database True, path to database


the following types are defined: machine, transporter, queue, product, transporter_distribution, simulation


**Example**

.. code-block:: JSON


    [Save]
    csv = True
    database = True
    path="/ontologysim/example/log/"
    sql_alchemy_database_uri = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"


Lvl2 - Basic
--------------

KPIs
++++++++
The KPIs section defines how the individual events should be logged

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - log_events
     - bool: True or False, defines if all events should be saved
   * - time_interval
     - defines time interval for the calculation of the kpis over time
   * - log_summary
     - defines, which kpis should be logged for a summary report: for types view Logger_Enum
   * - log_time
     - defines, which kpis should be logged over time intervals: for types view Logger_Enum

the storage folder depends on the path defined for KPIs

**Example**

.. code-block:: JSON

    [KPIs]
    time_interval=100
    log_summary= ["transporter"]
    log_time=["machine"]
    log_events=False

ConfigIni
+++++++++++++

This section copies all data from the specified folder if desired and saves it to the logger folder ``_ini``. The main purpose is to store the conifg files (ini-file) at the KPIs.

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - addIni
     - bool: True or False
   * - path
     - relative path to the config path

the storage folder depends on the path defined for KPIs

**Example**

.. code-block:: JSON

    [ConfigIni]
    addIni=True
    path="/example/config/"

Plot
+++++++

it is possible to display live KPIs in a graph

.. figure:: live_plot.PNG
   :align: center

**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - plot
     - bool: True or False
   * - number_of_points_x
     - defines how many data points are shown at once, until the graph overflows
   * - data
     - list of dicts, which defines the kpi
        [ {'object_name': label or 'all','kpi': str,'type': str}]

the following types are defined: machine, transporter, queue, product, transporter_distribution, simulation

**Example**

.. code-block:: JSON

    [Plot]
    plot=False
    number_of_points_x=15
    #max 3 values
    data=[{'object_name':'all','kpi':'AE','type':'machine'},{'object_name':'all','kpi':'AUIT','type':'transporter'},{'object_name':'all','kpi':'AOET','type':'product'}]

Save
++++++++++


**Main Structure**

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - csv
     - bool: True or False
   * - database
     - bool: True or False
   * - path
     - path for csv output
   * - sql_alchemy_database_uri
     - only needed if database True, path to database


the following types are defined: machine, transporter, queue, product, transporter_distribution, simulation


**Example**

.. code-block:: JSON


    [Save]
    csv = True
    database = True
    path="/ontologysim/example/log/"
    sql_alchemy_database_uri = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"

Lvl1 - Advanced
----------------

currently not available


Complete file
--------------

LVL3: Example
+++++++++++++++++++++
this file is available in ``example/config/logger_config_3.ini``

.. code-block:: JSON

    [Type]
    type = 'lvl3'

    [KPIs]
    time_interval=100
    log_summary=True
    log_time=True
    log_events=False


    [ConfigIni]
    addIni=False
    path="/example/config/"

    [Plot]
    plot=False
    number_of_points_x=15
    #max 3 values
    data=[{'object_name':'all','kpi':'AE','type':'machine'},{'object_name':'all','kpi':'AUIT','type':'transporter'},{'object_name':'all','kpi':'AOET','type':'product'}]

    [Save]
    csv = True
    database = True
    path="/ontologysim/example/log/"
    sql_alchemy_database_uri = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"


LVL2: Example
+++++++++++++++++++++
this file is available in ``example/config/logger_config_2.ini``

.. code-block:: JSON

    [Type]
    type = 'lvl2'

    [KPIs]
    time_interval=100
    log_summary= ["transporter"]
    log_time=["machine"]
    log_events=False

    [ConfigIni]
    addIni=False
    path="/example/config/"

    [Plot]
    plot=False
    number_of_points_x=15
    #max 3 values
    data=[{'object_name':'all','kpi':'AE','type':'machine'},{'object_name':'all','kpi':'AUIT','type':'transporter'},{'object_name':'all','kpi':'AOET','type':'product'}]


    [Save]
    csv = True
    database = True
    path="/ontologysim/example/log/"
    sql_alchemy_database_uri = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"