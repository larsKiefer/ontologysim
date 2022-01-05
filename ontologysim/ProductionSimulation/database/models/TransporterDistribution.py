from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ontologysim.ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class TransporterDistributionKPI(Base):
    __tablename__ = 'TransporterDistributionKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    fromToLocation = Column(String,nullable=False)
    value = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class TransporterDistributionTimeKPIValue(Base):
    __tablename__ = 'TransporterDistributionKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    fromToLocation = Column(String, nullable=False)
    value = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    transporterDistributionKPIID = Column(Integer, ForeignKey("TransporterDistributionTimeKPI.id"),nullable=True)


class TransporterDistributionTimeKPI(Base):
    __tablename__ = 'TransporterDistributionTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    transporterDistributionTimeKPIValue = relationship(TransporterDistributionTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)