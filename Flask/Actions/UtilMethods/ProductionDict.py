from ProductionSimulation.sim.Enum import Label


class ProductionDict():
    """

    class wicht transform ontologysim into dict
    """

    @classmethod
    def getProductionDict(cls, simCore):
        """
        transform ontologysim to production dict

        :param simCore:
        :return: dict
        """
        stateStorage = simCore.stateStorage

        response_dict = {}

        response_dict[Label.Transporter.name] = simCore.transport.transformToDict("all")

        for key,value in response_dict[Label.Transporter.name].items():
            if(stateStorage!=None):
                if(key in stateStorage.transporter.keys()):
                    response_dict[Label.Transporter.name][key]["state"] = stateStorage.transporter[key]
                else:
                    response_dict[Label.Transporter.name][key]["state"] = {}
            else:
                response_dict[Label.Transporter.name][key]["state"] = {}

            timeKPIs = simCore.logger.transporterLogger.time_kpis
            astKPI = 0
            attKPI = 0
            if(key in timeKPIs.keys()):
                if ("AUTTp" in timeKPIs[key].keys()):
                    if (len(timeKPIs[key]["AUTTp"]) > 1):
                        attKPI = timeKPIs[key]["AUTTp"][len(timeKPIs[key]["AUTTp"])-2]

                if ("AUSTp" in timeKPIs[key].keys()):

                    if (len(timeKPIs[key]["AUSTp"]) > 1):
                        astKPI = timeKPIs[key]["AUSTp"][len(timeKPIs[key]["AUSTp"])-2]

            response_dict[Label.Transporter.name][key]["kpi"] = {"AUTTp": attKPI, "AUSTp": astKPI}

        response_dict[Label.Machine.name] = simCore.machine.transformToDict("all")

        for key,value in response_dict[Label.Machine.name].items():
            if(stateStorage!=None):
                if(key in stateStorage.machine.keys()):
                    response_dict[Label.Machine.name][key]["state"] = stateStorage.machine[key]
                    if(key in stateStorage.lastProcess.keys()):
                        response_dict[Label.Machine.name][key]["last_process"] = stateStorage.lastProcess[key]
                else:
                    response_dict[Label.Machine.name][key]["state"] = {}
            else:
                response_dict[Label.Machine.name][key]["state"] = {}

            timeKPIs=simCore.logger.machineLogger.time_kpis
            aptKPI=0
            astKPI = 0
            if (key in timeKPIs.keys()):
                if("APTp" in  timeKPIs[key].keys()):
                    if(len(timeKPIs[key]["APTp"])>1):
                        aptKPI=timeKPIs[key]["APTp"][len(timeKPIs[key]["APTp"])-2]

                if("ASTp" in timeKPIs[key].keys()):
                    if (len(timeKPIs[key]["ASTp"]) > 1):
                        astKPI = timeKPIs[key]["ASTp"][len(timeKPIs[key]["ASTp"])-2]

            response_dict[Label.Machine.name][key]["kpi"]={"APTp":aptKPI,"ASTp":astKPI}

        response_dict[Label.StartQueue.name] = {}
        for queue_onto in simCore.central.start_queue_list:
            response_dict[Label.StartQueue.name] = simCore.queue.transformToDict(
                queue_onto.name)

        response_dict[Label.DeadlockQueue.name] = {}
        for queue_onto in simCore.central.dead_lock_list:
            response_dict[Label.DeadlockQueue.name] = simCore.queue.transformToDict(
                queue_onto.name)

        response_dict[Label.EndQueue.name] = {}
        for queue_onto in simCore.central.end_queue_list:
            response_dict[Label.EndQueue.name] = simCore.queue.transformToDict(
                queue_onto.name)

        response_dict['MachineQueue'] = {}
        for queue_onto in simCore.central.machine_queue_list:
            response_dict['MachineQueue'][queue_onto.name] = simCore.queue.transformToDict(
                queue_onto.name)[queue_onto.name]

        response_dict['ProcessQueue'] = {}
        for machine_onto in simCore.central.machine_list:
            for queue_onto in machine_onto.has_for_queue_process:
                response_dict['ProcessQueue'][queue_onto.name] = simCore.queue.transformToDict(queue_onto.name)[queue_onto.name]

        response_dict['TransporterQueue'] = {}
        for queue_onto_name in simCore.central.queue_to_transporter.keys():
            response_dict['TransporterQueue'][queue_onto_name] = simCore.queue.transformToDict(
                queue_onto_name)[queue_onto_name]

        response_dict["Position"] = {}
        for position_onto in simCore.onto.search(type=simCore.central.position_class):
            response_dict["Position"][position_onto.name] = simCore.position.transformToDict(
                position_onto.name)[position_onto.name]

        response_dict["ProductType"] = {}
        for productTypeOnto in simCore.onto.search(type=simCore.central.product_type_class):
            response_dict["ProductType"][productTypeOnto.name] = simCore.product_type.transformToDict(
                productTypeOnto.name)[productTypeOnto.name]

        response_dict["Product"] = {}
        for productOnto in simCore.onto.search(type=simCore.central.product_class):
            response_dict["Product"][productOnto.name] = simCore.product.transformToDict(
                productOnto.name)[productOnto.name]

        response_dict["Task"] = {}
        for taskOnto in simCore.onto.search(type=simCore.central.task_class):
            response_dict["Task"][taskOnto.name] = simCore.task.transformToDict(taskOnto.name)[taskOnto.name]



        return response_dict



