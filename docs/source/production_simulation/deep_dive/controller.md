Controller
============

## Introduction


Each controller variant is assigned an event type and has a 
defined call method. These are listed in the following table

Types of controller:


| Type                         | Event type          | Method                     |
| ---------------------------- | ------------------- | -------------------------- |
| MachineController            | Machine             | evaluateMachine            |
| TransporterController        | Transporter         | evaluateTransporter        |
| OrderReleaseController       | OrderRelease        | evaluateCreateOrderRelease |
| OrderReleaseController       | Release             | evaluateOrderRelease       |
| ServiceControllerTransporter | EvTransporterDefect | evaluateService            |
| ServiceControllerMachine     | EvMachineDefect     | evaluateService            |

  
## How to create your own controller?


1. Create your own controller class
    * which has the same entry method as described in the table.
    * to override the current controller import them from `from ontologysim.ProductionSimulation.controller.machine_controller.*`
2. add your controller to your main
    * Attention: pay attention to the same import method as in the example
    * filename and class are equal
    * don't import the class directly, only import the file

    
An *example* is shown in the example folder

1. MachineController_FIFO2.py in `/example/controller/MachineController_FIF02.py`
2. imported in the Main.py
    * `from example.controller import MachineController_FIFO2`