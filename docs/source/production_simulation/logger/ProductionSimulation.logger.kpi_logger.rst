
Logger
-----------------------------------------

.. automodule:: ontologysim.ProductionSimulation.logger.Logger
   :members:
   :undoc-members:
   :show-inheritance:

Sub logger
--------------------------------------------------------

.. automodule:: ontologysim.ProductionSimulation.logger.SubLogger
   :members:
   :undoc-members:
   :show-inheritance:

Machine logger
------------------------------------------------

.. list-table::
   :widths: 20 100
   :header-rows: 1

   * - Type
     - KPI
   * - Support
     - ["TTFp", "TTRp", "FE", "CMT", "AUITp", "AUBTp", "ADOTp", "AUSTp", "APTp", "AUPTp", "AUSTTp", "AUBLTp", "PBTp", "PRIp"]
   * - Basic
     - ["A", "AE", "TE", "UE", "SeR, E, OEE, NEE"]

.. automodule:: ontologysim.ProductionSimulation.logger.MachineLogger
   :members:
   :undoc-members:
   :show-inheritance:



Transporter logger
--------------------------------------------------
.. list-table::
   :widths: 20 100
   :header-rows: 1

   * - Type
     - KPI
   * - Support
     - ["TTFp", "TTRp", "FE", "CMTp","ADOTp", "AUITp", "AUSTp", "AUTTp"]
   * - Basic
     - []

.. automodule:: ontologysim.ProductionSimulation.logger.TransporterLogger
   :members:
   :undoc-members:
   :show-inheritance:

Product analyse logger
--------------------------------------------------------

.. list-table::
   :widths: 20 100
   :header-rows: 1

   * - Type
     - KPI
   * - Support
     - ["ProductType", "WIP", "ATTp", "AQMTp", "AUSTp", "APTp", "AUPTp", "AUSTnpp", "AOETp", "PPTp"]
   * - Basic
     - ["TR"]

.. automodule:: ontologysim.ProductionSimulation.logger.ProductAnalyseLogger
   :members:
   :undoc-members:
   :show-inheritance:

Queue fill level logger
--------------------------------------------------------

.. list-table::
   :widths: 20 100
   :header-rows: 1

   * - Type
     - KPI
   * - Support
     - ["FillLevel"]
   * - Basic
     - []

.. automodule:: ontologysim.ProductionSimulation.logger.QueueFillLevelLogger
   :members:
   :undoc-members:
   :show-inheritance:

Simulation logger
--------------------------------------------------------

.. list-table::
   :widths: 20 100
   :header-rows: 1

   * - Type
     - KPI
   * - Support
     - ["WIP","logging_time"]
   * - Basic
     - ["AR", "PR"]

.. automodule:: ontologysim.ProductionSimulation.logger.SimLogger
   :members:
   :undoc-members:
   :show-inheritance:

Transporter distribution logger
--------------------------------------------------------


.. automodule:: ontologysim.ProductionSimulation.logger.TransporterDistributionLogger
   :members:
   :undoc-members:
   :show-inheritance: