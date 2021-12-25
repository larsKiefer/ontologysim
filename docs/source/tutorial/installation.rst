Installation
==============

git lab
-----------

A stable version of Production simulation is periodically updated on the master and installed as follows:

.. code-block:: console

   git clone https://git.scc.kit.edu/ov0653/ontologysim.git
   cd ontologysim
   pip3 install -r requiirements.txt



How to check if everything works
---------------------------------------------

run in the example folder the `Main.py`


Problem handling
--------------------

Owlready2.0
~~~~~~~~~~~~

**Java Path**``

* to use owlready correctly, your java path needs to be set in the ``owl_config.ini`` 
    * [owl introduction](../configs/owl/owl_config)

**Java Memory**

if this error occurs

.. code-block:: console

   owlready2.base.OwlReadyJavaError: Java error message is:
   Error occurred during initialization of VM
   Could not reserve enough space for 2048000KB object heap


then you need to reduce the java memory

1. goto "site-packages\owlready2\reasoning.py"
2. reduce the Java Memory variable to 500

Database
~~~~~~~~~~~~

if a database error occurs

1. Check if file in ProductionSimulation/database/SimulationRun.db exist, otherwise create the missing file
2. run CreateDatabase.py in  ProductionSimulation/database