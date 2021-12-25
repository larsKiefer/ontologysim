import datetime
import math
import random
import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
parent_parent_parent_dir = os.path.dirname(parent_parent_dir)
sys.path.insert(0,current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, parent_parent_dir)
sys.path.insert(0, parent_parent_parent_dir)

from ProductionSimulation.database.DataBase import DataBase
from ProductionSimulation.database.models import SimulationRun,Base
from pytz import timezone

class DataSeeder(object):
    """
    data seeder, only an test area for data seeding
    """

    def __init__(self):
        """

        """
        self.db = DataBase("sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db")
        Base.metadata.create_all(self.db.db_engine)

    def addSimulationRun(self):
        """
        create simulation run
        :return:
        """
        UTC = timezone('UTC')
        for i in range(10):
            simulationRun = SimulationRun(start=datetime.datetime.now(UTC))
            self.db.session.add(simulationRun)

        self.db.session.commit()



    def dropAllData(self):
        """
        drop simulation run
        :return:
        """

        self.db.session.execute("DELETE FROM SimulationRun")



dataSeeder = DataSeeder()

#dataSeeder.addSimulationRun()
#print(dataSeeder.db.session.query(SimulationRun).all())
#dataSeeder.dropAllData()

print(dataSeeder.db.session.query(SimulationRun).all())