
from owlready2 import *

from ProductionSimulation.sim.Enum import Label, OrderRelease_Enum, Evaluate_Enum
from ProductionSimulation.sim.Machine import Machine


class OrderReleaseController:
    """
    main class for the order release process, each task is processed one after another
    """
    def __init__(self):
        self.orderRelease=None #add it over machine.addOrderReleaseController
        self.min_next_task=None


    def evaluateCreateOrderRelease(self):
        """
        Entry class for evaluating whether a new order should be created,

        check if order realease event will be created
        """

        if self.orderRelease.max_number > self.orderRelease.current_number_of_products:
            position_list=[]
            for start_queue in self.orderRelease.simCore.central.start_queue_list:
                position_list.extend(start_queue.has_for_position)

            number_free_position = 0
            for position in position_list:
                if position.blockedSpace == 0:
                    number_free_position += 1

            event_list = self.orderRelease.simCore.onto[Label.EventList.value + "0"].has_for_event

            number_of_events = 0
            for event in event_list:
                if event.type == OrderRelease_Enum.Release.value or event.type == Evaluate_Enum.OrderRelease.value:
                    number_of_events = 1
                    break

            number_of_todos = sum([task.todo_number for task in self.orderRelease.simCore.central.task_list])


            number_of_free_positions_deadlock = 0
            for deadlock_queue in self.orderRelease.simCore.central.dead_lock_list:
                number_of_free_positions_deadlock = self.orderRelease.simCore.queue.get_number_of_free_positions(deadlock_queue)

            if number_free_position > 0 and number_of_events == 0 and number_of_todos > 0 and number_of_free_positions_deadlock >0:
                #print(self.orderRelease.simCore.getCurrentTimestep(),Evaluate_Enum.OrderRelease)
                event_onto = self.orderRelease.simCore.event.createEvent(self.orderRelease.simCore.getCurrentTimestep(),
                                                            Evaluate_Enum.OrderRelease, 0)



    def evaluateOrderRelease(self,event_onto):
        """
        if the boundary conditions fit, i.e. number of free position and tasks available, some parts will be released

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

        if(number_free_position>0):
            task_list, createNewEvaluationEvent = self.getTaskList(event_onto)

            if len(task_list)>0:

                number_of_products=task_list[0][1]

                if number_of_products>number_free_position:
                    number_of_products=number_free_position

                self.orderRelease.create_release(task_list[0][0],number_of_products,time)

            elif self.min_next_task != None and createNewEvaluationEvent:
                event_onto=self.orderRelease.simCore.event.createEvent(self.min_next_task.start_time,Evaluate_Enum.OrderRelease,0)

        if self.orderRelease.simCore.central.number_of_start_positions<2:
            event_onto = self.orderRelease.simCore.event.createEvent(self.orderRelease.simCore.getCurrentTimestep()+5,
                                                                     Evaluate_Enum.OrderRelease, 0)

    def getTaskList(self, event_onto):
        """
        get task list of open tasks
        :param event_onto: onto element
        :return: task_list:[[task, task.todo_number, task.has_for_product_type_task.__getitem__(0)],...], createNewEvaluationEvent: bool
        """
        task_list = []
        createNewEvaluationEvent = False
        time = self.orderRelease.simCore.getCurrentTimestep()
        # print("number free position",number_free_position)

        if (self.min_next_task != None):
            if (self.min_next_task.start_time > time):
                createNewEvaluationEvent = True
            else:
                self.min_next_task = None

        if (not self.orderRelease.simCore.central.simInstance.allStartTasksFinished):
            task_list = [[task, task.todo_number, task.has_for_product_type_task.__getitem__(0)] for task in
                         self.orderRelease.simCore.central.task_list if
                         task.todo_number > 0 and task.task_type == "start"]

            if len(task_list) == 0:
                self.orderRelease.simCore.central.simInstance.allStartTasksFinished = True
            else:
                createNewEvaluationEvent = True
        if self.orderRelease.simCore.central.simInstance.allStartTasksFinished and not self.orderRelease.simCore.central.simInstance.allLoggingTasksFinished:

            for task in self.orderRelease.simCore.central.task_list:

                if task.todo_number > 0 and task.task_type == "logging":

                    if task.start_time > time and not createNewEvaluationEvent:

                        if self.min_next_task == None:
                            self.min_next_task = task
                        elif self.min_next_task.start_time > task.start_time:
                            self.min_next_task = task
                    elif task.start_time <= time:
                        task_list.append([task, task.todo_number, task.has_for_product_type_task.__getitem__(0)])

            # task_list = [[task, task.todo_number, task.has_for_product_type_task.__getitem__(0)] for task in
            #             self.orderRelease.simCore.central.task_list if
            #             task.todo_number > 0 and task.task_type == "logging"]

            if self.orderRelease.simCore.logger.start_logging == False:
                self.orderRelease.simCore.logger.setStartLogger(time)

            if len(task_list) == 0 and self.min_next_task == None:
                self.orderRelease.simCore.central.simInstance.allLoggingTasksFinished = True
            elif len(task_list) > 0:
                self.min_next_task = None

        if self.orderRelease.simCore.central.simInstance.allStartTasksFinished and self.orderRelease.simCore.central.simInstance.allLoggingTasksFinished:
            task_list = [[task, task.todo_number, task.has_for_product_type_task.__getitem__(0)] for task in
                         self.orderRelease.simCore.central.task_list if
                         task.todo_number > 0 and task.task_type == "end"]

        return task_list, createNewEvaluationEvent