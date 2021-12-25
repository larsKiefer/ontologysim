from collections import defaultdict

from ProductionSimulation.controller.machine_controller.MachineController import MachineController
from ProductionSimulation.sim.Enum import Queue_Enum


class MachineController_EDD(MachineController):
    """
    EDD= Earlist Due Date, since there is currently no due date, the start time is used for the production of the part
    """

    def sort_products(self, machine_onto):
        """
        output of all products in the machine queue, scheduled after EDD

        :param machine_onto:
        :return:
        """
        erg_queue = machine_onto.has_for_input_queue
        erg = []
        for queue in erg_queue:
            position_list = queue.has_for_position
            for position in position_list:
                for product in position.has_for_product:
                    if product.blocked_for_machine == 0 and product.has_for_product_state[0].state_name != "sink":
                        erg.append([product, product.start_of_production_time])
        erg.sort(key=lambda x: x[1])

        return erg
