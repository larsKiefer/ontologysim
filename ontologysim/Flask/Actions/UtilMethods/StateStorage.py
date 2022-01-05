from ontologysim.ProductionSimulation.sim.Enum import Evaluate_Enum, Machine_Enum, Queue_Enum, Transporter_Enum, OrderRelease_Enum, \
    Product_Enum


class StateStorage(object):
    """

    saves all states (current event) in a dictionary
    """

    def __init__(self,simCore):
        """

        :param simCore: SimCore object
        """
        self.simCore=simCore
        self.machine={}
        self.product={}
        self.queue={}
        self.position={}
        self.transporter={}
        self.lastProcess={}
        self.rememberProcess={}


    def changeState(self,event_onto):
        """
        changing all state of the associated objects when triggering a new event

        :param event_onto: event onto
        """
        event_type= event_onto.type
        if event_type == Evaluate_Enum.Machine.value:
            machine_onto = event_onto.has_for_machine_event[0]
            self.machine[machine_onto.name] = {"state":event_type, "timeDiff": event_onto.time_diff}
        elif event_type == Evaluate_Enum.Product.value:
            pass
        elif event_type == Evaluate_Enum.Transporter.value:
            transport_onto = event_onto.has_for_transport_event[0]
            self.transporter[transport_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff
                                                     }
        elif event_type == Evaluate_Enum.ProductFinished.value:
            pass
        elif event_type == Evaluate_Enum.OrderRelease.value:
            pass
        elif event_type == Machine_Enum.Defect.value:

            machine_onto = event_onto.has_for_machine_event[0]
            self.machine[machine_onto.name] = {"state":event_type, "timeDiff": event_onto.time_diff}

        elif event_type == Machine_Enum.SetUp.value:

            process_onto = event_onto.has_for_process_event.__getitem__(0)
            machine_onto = process_onto.is_prodprocess_of.__getitem__(0)

            self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

        elif event_type == Machine_Enum.Wait.value:

            machine_onto = event_onto.has_for_machine_event.__getitem__(0)
            self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

        elif event_type == Machine_Enum.Process.value:

            process_onto = event_onto.has_for_process_event.__getitem__(0)
            machine_onto = process_onto.is_prodprocess_of.__getitem__(0)
            self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff,"process":process_onto.is_prodprocess_of_process[0].process_id}

            self.rememberProcess[machine_onto.name]=process_onto.is_prodprocess_of_process[0].process_id
            #get Product: product_onto_list[0]

        elif event_type == Queue_Enum.Change.value:

            product_onto = event_onto.has_for_product_event.__getitem__(0)
            oldPosition = product_onto.is_position_of.__getitem__(0)
            new_position_onto = event_onto.has_for_position_event.__getitem__(0)
            old_queue = oldPosition.is_queue_of.__getitem__(0)
            queue = new_position_onto.is_queue_of.__getitem__(0)

            if event_onto.additional_type == Queue_Enum.RemoveFromTransporter.value:
                transporter_onto = old_queue.is_transp_queue_of[0]
                self.transporter[transporter_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff
                                                       }
            elif event_onto.additional_type == Queue_Enum.AddToTransporter.value:
                transporter_onto = queue.is_transp_queue_of[0]
                self.transporter[transporter_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff
                                                         }

            elif event_onto.additional_type == Queue_Enum.EndProcess.value:
                machineOntoList = old_queue.is_for_queue_process_of
                machine_onto = machineOntoList[0]
                self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}
                if (machine_onto.name in self.rememberProcess.keys()):
                    self.lastProcess[machine_onto.name] = self.rememberProcess[machine_onto.name]

            elif event_onto.additional_type == Queue_Enum.StartProcess.value:
                machineOntoList = queue.is_for_queue_process_of
                machine_onto = machineOntoList[0]
                self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

            elif event_onto.additional_type == Queue_Enum.StartProcessStayBlocked.value:
                machineOntoList = queue.is_for_queue_process_of
                machine_onto = machineOntoList[0]
                self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}


            elif event_onto.additional_type == Queue_Enum.RemoveFromTransporterDeadlock.value:
                transporter_onto = old_queue.is_transp_queue_of[0]
                self.transporter[transporter_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}


        elif event_type == Transporter_Enum.Defect.value:

            transport_onto = event_onto.has_for_transport_event[0]
            self.transporter[transport_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff
                                                     }

        elif event_type == Transporter_Enum.Transport.value:

            new_location_onto = event_onto.has_for_location_event.__getitem__(0)
            transport_onto = event_onto.has_for_transport_event.__getitem__(0)
            old_location = transport_onto.has_for_transp_queue.__getitem__(0).has_for_queue_location.__getitem__(0)

            newQueueLocation = self.simCore.location.location_queue_dict["location"][new_location_onto.name]
            oldQueueLocation = self.simCore.location.location_queue_dict["location"][old_location.name]

            self.transporter[transport_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff,"newLocation":newQueueLocation,"oldLocation":oldQueueLocation}

        elif event_type == Transporter_Enum.Wait.value:

            transport_onto=event_onto.has_for_transport_event[0]

            self.transporter[transport_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

        elif event_type == OrderRelease_Enum.Release.value:
            pass
        elif event_type == Evaluate_Enum.TransporterDefect.value:
            service_onto = event_onto.has_for_service_event[0]
            transport_onto = service_onto.has_for_wait_transporter_service[0]
            self.transporter[transport_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

        elif event_type == Evaluate_Enum.MachineDefect.value:
            service_onto = event_onto.has_for_service_event[0]
            machine_onto = service_onto.has_for_wait_machine_service[0]
            self.machine[machine_onto.name] = {"state": event_type, "timeDiff": event_onto.time_diff}

        elif event_type == Product_Enum.EndBlockForTransporter.value:
            pass
        else:
            raise Exception("event type does not exist: " + str(event_type) + ", " + str(event_onto))

