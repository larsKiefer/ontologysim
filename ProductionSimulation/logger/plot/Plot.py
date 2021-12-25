import math
from random import random

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from ProductionSimulation.utilities import init_utilities
from ProductionSimulation.utilities.path_utilities import PathTest


class Plot:
    """
    file for plotting kpis during simulation run
    """

    def __init__(self, logger):
        """

        :param logger:
        """

        self.logger = logger
        self.plot_activated = False
        self.setting_dict = {}
        self.number_of_points_x = 0
        self.last_time_index = 0
        self.time_intervall = 1
        self.start_logging_multiple = 0

        self.time_kpis = []
        self.number_kpis = []
        self.percentage_kpis = []

        self.y_lookup_tabel = "/ProductionSimulation/logger/plot/y_lookup_tabel.ini"

    def initPlot(self, plot_config):
        """
        init plot and create figure

        :param plot_config: log dict
        :return:
        """

        try:

            self.plot_activated = plot_config['Plot']['plot']
        except:
            print("waring add [Plot]")

        if self.plot_activated:
            self.setting_dict = plot_config['Plot']['data']
            self.number_of_points_x = plot_config['Plot']['number_of_points_x']
        else:
            return

        axis_config_path = PathTest.check_file_path(self.y_lookup_tabel)

        # Read from Configuration File
        axis_conf = init_utilities.Init(axis_config_path)
        axis_conf.read_ini_file()


        number_kpis = axis_conf.configs['LookUp']['number']
        time_kpis = axis_conf.configs['LookUp']['time']
        self.number_time_kpis = number_kpis + time_kpis

        self.percentage_kpis = axis_conf.configs['LookUp']['percentage']

        self.logger_data = []

        number_time_axis = None
        percentage_axis = None
        number_of_axis = 0

        plt.ion()
        matplotlib.use('TkAgg')
        self.fig = plt.figure(figsize=(5, 4), dpi=100)
        self.fig.suptitle('KPI plot', fontsize=16)

        if len(self.setting_dict)>3:
            raise Exception("to many plot data added")

        for setting in self.setting_dict:

            if setting["type"] == "machine":
                sub_logger=self.logger.machineLogger
            elif setting["type"] == "transporter":
                sub_logger=self.logger.transporterLogger
            elif setting["type"] == "product":
                sub_logger= self.logger.productAnalyseLogger
            elif setting["type"]=="queue":
                sub_logger= self.logger.queueFillLevelLogger
            elif setting["type"]=="transporter_distribution":
                sub_logger = self.logger.transporterDistributionLogger
            elif setting["type"] == "simulation":
                sub_logger = self.logger.simLogger
            else:
                raise Exception(setting["type"]+" not defiened")

            self.logger_data.append(
                {'sub_logger': sub_logger, 'type': setting["type"], 'x': [0], 'y': [0], 'y_type': "",
                 'object_name': setting['object_name'], 'kpi': setting['kpi'], 'axis': None, 'line': ''})

            if not setting['kpi'] in self.logger_data[-1]['sub_logger'].kpi_list and not setting['kpi'] in \
                                                                                         self.logger_data[-1][
                                                                                             'sub_logger'].basic_kpi_list:
                raise Exception("kpi not found " + str(setting['object_name']) + " " + str(setting['kpi']) + " " + str(
                    setting['type']))

            if not setting['object_name'] in list(self.logger_data[-1]['sub_logger'].time_kpis.keys()):
                raise Exception("kpi not found " + str(setting['object_name']) + " " + str(setting['kpi']) + " " + str(
                    setting['type']))



            if setting['kpi'] in self.number_time_kpis:
                if number_time_axis == None and number_of_axis == 0:
                    number_time_axis = self.fig.add_subplot(111)
                    number_time_axis.grid()
                elif number_time_axis == None:
                    number_time_axis = percentage_axis.twinx()
                self.logger_data[-1]['axis'] = number_time_axis
                self.logger_data[-1]['y_type'] = "time"

            elif setting['kpi'] in self.percentage_kpis:

                if percentage_axis == None and number_of_axis == 0:
                    percentage_axis = self.fig.add_subplot(111)
                    percentage_axis.grid()

                elif percentage_axis == None:
                    percentage_axis = number_time_axis.twinx()
                self.logger_data[-1]['axis'] = percentage_axis
                self.logger_data[-1]['y_type'] = "percentage"

            else:
                raise Exception(setting['kpi'] + " not defined in y_lookup_tabel.ini")
            number_of_axis += 1


    def startPlot(self,time):
        """
        start plotting

        :param time: int: currently not used
        :return:
        """
        if not self.plot_activated:
            return

        color_list = ['r', 'b', 'g','c','m','y']
        i = 0
        for logger_dict in self.logger_data:


            logger_dict['x'][0]=logger_dict['sub_logger'].start_logging_multiple*logger_dict['sub_logger'].logger.time_intervall
            logger_dict['line'], = logger_dict['axis'].plot([], [], color_list[i], lw=3,
                                                            label=logger_dict['type'] + "_" + logger_dict[
                                                                'object_name'] + "_" + logger_dict['kpi'])
            logger_dict['axis'].legend(loc=i)
            i += 1

        self.fig.canvas.draw()

    def update_plot(self, time):
        """
        update plot

        :param time: double
        :return:
        """
        if self.logger.plot.plot_activated and self.logger.start_logging and self.last_time_index < math.floor(
                time / self.time_intervall) - self.start_logging_multiple - 1:
            for logger_dict in self.logger_data:

                self.update_figure_with_new_value(logger_dict, logger_dict['x'][-1] + 1*logger_dict['sub_logger'].logger.time_intervall,
                                                  logger_dict['sub_logger'].time_kpis[logger_dict['object_name']][
                                                      logger_dict['kpi']][-2])

            self.view_update()
            self.last_time_index = math.floor(time / self.time_intervall) - self.start_logging_multiple

    def update_figure_with_new_value(self, logger_dict, xval, yval):
        """
        sub method for updating plot with new data

        :param logger_dict:
        :param xval:
        :param yval:
        :return:
        """

        logger_dict['x'].append(xval)
        logger_dict['y'].append(yval)

        if len(logger_dict['x']) > self.number_of_points_x:
            logger_dict['x'].pop(0)
        if len(logger_dict['y']) > self.number_of_points_x:
            logger_dict['y'].pop(0)

        logger_dict['line'].set_data(logger_dict['x'], logger_dict['y'])

        logger_dict['axis'].relim()
        logger_dict['axis'].autoscale_view()

    def view_update(self):
        """
        update fig
        :return:
        """
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

