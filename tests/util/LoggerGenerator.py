import configparser

from tests.util.Generator import Generator


class LoggerGenerator(Generator):
    """
    Logger generator
    """

    def __init__(self,seedParameter,path):
        """

        :param seedParameter: int: random parameter
        :param path: string: for saving csv
        """
        super().__init__(seedParameter)
        self.path = path

    def createConfigDict(self):
        """
        main methode for creating config dict

        :return: configparser element
        """
        logger_config = configparser.ConfigParser()
        lvl="lvl3"
        logger_config["Type"] = self.addType(lvl)
        logger_config['KPIs'] = self.addKPIs()
        logger_config["ConfigIni"] = self.addConfigIni()
        logger_config["Plot"] = self.addPlot()
        logger_config["Save"] = self.addSave()

        return logger_config


    def addKPIs(self):
        """
        define KPI settings

        :return: dict
        """

        config = {}
        config["time_interval"] = 100
        config["log_summary"] = True if self.randomDistribution.random()>0.5 else False
        config["log_time"] = True if self.randomDistribution.random() > 0.5 else False
        config["log_events"] = True if self.randomDistribution.random() > 0.5 else False
        config["path"] = self.path

        return config

    def addConfigIni(self):
        """
        define config settings

        :return: dict
        """
        config = {}
        config["addIni"] = False
        config["path"] = "/example/config/"

        return config

    def addPlot(self):
        """
        define plot settings

        :return: dict
        """
        config = {}

        config["plot"] = True if self.randomDistribution.random()>0.5 else False
        config["number_of_points_x"] = 15
        # max 3 values
        config["data"] = [{'object_name': 'all', 'kpi': 'AE', 'type': 'machine'},
                {'object_name': 'all', 'kpi': 'AUIT', 'type': 'transporter'},
                {'object_name': 'all', 'kpi': 'AOET', 'type': 'product'}]

        return config

    def addSave(self):
        """
        define save settings

        :return: dict
        """
        config = {}
        config["csv"] = True if self.randomDistribution.random()>0.3 else False
        config["database"] = True if self.randomDistribution.random()>0.6 else False
        config["path"] = "/ontologysim/example/log/"
        config["sql_alchemy_database_uri"] = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"

        return config



