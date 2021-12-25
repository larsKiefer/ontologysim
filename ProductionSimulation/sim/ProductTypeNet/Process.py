from ProductionSimulation.sim.Enum import Label


class Process:
    """
    handles the petri nets and the production process onto
    """
    def __init__(self,simCore):
        """

        :param simCore:
        """
        self.simCore=simCore

    def createProcess(self,process_config):
        """

        create process in ontologysim
        :param process_config: dict
        :return:
        """

        processInstance =self.simCore.central.process_class(Label.Process.value + str(process_config["id"]))
        processInstance.combine_process = False
        processInstance.process_id = process_config["id"]

class MergeProcess(Process):
    """
    is used for merge and split process
    """

    def createProcess(self,process_config):
        """

        create process in ontologysim
        :param process_config: dict
        :return:
        """
        processInstance =self.simCore.central.merge_process_class(Label.Process.value + str(process_config["id"]))
        processInstance.process_id = process_config["id"]
        processInstance.combine_process = True

        for in_config in process_config["merged"]["in"]:
            combine_process_data_onto = self.createCcombineProcessData(in_config)
            processInstance.has_for_input_combine.append(combine_process_data_onto)

        for out_config in process_config["merged"]["out"]:
            combine_process_data_onto = self.createCcombineProcessData(out_config)
            processInstance.has_for_output_combine.append(combine_process_data_onto)

    def createCcombineProcessData(self,config):
        """

        :param config:
        :return:
        """
        combineProcessDataInstance = self.simCore.central.combine_process_data_class(Label.CombineProcessData.value + str(self.simCore.combine_process_data_id))
        combineProcessDataInstance.number_state= config["number"]
        self.simCore.combine_process_data_id+=1

        return combineProcessDataInstance