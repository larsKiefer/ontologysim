Simulation
===================

Introduction
--------------

This production simulation is an ontology-based deterministic, time-discrete simulation
This has the following implications:

* The data and knowledge are stored in the Ontology. A python class has been created on the most important ontology classes to make it easier to change the ontology.
    * the simulation can be saved at any time
    * high degrees of freedom and possibilities


Main concept
---------------

### Ontology

* unique names are set for the quick access of ontology instances. These always consist of the 'Label(Enum)` and a number
* except for the event_logger the owl connections are always on both sides to allow access to the data

*Restrictions*
* the machine can only have one queue with on position
* the transport has only one queue
* no due date, no quality of products

### Simulation

* the main class is the simCore class
* An action in the simulation always consists of 2 events. First, an evaluation Event. The action is determined and then executed at a later time. 
    * the actual event always marks the end of an action. Example: if the event "process" is called at time t, then the action was executed between t-(delta t) and t
    * so it is more complicated to find out the current state of affairs, as this was only done in the future. To find out the current state anyway, the 'Event list' must be searched
* the defect does not interrupt the current action
* the simulation loop for the next events is the main method in SimCore
* for first start view: [create a simulation](../../tutorial/creating_a_simulation.md)


UML-Python
--------------

The following picture should give a short overview of the python classes

![UML](UML.png "UML")

for the ontology structure view:  [ontology](ontology.md)
