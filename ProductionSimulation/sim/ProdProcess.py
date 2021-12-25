from ProductionSimulation.sim.Enum import Label


class ProdProcess:


    def __init__(self, simCore):
        """

        """
        self.simCore = simCore
        self.process_config = {}
        self.meanProcessTimeDict = {}

    def ini_dict(self,process_config_list):
        """
        initialize dict, which add process donfig to dict
        :param process_config_list:
        :return:
        """

        for process_config_it in process_config_list:

            self.process_config[process_config_it['id']] = process_config_it



    def createProdProces(self,process_id,machineInstance=None):
        """
        create prod process
        :param process_id:
        :param machineInstance:
        :return:
        """

        prod_processInstance = None
        process_config = self.process_config[process_id]

        prod_processInstance = self.simCore.central.prod_process_class(
                Label.ProdProcess.value + str(self.simCore.prod_process_id), namespace=self.simCore.onto)
        prod_processInstance.is_prodprocess_of_process.append(self.simCore.onto[Label.Process.value + str(process_config['id'])])

        if 'adjusted' in process_config.keys():

            machine_id = (int)((machineInstance.name).replace(Label.Machine.value, ''))

            distributionInstance = None
            for dict_adjusted in process_config['adjusted']:
                if machine_id == dict_adjusted['machine_id']:
                    distributionInstance = self.simCore.distribution.createDistribution(dict_adjusted,
                                                                                        prod_processInstance.name)
                    break
            if distributionInstance == None:
                distributionInstance = self.simCore.distribution.createDistribution(process_config['default'],
                                                                                    prod_processInstance.name)
        else:

            distributionInstance = self.simCore.distribution.createDistribution(process_config['default'],
                                                                                prod_processInstance.name)

        self.meanProcessTimeDict[prod_processInstance.name] = distributionInstance.mean
        prod_processInstance.has_for_prod_distribution.append(distributionInstance)
        self.simCore.prod_process_id += 1

        return prod_processInstance

    def transformSubProduct(self):
        """
        TODO for merge
        :return:
        """
        pass

    def getID(self,prodProcessInstance):
        """
        get id of process id of prodProcess instance
        :param prodProcessInstance: onto
        :return: int
        """
        return prodProcessInstance.is_prodprocess_of_process[0].process_id
