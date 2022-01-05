Production ini
==============

There are three different complexity levels available for creating a production. Lvl1 is the most complex production.
The level is saved in the section Type.

**type**: defines the lvl: *'lvl1'*, *'lvl2'* or *'lvl3'*

.. code-block::

    [Type]
    type = 'lvl2'


Lvl3 - Basic
--------------

A complete example can be viewed under: ``/example/config/for_docu/production_config_lvl3.ini``.
The most values are set via ontologysim site packages ``ontologysim/ProductionSimulation/init/defaultValue.init``

Machine
++++++++

**Parameters**

* **number_of_machines**: defines the number of machines
* **settings**: list with dict{'number_of_positions', 'process','location'}
    * **location**: [x, y, z] list with 3 numbers
    * **number_of_positions**: 1..n
    * **process**: list with process_id

**Code Example**

.. code-block::

    [Machine]
    number_of_machines=2
    #only standard and number_of_queue=1 is working
    settings=[{'number_of_positions':3,'process':[0,1],'location':[10,10,0]},
            {'number_of_positions':3,'process':[0,1],'location':[0,5,0]}
            ]

ProductType
+++++++++++++

**Parameters**

* **settings**: list with dict{'id', 'path'}
    * **id**: number
    * **cofnig**: nested list

.. code-block::

    [ProductType]
    settings=[{'id':0,'config':[[0,1,2],[2,2,1,0]]},
         {'id':1,'config':[[0,2,1]]},
         {'id':2,'config':[[0,1]]}
                ]

Task
+++++

**Parameters**

* **settings**: list with dict{'product_type', 'number_of_parts', 'type'}
    * **product_type**:
    * **number_of_parts**:
    * **type**: defines the type of task
        * start: these products are not logged, there only task is to reduce the starting effect
        * logging: after the first logging product is inserted the logging starts
        * end: these products are not logged, there only task is to reduce the ending effect, when every logging product is produced the production ends

**Code Example**

.. code-block::

    [Task]
    settings=[{'product_type':0,'number_of_parts':10,"type":'start'},
          {'product_type':0,'number_of_parts':150,"type":'logging'},
          {'product_type':1,'number_of_parts':150,"type":'logging'},
          {'product_type':2,'number_of_parts':150,"type":'logging'},
          {'product_type':0,'number_of_parts':10,"type":'end'}
          ]

Process
+++++++++

**Parameters**

* **settings**: list of dict{'id', 'mean', 'deviation', 'type'}
    * **id**: this number must be identical to the id in the pnml-file and in the machine section
    * **mean**: number
    * **deviation**: number
    * **type**: only 'normal' available


**Code Example**

.. code-block::

    [Process]
    settings=[{'id':0,'mean':5,'deviation':0,'type':'normal'},
        {'id':1,'mean':10,'deviation':2,'type':'normal'},
        {'id':2,'mean':15,'deviation':1,'type':'normal'}]

Transporter
++++++++++++++

**Parameters**

* **number_of_transporter**: defines the number of transporters
* **settings**: list with dict{'number_of_positions', 'location_id', 'speed', 'add_time', 'remove_time'}
    * **number_of_positions**: 1..n
    * **speed**: number

**Code Example**

.. code-block::

    [Transporter]
    number_of_transporter=3
    settings=[{'number_of_positions':3,'speed':3},{'number_of_positions':3,'speed':3},{'number_of_positions':3,'speed':3}]


ChangeTime
++++++++++++++

**Parameters**

    * **set_up_time**: set up time for machine
    * **add_time**:  add time for queue
    * **remove_time**: remove time for queue
    * **deviation**: deviation of all times

**Code Example**

.. code-block::

    [ChangeTime]
    set_up_time=0
    add_time=0
    remove_time=0
    deviation=0



Defect
++++++++

only needed if a defect is added to the simulation

**Parameters**

* **transporter_defect_possible**: bool, True or False

* **transporter_normal**: dict{ 'defect', 'repair'}
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect
* **machine_defect_possible**: bool, True or False
* **machine_normal**: list of dict{'defect_type', 'defect', 'repair'}
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect

**Code Example**

.. code-block::

    [Defect]
    transporter_defect_possible=True
    transporter_normal={'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}}

    machine_defect_possible=True
    machine_normal={'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}}

Repair
++++++++

only needed when defect is added

**Parameters**

* **machine_repair** = 1..n
* **transporter_repair** = 1..n


**Code Example**

.. code-block::

    [Repair]
    machine_repair=2
    transporter_repair=1

RandomSeed
+++++++++++++

each simulation run through provides the same results, to change it you need to vary the AppendValue

**Parameters**
* **AppendValue**: number

**Code Example**

.. code-block::

    [RandomSeed]
    AppendValue=0



Lvl2 - Intermediate
---------------------

A complete example can be viewed under: ``/example/config/for_docu/production_config.ini`` or ``/example/config/for_docu/production_config_lvl2.ini``

Machine
++++++++

**Parameters**

* **number_of_machines**: defines the number of machines
* **settings**: list with dict{'queue_type', 'number_of_queue', 'number_of_positions', 'process', 'set_up', 'location', 'add_time', 'remove_time'}
    * **queue_type**: 'standard'
    * **number_of_queues**: 1
    * **number_of_positions**: 1..n
    * **process**: list with process_id
    * **waiting_time**: idle waiting time (optional), otherwise default value
    * **set_up**: list with dict{'start', 'end', 'mean', 'deviation', 'type'}
        * each combination of the process list needs to be initialized (both direction independently)
        * **start**: process_id, from which process_id should the set_up start
        * **end**: process_id, to which process_id should the set_up be performed
        * **mean**: number
        * **deviation**: number
        * **type**: 'normal', the set up can only have a normal distribution
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [Machine]
    number_of_machines=2
    #only standard and number_of_queue=1 is working
    settings=[{'queue_type':"standard",'number_of_queue':1, "waiting_time":5,'number_of_positions':3,'process':[0,1],'set_up':[{'start':0 ,'end':1 ,'mean':1 ,'deviation':0 ,'type':'normal'},{'start':1 ,'end':0 ,'mean':1 ,'deviation':0 ,'type':'normal'}],'location':[10,10,0],
             'add_time':{'mean':2,'deviation':0.4,'type':'normal'},'remove_time':{'mean':1,'deviation':0.2,'type':'normal'}},
            {'queue_type':"standard",'number_of_queue':1,"waiting_time":5,'number_of_positions':3,'process':[0,1],'set_up':[{'start':0 ,'end':1 ,'mean':1 ,'deviation':0 ,'type':'normal'},{'start':1 ,'end':0 ,'mean':1 ,'deviation':0 ,'type':'normal'}],'location':[0,5,0],
             'add_time':{'mean':2,'deviation':0.4,'type':'normal'},'remove_time':{'mean':1,'deviation':0.2,'type':'normal'}}
            ]

Start_Queue
++++++++++++

**Parameters**

* **number_of_queue**: defines the number of start queues
* **settings**: list with dict{'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **number_of_positions**: 1..n
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [Start_Queue]
    number_of_queue=1
    settings=[{'location':[0,0,0], 'number_of_positions':3,'add_time': {'mean':1,'deviation':0.2,'type':'normal'},'remove_time': {'mean':1,'deviation':0.2,'type':'normal'}}]

End_Queue
++++++++++++

**Parameters**

* **number_of_queue**: defines the number of end queues
* **settings**: list with dict{'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **number_of_positions**: only 1 possible
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [End_Queue]
    number_of_queue=1
    settings=[{'location':[0,0,0], 'number_of_positions':3,'add_time': {'mean':1,'deviation':0.2,'type':'normal'},'remove_time': {'mean':1,'deviation':0.2,'type':'normal'}}]

Deadlock_Queue
++++++++++++++++

**Parameters**

* **number_of_queue**: defines the number of deadlock queues
* **settings**: list with dict{'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **number_of_positions**: 1..n
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
* **deadlock_waiting_time**: Time in which the part cannot be transported in the deadlock queue

**Code Example**

.. code-block::

    [Deadlock_Queue]
    number_of_queue=1
    settings=[{'location':[3,3,0],'number_of_positions':5,'add_time': {'mean':1,'deviation':0.2,'type':'normal'},'remove_time': {'mean':1,'deviation':0.2,'type':'normal'}}]
    deadlock_waiting_time = 5

ProductType
+++++++++++++

**Parameters**

* **settings**: list with dict{'id', 'path'}
    * **id**: number
    * **cofnig**: nested list

.. code-block::

    [ProductType]
    settings=[{'id':0,'config':[[0,1,2],[2,2,1,0]]},
         {'id':1,'config':[[0,2,1]]},
         {'id':2,'config':[[0,1]]}
                ]

Task
+++++

**Parameters**

* **settings**: list with dict{'product_type', 'number_of_parts', 'type'}
    * **product_type**:
    * **number_of_parts**:
    * **type**: defines the type of task
        * start: these products are not logged, there only task is to reduce the starting effect
        * logging: after the first logging product is inserted the logging starts
        * end: these products are not logged, there only task is to reduce the ending effect, when every logging product is produced the production ends

**Code Example**

.. code-block::

    [Task]
    settings=[{'product_type':0,'number_of_parts':10,"type":'start'},
          {'product_type':0,'number_of_parts':150,"type":'logging'},
          {'product_type':1,'number_of_parts':150,"type":'logging'},
          {'product_type':2,'number_of_parts':150,"type":'logging'},
          {'product_type':0,'number_of_parts':10,"type":'end'}
          ]

Process
+++++++++

**Parameters**

* **settings**: list of dict{'id', 'mean', 'deviation', 'type'}
    * **id**: this number must be identical to the id in the pnml-file and in the machine section
    * **mean**: number
    * **deviation**: number
    * **type**: only 'normal' available


**Code Example**

.. code-block::

    [Process]
    settings=[{'id':0,'mean':5,'deviation':0,'type':'normal'},
        {'id':1,'mean':10,'deviation':2,'type':'normal'},
        {'id':2,'mean':15,'deviation':1,'type':'normal'}]


Transporter
++++++++++++++

**Parameters**

* **number_of_transporter**: defines the number of transporters
* **settings**: list with dict{'number_of_positions', 'location_id', 'speed', 'add_time', 'remove_time'}
    * **number_of_positions**: 1..n
    * **location_id**: number, must be defined in start_location
    * **waiting_time**: idle waiting time
    * **speed**: number
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
* **start_location**: list of dict{'id', 'location'}
    * **id**: number
    * **location**: [x,y,z], list with 3 numbers

**Code Example**

.. code-block::

    [Transporter]
    number_of_transporter=3
    settings=[{'number_of_positions':3,'location_id':0,'speed':3,'waiting_time': 5,'add_time':{'mean':1,'deviation':0.2,'type':'normal'},'remove_time':{'mean':1,'deviation':0.2,'type':'normal'}},
                   {'number_of_positions':3,'location_id':0,'speed':3,'waiting_time': 5,'add_time':{'mean':1,'deviation':0.2,'type':'normal'},'remove_time':{'mean':1,'deviation':0.2,'type':'normal'}},
                   {'number_of_positions':3,'location_id':0,'speed':3,'waiting_time': 5,'add_time':{'mean':1,'deviation':0.2,'type':'normal'},'remove_time':{'mean':1,'deviation':0.2,'type':'normal'}}]
    start_location=[{'id':0,'location':[1,1,0]}]

Defect
++++++++

only needed if a defect is added to the simulation

**Parameters**

* **transporter_defect_possible**: bool, True or False
* **transporter_random**: {'type', 'min', 'max'}
    * **type**: 'random'
    * **min**: 0
    * **max**: number of transporter defect_types -1
* **transporter_normal**: list of dict{'defect_type', 'defect', 'repair'}
    * **defect_type**: any string
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect
* **machine_defect_possible**: bool, True or False
* **machine_random**: {'type', 'min', 'max'}
    * **type**: 'random'
    * **min**: 0
    * **max**: number of transporter defect_types -1
* **machine_normal**: list of dict{'defect_type', 'defect', 'repair'}
    * **defect_type**: any string
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect

**Code Example**

.. code-block::

    [Defect]
    transporter_defect_possible=True
    transporter_random={'type':"random",'min':0,'max':2}
    transporter_normal=[{'defect_type':"short",'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"medium",'defect':{'type':"normal",'mean':1500,'deviation':300},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"long",'defect':{'type':"normal",'mean':2000,'deviation':400},'repair':{'mean':20,'deviation':1,'type':"normal"}}]
    machine_defect_possible=True
    machine_random={'type':"random",'min':0,'max':2}
    machine_normal=[{'defect_type':"short",'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"medium",'defect':{'type':"normal",'mean':1500,'deviation':300},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"long",'defect':{'type':"normal",'mean':2000,'deviation':400},'repair':{'mean':20,'deviation':1,'type':"normal"}}]

Repair
++++++++

only needed when defect is added

**Parameters**

* **machine_repair** = 1..n
* **transporter_repair** = 1..n


**Code Example**

.. code-block::

    [Repair]
    machine_repair=2
    transporter_repair=1

RandomSeed
+++++++++++++

each simulation run through provides the same results, to change it you need to vary the AppendValue

**Parameters**

* **AppendValue**: number


**Code Example**

.. code-block::

    [RandomSeed]
    AppendValue=0


Lvl1 - Advanced
-----------------

A complete example can be viewed under: ``/example/config/for_docu/production_config_lvl1.ini``.
In comparison to **Lvl2 - Intermediate** mostly ``Machine`` and ``Transporter`` changed.

* Lvl 1 is capable of having machines with different queue combination
    * sharing of queues between machines is possible
    * the queue are devided in input_queue and output_queue

Machine
++++++++

the queue id's must be unique

**Parameters**

* **number_of_machines**: defines the number of machines
* **machine_dict**: list with dict{'machine_id', 'queue_input_id', 'queue_output_id', 'process', 'set_up', 'add_time', 'remove_time'}
    * **machine_id**: number
    * **queue_input_id**: list with queue id's
    * **queue_output_id**: list with queue id's
    * **queue_process_id**: list with queue id's, only 1 queue allowed
    * **process**: list with process_id
    * **waiting_time**: idle waiting time
    * **set_up**: list with dict{'start', 'end', 'mean', 'deviation', 'type'}
        * each combination of the process list needs to be initialized (both direction independently)
        * **start**: process_id, from which process_id should the set_up start
        * **end**: process_id, to which process_id should the set_up be performed
        * **mean**: number
        * **deviation**: number
        * **type**: 'normal', the set up can only have a normal distribution
* **queue_dict**: list with dict{'queue_id', 'number_of_positions', 'location', 'add_time', 'remove_time'}
    * **queue_id**: number
    * **number_of_positions**: number
    * **location**: [x,y,z], list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

* **queue_process_dict**: list with dict{'queue_id', 'number_of_positions', 'location', 'add_time', 'remove_time'}
    * **queue_id**: number
    * **number_of_positions**: 1, only 1 is allowed
    * **location**: [x,y,z], list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [Machine]
    umber_of_machines = 4
    machine_dict = [{'machine_id': 0,'waiting_time':5, 'queue_input_id': [5], 'queue_output_id': [2], 'queue_process_id': [12], 'process': [0, 4], 'set_up': [{'start': 0, 'end': 4, 'mean': 0.7251840539819828, 'deviation': 0.0, 'type': 'normal'}, {'start': 4, 'end': 0, 'mean': 1.367229554157118, 'deviation': 0.0, 'type': 'normal'}]},
                   {'machine_id': 1,'waiting_time':5, 'queue_input_id': [2], 'queue_output_id': [3], 'queue_process_id': [13], 'process': [1, 5], 'set_up': [{'start': 1, 'end': 5, 'mean': 1.4874517298755754, 'deviation': 0.0, 'type': 'normal'}, {'start': 5, 'end': 1, 'mean': 0.813406230647941, 'deviation': 0.0, 'type': 'normal'}]},
                   {'machine_id': 2,'waiting_time':5, 'queue_input_id': [3], 'queue_output_id': [4], 'queue_process_id': [14], 'process': [2, 7], 'set_up': [{'start': 2, 'end': 7, 'mean': 0.8800168197636069, 'deviation': 0.0, 'type': 'normal'}, {'start': 7, 'end': 2, 'mean': 1.4140742063085612, 'deviation': 0.0, 'type': 'normal'}]},
                   {'machine_id': 3,'waiting_time':5, 'queue_input_id': [4], 'queue_output_id': [5], 'queue_process_id': [15], 'process': [3, 6], 'set_up': [{'start': 3, 'end': 6, 'mean': 1.3126545004777332, 'deviation': 0.0, 'type': 'normal'}, {'start': 6, 'end': 3, 'mean': 1.1796101423682712, 'deviation': 0.0, 'type': 'normal'}]}]
    queue_dict = [{'queue_id':1, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},{'queue_id':2, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                 {'queue_id':3, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},{'queue_id':4, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                 {'queue_id':5, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},{'queue_id':6, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                 {'queue_id':7, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},{'queue_id':8, 'number_of_positions':3, 'location':[4,5,0],'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                 ]
    queue_process_dict = [{'queue_id':12, 'number_of_positions':1, 'location':[4,5,0], 'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                           {'queue_id':13, 'number_of_positions':1, 'location':[10,5,0], 'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                         {'queue_id':14, 'number_of_positions':1, 'location':[4,15,0], 'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},
                         {'queue_id':15, 'number_of_positions':1, 'location':[20,5,0], 'add_time': {'mean': 1.0685729521901768, 'deviation': 0.28984742714339595, 'type': 'normal'}, 'remove_time': {'mean': 1.5275942986146165, 'deviation': 0.3318619177096951, 'type': 'normal'}},]


Start_Queue
++++++++++++

**Parameters**

* **number_of_queue**: defines the number of start queues
* **settings**: list with dict{'queue_id', 'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **queue_id**: number
    * **number_of_positions**: 1..n
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [Start_Queue]
    number_of_queue = 1
    settings = [{'queue_id':8,'location': [0, 0, 0], 'number_of_positions': 3, 'add_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}, 'remove_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}}]

End_Queue
++++++++++++

**Parameters**

* **number_of_queue**: defines the number of end queues
* **settings**: list with dict{'queue_id', 'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **queue_id**: number
    * **number_of_positions**: only 1 possible
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal

**Code Example**

.. code-block::

    [End_Queue]
    number_of_queue = 1
    settings = [{'queue_id':9,'location': [0, 0, 0], 'add_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}, 'remove_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}}]

Deadlock_Queue
++++++++++++++++

**Parameters**

* **number_of_queue**: defines the number of deadlock queues
* **settings**: list with dict{'queue_id', 'location', 'number_of_positions', 'add_time', 'remove_time'}
    * **queue_id**: number
    * **number_of_positions**: 1..n
    * **location**: [x, y, z] list with 3 numbers
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
* **deadlock_waiting_time**: Time in which the part cannot be transported in the deadlock queue

**Code Example**

.. code-block::

    [Deadlock_Queue]
    number_of_queue=1
    settings=[{'location':[3,3,0],'number_of_positions':5,'add_time': {'mean':1,'deviation':0.2,'type':'normal'},'remove_time': {'mean':1,'deviation':0.2,'type':'normal'}}]
    deadlock_waiting_time = 5

ProductType
+++++++++++++

**Parameters**

* **settings**: list with dict{'id', 'path'}
    * **id**: number
    * **config**: nested list

.. code-block::

    [ProductType]
    settings=[{'id':0,'config':[[0,1,2],[2,2,1,0]]},
         {'id':1,'config':[[0,2,1]]},
         {'id':2,'config':[[0,1,3,4,7]]},
         {'id':3,'config':[[5,6,7,6,0]]},
         {'id':4,'config':[[4,5,2,3,0]]},
         {'id':5,'config':[[0,7,7,6,6,1]]}
                ]

Task
+++++

**Parameters**

* **settings**: list with dict{'product_type', 'number_of_parts', 'type'}
    * **product_type**:
    * **number_of_parts**:
    * **type**: defines the type of task
        * start: these products are not logged, there only task is to reduce the starting effect
        * logging: after the first logging product is inserted the logging starts
        * end: these products are not logged, there only task is to reduce the ending effect, when every logging product is produced the production ends

**Code Example**

.. code-block::

    settings=[{'product_type':0,'number_of_parts':10,"type":'start'},
          {'product_type':0,'number_of_parts':150,"type":'logging'},
          {'product_type':1,'number_of_parts':150,"type":'logging'},
          {'product_type':2,'number_of_parts':150,"type":'logging'},
          {'product_type':0,'number_of_parts':10,"type":'end'}
          ]

Process
+++++++++

**Parameters**

* **settings**: list of dict{'id', 'default', 'adjusted'}
    * **id**: this number must be identical to the id in the pnml-file and in the machine section
    * **default**: dict{'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **adjusted**: list with dict of {'mean': number, 'deviation': number, 'type': 'normal'}
        * (optional) every machine can now have for a process it's own distribution

**Code Example**

.. code-block::

    [Process]
    settings = [{'id': 0, default:{'mean': 6.862095883770332, 'deviation': 0.0, 'type': 'normal'},
    adjusted: [{'machine_id':2,'mean': 6.862095883770332, 'deviation': 0.0, 'type': 'normal'}] }, {'id': 4, 'mean': 5.778627553085438, 'deviation': 0.0, 'type': 'normal'}, {'id': 1, 'mean': 6.927675665841848, 'deviation': 0.0, 'type': 'normal'},
    {'id': 5, 'mean': 3.607603706460525, 'deviation': 0.0, 'type': 'normal'}, {'id': 2, 'mean': 3.3168779683080283, 'deviation': 0.0, 'type': 'normal'}, {'id': 7, 'mean': 5.629809687872099, 'deviation': 0.0, 'type': 'normal'}, {'id': 3, 'mean': 5.158519573931287, 'deviation': 0.0, 'type': 'normal'}, {'id': 6, 'mean': 3.9434044637703973, 'deviation': 0.0, 'type': 'normal'}]



Transporter
++++++++++++++

**Parameters**

* **number_of_transporter**: defines the number of transporters
* **settings**: list with dict{'number_of_positions', route', 'location_id', 'speed', 'add_time', 'remove_time'}
    * **number_of_positions**: 1..n
    * **location_id**: number, must be defined in start_location
    * **speed**: number
    * **add_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **remove_time**: {'mean': number, 'deviation': number, 'type': 'normal'}, type have to be normal
    * **waiting_time**: idle waiting time
    * **route**: dict which provides further information
        * **free**: transporter are allowed to drive to every queue; {'type':'free'}
        * **restricted**: transporter is only allowed to drive to some queues; {'type':'restricted','queue_list': list with queue id's}
        * **ordered**: transporter drives to the defined queues in the exact orders, {'type':'ordered','queue_list': list with queue id's}
            * this option is currently not available
* **start_location**: list of dict{'id', 'location'}
    * **id**: number
    * **location**: [x,y,z], list with 3 numbers

**Code Example**

.. code-block::

    [Transporter]
    number_of_transporter = 3
    settings = [{'number_of_positions': 3,'waiting_time':5, 'location_id': 0,'route':{'type':'free'} ,'speed': 3, 'add_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}, 'remove_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}},
                        {'number_of_positions': 3,'waiting_time':5, 'location_id': 0,'route':{'type':'restricted','queue_list':[5,9,11]}, 'speed': 3, 'add_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}, 'remove_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}},
                     {'number_of_positions': 3,'waiting_time':5, 'location_id': 0,'route':{'type':'ordered','queue_list':[1,2,3,4,5,9,11]}, 'speed': 3, 'add_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}, 'remove_time': {'mean': 1, 'deviation': 0.2, 'type': 'normal'}}]
    start_location = [{'id': 0, 'location': [1, 1, 0]}]

Defect
++++++++

only needed if a defect is added to the simulation

**Parameters**

* **transporter_defect_possible**: bool, True or False
* **transporter_random**: {'type', 'min', 'max'}
    * **type**: 'random'
    * **min**: 0
    * **max**: number of transporter defect_types -1
* **transporter_normal**: list of dict{'defect_type', 'defect', 'repair'}
    * **defect_type**: any string
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect
* **machine_defect_possible**: bool, True or False
* **machine_random**: {'type', 'min', 'max'}
    * **type**: 'random'
    * **min**: 0
    * **max**: number of transporter defect_types -1
* **machine_normal**: list of dict{'defect_type', 'defect', 'repair'}
    * **defect_type**: any string
    * **defect**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the probability of the defect
    * **repair**: dict{'mean': number, 'deviation': number, 'type': 'normal'}
        * defines the repair time of the defect

**Code Example**

.. code-block::

    [Defect]
    transporter_defect_possible=True
    transporter_random={'type':"random",'min':0,'max':2}
    transporter_normal=[{'defect_type':"short",'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"medium",'defect':{'type':"normal",'mean':1500,'deviation':300},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"long",'defect':{'type':"normal",'mean':2000,'deviation':400},'repair':{'mean':20,'deviation':1,'type':"normal"}}]
    machine_defect_possible=True
    machine_random={'type':"random",'min':0,'max':2}
    machine_normal=[{'defect_type':"short",'defect':{'type':"normal",'mean':1000,'deviation':250},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"medium",'defect':{'type':"normal",'mean':1500,'deviation':300},'repair':{'mean':20,'deviation':1,'type':"normal"}},
                      {'defect_type':"long",'defect':{'type':"normal",'mean':2000,'deviation':400},'repair':{'mean':20,'deviation':1,'type':"normal"}}]

Repair
++++++++

only needed when defect is added

**Parameters**

* **machine_repair** = 1..n
* **transporter_repair** = 1..n


**Code Example**

.. code-block::

    [Repair]
    machine_repair=2
    transporter_repair=1

RandomSeed
+++++++++++++

each simulation run through provides the same results, to change it you need to vary the AppendValue

**Parameters**

* **AppendValue**: number


**Code Example**

.. code-block::

    [RandomSeed]
    AppendValue=0

