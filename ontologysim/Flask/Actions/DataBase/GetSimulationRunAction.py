import inspect
import json
import os
import sys

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.database.models.SimulationRun import SimulationRun
from ontologysim.ProductionSimulation.database.models.User import User


class GetSimulationRunAction(APIAction):
    """

    /database/simulationrun: /get: get all elements of simulationRun table
    """
    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()


        simulation_list = []

        session=self.flaskApp.db.createSession(self.flaskApp.db.db_engine)

        #for row in self.flaskApp.db.db_engine.execute("SELECT * FROM SimulationRun"):
        #    print(row)



        for simulation_run in session.query(SimulationRun).all():

            simulation_dict = {}
            simulation_dict["id"] = simulation_run.id
            simulation_dict["start"] = str(simulation_run.start)
            #print(simulation_dict)
            simulation_list.append(simulation_dict)        

        self.response = self.response200OK(json.dumps({"result": simulation_list}))
        return self.response