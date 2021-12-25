from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from ProductionSimulation.database.models.Base import Base
from ProductionSimulation.database.models.MachineKPI import MachineKPI, MachineTimeKPI
from ProductionSimulation.database.models.ProductKPI import ProductKPI, AllProducts, ProductTimeKPI
from ProductionSimulation.database.models.QueueKPI import QueueKPI, QueueTimeKPI
from ProductionSimulation.database.models.SimulationKPI import SimulationTimeKPI, SimulationKPI
from ProductionSimulation.database.models.TransporterDistribution import TransporterDistributionKPI, \
    TransporterDistributionTimeKPI
from ProductionSimulation.database.models.TransporterKPI import TransporterTimeKPI, TransporterKPI
from ProductionSimulation.database.models.TransporterLocation import TransporterLocationKPI, TransporterLocationTimeKPI


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



