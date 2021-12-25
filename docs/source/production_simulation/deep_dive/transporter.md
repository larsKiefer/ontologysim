Transporter
===================

Transporter types
------------------
 
 ### Free:
 
 The transporter vehicles are not restricted to a route or limit to a place
 
 ### Restricted: 
 
 The transporter is only allowed to drive to certain queues, the order doesn't matter
 
 ### Ordered:
 
  > currently not working
>
 The transporter is only allowed to drive to certain queues, the order can not be changed.

 
Deadlock
----------

The current transporter controller contains a deadlock detection and deadlock strategy

### Detection:

The transporter scans all parts in machine, start and end queues and evaluates them according to a heuristic e.g. FIFO. These evaluated parts are then checked to see if the next machine is available. If no machine is available for the product, the next prioritised part is evaluated. If no part can be processed further. If a deadlock handling is carried out.

### Deadlock strategy:

At deadlock the transporter first drives to a start queue if there is still room for an additional product. If this is not the case, it places a part in the deadlock queue as soon as a part is placed in the deadlock queue. 
Then no more new parts are inserted into the system. After removing one part from the transporter. The evaluation starts again. The parts on the deadlock queue are blocked for transportation for a certain time.

> Important: for Restricted or Ordered Transporters the deadlock and start queues does not need to be added. For a deadlock case the transporter is allowed to drive to these queues