import configparser

from tests.util.Generator import Generator


class ControllerGenerator(Generator):
    """
    generates controller config data
    """
    def __init__(self, seedParameter):
        """

        :param seedParameter: random paramter
        """
        super().__init__(seedParameter)


    def createConfigDict(self):
        """
        main methode for creating config dict

        :return: configparser element
        """

        controller_config = configparser.ConfigParser()
        controller_config['Controller'] = {}
        controller_config["Controller"]["machine"] = str(self.addMachineController())
        controller_config["Controller"]["transporter"] = str(self.addTransporterController())
        controller_config["Controller"]["orderrelease"] = str(self.addOrderreleaseController())
        controller_config["Controller"]["service_machine"] = str(self.addServiceMachineController())
        controller_config["Controller"]["service_transporter"] = str(self.addServiceTransporterController())

        return controller_config


    def addMachineController(self):
        """
        defines machine controller

        :return: dict
        """

        machineList = ['MachineController_FIFO', 'MachineController_LIFO', 'MachineController_EDD']

        controller_config_machine_dict = {}
        if(self.randomDistribution.random()<0.7):
            controller_config_machine_dict['type'] = 'MachineController_Hybrid'
            controller_config_machine_dict['add'] = {}
            for i in range(0,int(self.randomDistribution.random()*10)%len(machineList) +1):
                controller_config_machine_dict['add'][machineList[i%len(machineList)]] = round(self.randomDistribution.randint(1,99)/100,2)

        else:
            controller_config_machine_dict['add'] = {}
            controller_config_machine_dict["type"]= machineList[int(self.randomDistribution.random()*10)%len(machineList)]

        return controller_config_machine_dict


    def addTransporterController(self):
        """
        defines trasnporter controller
        :return: dict
        """

        transporterList = ['TransporterController_FIFO', 'TransporterController_NJF', 'TransporterController_EDD', 'TransporterController_SQF', 'TransporterController_LIFO']

        controller_config_transporter_dict = {}
        if(self.randomDistribution.random()<0.7):
            controller_config_transporter_dict['type'] = 'TransporterController_Hybrid'
            controller_config_transporter_dict['add'] = {}
            for i in range(0,int(self.randomDistribution.random()*10)%len(transporterList) +1):
                controller_config_transporter_dict['add'][transporterList[i%len(transporterList)]] = round(self.randomDistribution.randint(1,99)/100,2)

        else:
            controller_config_transporter_dict['add'] = {}
            controller_config_transporter_dict["type"]= transporterList[int(self.randomDistribution.random()*10)%len(transporterList)]

        return controller_config_transporter_dict

    def addServiceMachineController(self):
        """
        defines service controller for machine

        :return: dict
        """
        controller_config_dict = {   'type':'ServiceControllerMachine','add':{}  }
        return controller_config_dict


    def addServiceTransporterController(self):
        """
        defines service controller for transporter

        :return: dict
        """
        controller_config_dict = {'type': 'ServiceControllerTransporter', 'add': {}}
        return controller_config_dict

    def addOrderreleaseController(self):
        """
        defines order release controller

        :return: dict
        """
        controller_config_dict = {}
        orderRealaseList = ["OrderReleaseControllerEqual", "OrderReleaseController"]

        controller_config_dict["type"] = orderRealaseList[int(self.randomDistribution.random()*10)%len(orderRealaseList)]
        controller_config_dict["fillLevel"]  =  self.randomDistribution.randint(40,85)/100

        return controller_config_dict

