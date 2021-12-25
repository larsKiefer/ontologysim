import inspect
import json
import os
import sys

from Flask.Actions.APIAction import APIAction
from ProductionSimulation.database.DataBase import DataBase


class ConnectDataBaseAction(APIAction):
    """

    /database/connect: get: connect to sqllite data base
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        self.flaskApp.db = DataBase("sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db")

        response = self.response200OK(json.dumps({"message":"OK"}))

        return response


