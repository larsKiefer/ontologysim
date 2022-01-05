import csv
import datetime
import os

from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest


class TimeAnalyse:
    """
    serves to make runtime analyses in order to reduce the computing time
    """
    time_dict={}
    time_current_dict={}
    @staticmethod
    def time_analyse(info_string,is_start):
        """
        all times with the same string are enumerated The time between start and end is always stopped
        :param info_string: must be unique
        :param is_start: true=start time, false=end time
        """
        if is_start:
            TimeAnalyse.time_current_dict[info_string]=datetime.datetime.now()
        else:
            TimeAnalyse.time_current_dict[info_string] = datetime.datetime.now() - TimeAnalyse.time_current_dict[
                info_string]
            if info_string in TimeAnalyse.time_dict.keys():
                TimeAnalyse.time_dict[info_string]+=TimeAnalyse.time_current_dict[info_string]
            else:
                TimeAnalyse.time_dict[info_string]=TimeAnalyse.time_current_dict[info_string]
            TimeAnalyse.time_current_dict[info_string]=0

    @staticmethod
    def save_dict_to_csv():
        """
        saves the time_dict to an csv, the path is predefined
        """
        path="/ontologysim/example/analyse/time_analyse.csv"
        path=PathTest.check_dir_path(path)

        with open(path, "w", newline='') as order_logger:
            wr = csv.writer(order_logger, delimiter=';', quotechar=' ', quoting=csv.QUOTE_ALL)
            wr.writerow([key for key in TimeAnalyse.time_dict.keys()])
            wr.writerow([str(v) for k,v in TimeAnalyse.time_dict.items()])
