from collections import defaultdict

from ontologysim.ProductionSimulation.controller.machine_controller.MachineController import MachineController
from ontologysim.ProductionSimulation.sim.Enum import Queue_Enum


class MachineController_LIFO(MachineController):
    """
    LIFO =Last in First out, maschine controller based on LIFO (shortest waiting time in queue)

    """

    def sort_products(self, machine_onto):
        """
        output of all products in the machine queue, scheduled after LIFO

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
                        event_list = position.is_position_event_of
                        for event in event_list:
                            if event.type == Queue_Enum.Change.value:
                                erg.append([product, event.time])
        erg.sort(key=lambda x: x[1])

        res = defaultdict(list)
        for v, k in erg: res[v].append(k)

        erg = [[k, v[-1]] for k, v in res.items()]
        erg.sort(key=lambda x: x[1], reverse=True)
        return erg
