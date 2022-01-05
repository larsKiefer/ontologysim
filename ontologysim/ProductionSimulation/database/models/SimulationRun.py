from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from ontologysim.ProductionSimulation.database.models.Base import Base
from ontologysim.ProductionSimulation.database.models.MachineKPI import MachineKPI, MachineTimeKPI
from ontologysim.ProductionSimulation.database.models.ProductKPI import ProductKPI, AllProducts, ProductTimeKPI
from ontologysim.ProductionSimulation.database.models.QueueKPI import QueueKPI, QueueTimeKPI
from ontologysim.ProductionSimulation.database.models.SimulationKPI import SimulationTimeKPI, SimulationKPI
from ontologysim.ProductionSimulation.database.models.TransporterDistribution import TransporterDistributionKPI, \
    TransporterDistributionTimeKPI
from ontologysim.ProductionSimulation.database.models.TransporterKPI import TransporterTimeKPI, TransporterKPI
from ontologysim.ProductionSimulation.database.models.TransporterLocation import TransporterLocationKPI, TransporterLocationTimeKPI


class SimulationRun(Base):
    __tablename__ = 'SimulationRun'
    id = Column(Integer, primary_key=True)
    start = Column(DateTime, nullable=False)
    simulationFacts = relationship("SimulationFacts",backref=backref("SimulationRun",uselist=False))
    simulationFactsID = Column(Integer,ForeignKey("SimulationFacts.id"),nullable=True)
    machineKPI = relationship(MachineKPI)
    machineTimeKPI = relationship(MachineTimeKPI)
    transporterKPI = relationship(TransporterKPI)
    transporterTimeKPI = relationship(TransporterTimeKPI)
    simulationTimeKPI = relationship(SimulationTimeKPI)
    simulationKPI = relationship(SimulationKPI)
    queueKPI = relationship(QueueKPI)
    queueTimeKPI = relationship(QueueTimeKPI)
    productKPI = relationship(ProductKPI)
    productTimeKPI = relationship(ProductTimeKPI)
    allProducts = relationship(AllProducts)
    transporterDistributionKPI = relationship(TransporterDistributionKPI)
    transporterDistributionTimeKPI = relationship(TransporterDistributionTimeKPI)
    transporterLocationKPI = relationship(TransporterLocationKPI)
    transporterLocationTimeKPI = relationship(TransporterLocationTimeKPI)
    userID = Column(Integer, ForeignKey('User.id'), nullable=True)
    user = relationship("User", back_populates="simulationRuns")



