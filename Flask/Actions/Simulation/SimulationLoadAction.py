from flask import json, request

from Flask.Actions.APIAction import APIAction
from ProductionSimulation.init.API.IntitializerProducttypeAPI import InitializerProducttypeAPI

import os
from os import listdir
from os.path import isfile, join

from ProductionSimulation.utilities.path_utilities import PathTest


class SimulationLoadAction(APIAction):
    """
    parent class for simulation load, define default path
    """

    def __init__(self,action, flaskApp):
        """

        :param action:
        :param flaskApp:
        """
        super().__init__(action, flaskApp)
        self.path="/ontologysim/Flask/Assets/DefaultFiles"

        self.fullPath = PathTest.check_dir_path_current_dir_given(self.path,os.path.dirname(__file__))

class FileLoadAction(SimulationLoadAction):
    """
    get: /load_files: return all file names from default directory
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        onlyfiles = [f for f in listdir(self.fullPath) if isfile(join(self.fullPath, f))]

        self.response=self.response200OK(json.dumps({"files":onlyfiles}))

        return self.response

