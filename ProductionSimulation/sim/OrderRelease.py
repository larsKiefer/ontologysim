from owlready2 import *

from ProductionSimulation.sim.Enum import Label, Evaluate_Enum, OrderRelease_Enum


class OrderRelease:
    """
    handles the order release process at the starting queues
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore
        self.orderReleaseController = None
        self.number_of_positions = 0
        self.max_number = 0
        self.current_number_of_products = 0

    def setMaxNumber(self, percent):
        """
        given a percentage of the fill level of the production the max number of parts are getting calculated
        the start and end queues are not considered, the process queue positions, were count

        :param percent: double
        """
        self.number_of_positions = len(
            [position for position in self.simCore.onto.search(type=self.simCore.central.position_class) if
             not (Label.EndQueue.value in position.is_queue_of.__getitem__(0).name) and not (
                         Label.StartQueue.value in position.is_queue_of.__getitem__(0).name)])

        self.max_number = self.number_of_positions * percent

    def addOrderReleaseController(self, orderReleaseController):
        """
        combines Order release controller with controller

        :param orderReleaseController: Order release controller
        """
        self.orderReleaseController = orderReleaseController
        orderReleaseController.orderRelease = self

    def release(self, event_onto):
        """
        adding parts to the start queue

        :param event_onto: onto
        """
        number_of_parts = event_onto.number_of_products

        task_onto = event_onto.has_for_task_event.__getitem__(0)

        product_type_onto = task_onto.has_for_product_type_task.__getitem__(0)
        self.simCore.logger.evaluatedInformations(
            [{"type": event_onto.type, "event_onto_time": event_onto.time, "number_of_products": number_of_parts,
              "product_type": product_type_onto.name}])

        self.simCore.event.add_to_logger(event_onto)
        self.simCore.event.remove_from_event_list(event_onto)
        self.simCore.event.store_event(event_onto)

        products = []
        for i in range(number_of_parts):
            product_onto = self.simCore.product.createProduct(product_type_onto)

            products.append(product_onto)
        time = self.simCore.getCurrentTimestep()
        if len(products) > 0:
            i = 0
            for start_queue_instance in self.simCore.central.start_queue_list:

                positions = start_queue_instance.has_for_position

                for position in positions:
                    if position.blockedSpace == 0:
                        position.has_for_product.append(products[i])

                        position.blockedSpace = 1
                        self.simCore.queue.create_change_for_start_queue(products[i], position, time)
                        i += 1
                        if i >= len(products):
                            break
                if i >= len(products):
                    break

        self.orderReleaseController.evaluateCreateOrderRelease()

    def create_release(self, task_onto, number_of_parts, time):
        """
        creating a release event and reduces the number of todos in task

        :param task_onto: onto
        :param number_of_parts: number
        :param time: double
        """
        event_onto = self.simCore.event.createEvent(time, OrderRelease_Enum.Release, 0)
        self.simCore.event.add_task_to_event(event_onto, task_onto)
        event_onto.number_of_products = number_of_parts
        task_onto.todo_number -= number_of_parts
        self.current_number_of_products += number_of_parts

