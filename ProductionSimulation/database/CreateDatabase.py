import ast
import inspect
import json
import os
import sys

from ProductionSimulation.utilities.path_utilities import PathTest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.dirname(parent_dir))



from ProductionSimulation.database.DataBase import DataBase
from ProductionSimulation.database.models.Base import Base
#dont remove
from ProductionSimulation.database.models.User import *
from ProductionSimulation.database.models.SimulationFacts import *
from ProductionSimulation.database.models.SimulationRun import *
from ProductionSimulation.database.models.MachineKPI import *
from ProductionSimulation.database.models.TransporterKPI import *
from ProductionSimulation.database.models.SimulationKPI import *
from ProductionSimulation.database.models.ProductKPI import *
from ProductionSimulation.database.models.QueueKPI import *
from ProductionSimulation.database.models.TransporterLocation import *
from ProductionSimulation.database.models.TransporterDistribution import *

"""
Method for loading database

"""

PathTest.current_main_dir = current_dir

dbPath = "sqlite:///ontologysim/ProductionSimulation/database/SimulationRun.db"


db = DataBase(dbPath)

Base.metadata.create_all(db.db_engine)

defaultUserPath = PathTest.check_file_path("/ontologysim/ProductionSimulation/database/defaultUser.json")
with open(defaultUserPath,"r") as f:
    userJSON=ast.literal_eval(f.read())

print(userJSON)
print(userJSON["userName"])

user = db.session.query(User).filter_by(userName=userJSON["userName"]).first()
if not user:
   user = User(**userJSON)
   db.session.add(user)
   db.session.commit()


