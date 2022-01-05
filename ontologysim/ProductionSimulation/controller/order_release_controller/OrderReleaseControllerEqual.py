
from owlready2 import *

from ontologysim.ProductionSimulation.controller.order_release_controller.OrderReleaseController import OrderReleaseController
from ontologysim.ProductionSimulation.sim.Enum import Label, OrderRelease_Enum, Evaluate_Enum
from ontologysim.ProductionSimulation.sim.Machine import Machine


class OrderReleaseControllerEqual(OrderReleaseController):
    """
    kind classe by orderrelease, all tasks are processed so that they contain the same number of parts to produce. Leads to a stronger mixing of the processes
    """

    def evaluateOrderRelease(self,event_onto):
        """
        if the boundary conditions fit, i.e. number of free position and tasks available, some parts will be released
        it is only ever released by a Task type parts

        :param event_onto:
        """

        time = self.orderRelease.simCore.getCurrentTimestep()

        self.orderRelease.simCore.event.remove_from_event_list(event_onto)
        self.orderRelease.simCore.event.store_event(event_onto)

        position_list = []
        for start_queue in self.orderRelease.simCore.central.start_queue_list:
            position_list.extend(start_queue.has_for_position)
        number_free_position = len([position for position in position_list if position.blockedSpace == 0])
        # print("number free position",number_free_position)
        task_list = []
        createNewEvaluationEvent = False

        if number_free_position > 0:
            task_list, createNewEvaluationEvent = self.getTaskList(event_onto)

            if len(task_list)>0:

                task_list.sort(key=lambda x:x[1],reverse=True)
                number_of_products=task_list[0][1]

                if number_of_products>number_free_position:
                    number_of_products=number_free_position
                #print("create_release",time,task_list[0][0])
                self.orderRelease.create_release(task_list[0][0],number_of_products,time)

                if self.min_next_task!= None:
                    if(self.min_next_task.start_time<time):
                        self.min_next_task=None


            elif self.min_next_task != None and createNewEvaluationEvent:

                event_onto = self.orderRelease.simCore.event.createEvent(self.min_next_task.start_time,
                                                                         Evaluate_Enum.OrderRelease, 0)

        if self.orderRelease.simCore.central.number_of_start_positions<2:

            event_onto = self.orderRelease.simCore.event.createEvent(self.orderRelease.simCore.getCurrentTimestep()+5,
                                                                     Evaluate_Enum.OrderRelease, 0)

