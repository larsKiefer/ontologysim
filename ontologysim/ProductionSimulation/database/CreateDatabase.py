import ast
import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_parent_dir = os.path.dirname(parent_dir)
parent_parent_parent_dir = os.path.dirname(parent_parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0,parent_parent_dir)
sys.path.insert(0,parent_parent_parent_dir)


from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest

from ontologysim.ProductionSimulation.database.DataBase import DataBase
from ontologysim.ProductionSimulation.database.models.Base import Base
#dont remove
from ontologysim.ProductionSimulation.database.models.User import *
from ontologysim.ProductionSimulation.database.models.SimulationFacts import *
from ontologysim.ProductionSimulation.database.models.SimulationRun import *
from ontologysim.ProductionSimulation.database.models.TransporterKPI import *
from ontologysim.ProductionSimulation.database.models.SimulationKPI import *
from ontologysim.ProductionSimulation.database.models.ProductKPI import *
from ontologysim.ProductionSimulation.database.models.QueueKPI import *
from ontologysim.ProductionSimulation.database.models.TransporterLocation import *
from ontologysim.ProductionSimulation.database.models.TransporterDistribution import *

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


