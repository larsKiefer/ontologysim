

from distutils.util import strtobool

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.Flask.Actions.UtilMethods.StateStorage import StateStorage
from ontologysim.ProductionSimulation.init.Initializer import Initializer
from ontologysim.ProductionSimulation.sim.Enum import Label


class ResetBEAction(APIAction):
    """
    get: /reset_be: destroy onto & reinit simcore
    """

    def __call__(self, *args):
        self.action()


        try:
            self.flaskApp.init.s.destroyOnto()
        except:
            print("onto not defined")

        self.flaskApp.init.initSimCore()
        self.flaskApp.startAlready=False

        self.response = self.response200OK(json.dumps({"alreadyStarted": False,
                                                               "run": False, "production": {}}))

        return self.response