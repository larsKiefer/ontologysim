from owlready2 import *

from ProductionSimulation.sim.Enum import Label, Evaluate_Enum


class Task:
    """
    handles the tasks in onto
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

    def createTask(self, product_type_onto, number_of_products, task_type="logging",start_time=0):
        """
        creates a new task in onto, tasks types: start, logging, end

        :param product_type_onto: onto
        :param number_of_products: number
        :param task_type: str
        """
        taskInstance = self.simCore.central.task_class(Label.Task.value + str(self.simCore.task_id))
        taskInstance.number = number_of_products
        taskInstance.todo_number = number_of_products
        taskInstance.has_for_product_type_task.append(product_type_onto)
        taskInstance.task_type = task_type
        taskInstance.start_time = start_time
        self.simCore.task_id += 1

    def updateTaskList(self):
        """
        sets the task list in central class
        """
        self.simCore.central.task_list = self.simCore.onto.search(type=self.simCore.central.task_class)

    def transformToDict(self,id):
        """
        transform to dict
        :param id: string
        :return:
        """
        response_dict = {}
        if (id == "all"):
            task_list = [task_onto for task_onto in
                                 self.simCore.onto.search(type=self.simCore.central.task_class)]
        else:
            task_list = [self.simCore.onto[id]]
        if task_list == [None]:
            return {'error': "id_not_found"}
        for task_onto in task_list:
            response_dict[task_onto.name] = {}
            response_dict[task_onto.name]['number'] = task_onto.number
            response_dict[task_onto.name]['todo_number'] = task_onto.todo_number
            response_dict[task_onto.name]['start_time'] = task_onto.start_time
            response_dict[task_onto.name]['task_type'] = task_onto.todo_number
            response_dict[task_onto.name]['product_type'] = task_onto.has_for_product_type_task[0].name

        return response_dict
