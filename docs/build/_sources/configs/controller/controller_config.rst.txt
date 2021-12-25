Controller ini
==============

in this ini the controller is defined. In the example folder the ``controller_config.ini`` is separated from the other ini's. But this is not a must. Important is only that the section starts with ``[Controller]``.

the following inputs have to be defined:

* **machine**
* **transporter**
* **orderrelease**
* **service_machine**: could be empty if no defect is defined
* **service_transporter**: could be empty if no defect is defined

Main structure
----------------

after each controller type e.g. machine, there needs to be a dict with the following keys:

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Key
     - Value
   * - type
     - Python class name of the control strategy
   * - add
     - default 'add': {}, if you want to combine multiple strategies, then 'add':{'conroller_class_name':number}

the number needs to be between 0 and 1

Example
---------

this file is available in ``example/config/controller_config.ini``

.. code-block:: JSON

    [Controller]
    machine = {'type': 'MachineController_FIFO', 'add': {}}
    transporter = {'type': 'TransporterController_Hybrid', 'add': {'TransporterController_FIFO': 0.328904853393797, 'TransporterController_NJF': 0.7350431153281545, 'TransporterController_EDD': 0.2947845362113132}}
    orderrelease = {'type':'OrderReleaseControllerEqual','add':{},'fillLevel':0.5}
    service_machine = {'type':'ServiceControllerMachine','add':{}}
    service_transporter = {'type':'ServiceControllerTransporter','add':{}}

