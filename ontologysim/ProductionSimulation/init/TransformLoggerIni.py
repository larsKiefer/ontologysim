from ontologysim.ProductionSimulation.logger.Enum_Logger import Logger_Enum


class TransformLoggerIni:
    """
    there are multiple config structures available,
    currently lvl2 and lvl3
    lvl1 is the most detailed, all config-files are getting converted to lvl1

    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

    def transform_ini(self, logger_ini={}):
        """
        main method, which transform the config-file

        :param production_ini:
        :return:
        """
        output_ini = {}
        type = logger_ini['Type']['type']

        output_ini['Tpye'] = {'type': 'lvl1'}
        output_ini['KPIs'] = self.transform_kpis(type, logger_ini['KPIs'])
        output_ini['ConfigIni'] = self.transform_config_ini(type, logger_ini['ConfigIni'])
        output_ini['Plot'] = self.transform_plot(type, logger_ini['Plot'])
        output_ini["Save"] = self.transform_save(type,logger_ini['Save'])

        return output_ini


    def transform_kpis(self, type="lvl3", old_kpi_ini_dict={}):
        """
        transforms the kpis input

        :param type:
        :param old_kpi_ini_dict:
        :return:
        """
        new_kpi_ini_dict={}
        if type == "lvl2":
            return old_kpi_ini_dict
        elif type == "lvl1":
            return old_kpi_ini_dict
        elif type == "lvl3":
            new_kpi_ini_dict["time_interval"]=old_kpi_ini_dict["time_interval"]
            new_kpi_ini_dict["log_events"]=old_kpi_ini_dict["log_events"]
            if(old_kpi_ini_dict["log_summary"]):
                new_kpi_ini_dict["log_summary"]=[element.value for element in Logger_Enum]
            else:
                new_kpi_ini_dict["log_summary"]=[]

            if(old_kpi_ini_dict["log_time"]):
                new_kpi_ini_dict["log_time"] =[element.value for element in Logger_Enum]
            else:
                new_kpi_ini_dict["log_time"] = []
            return new_kpi_ini_dict

    def transform_config_ini(self, type="lvl3", old_config_ini_dict={}):
        """
        transforms the cofing input

        :param type:
        :param old_config_ini_dict:
        :return:
        """

        if type == "lvl2":
            return old_config_ini_dict
        elif type == "lvl1":
            return old_config_ini_dict
        elif type == "lvl3":
            return old_config_ini_dict


    def transform_plot(self, type="lvl3", old_plot_ini_dict={}):
        """
        transforms the plot input

        :param type:
        :param old_plot_ini_dict:
        :return:
        """

        if type == "lvl2":
            return old_plot_ini_dict
        elif type == "lvl1":
            return old_plot_ini_dict
        elif type == "lvl3":
            return old_plot_ini_dict

    def transform_save(self, type="lvl3", old_plot_ini_dict={}):
        """
        transforms the kpis input

        :param type:
        :param old_plot_ini_dict:
        :return:
        """

        if type == "lvl2":
            return old_plot_ini_dict
        elif type == "lvl1":
            return old_plot_ini_dict
        elif type == "lvl3":
            return old_plot_ini_dict