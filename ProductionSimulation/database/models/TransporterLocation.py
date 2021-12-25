from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class TransporterLocationKPI(Base):
    __tablename__ = 'TransporterLocationKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    location = Column(String,nullable=False)
    value = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class TransporterLocationTimeKPIValue(Base):
    __tablename__ = 'TransporterLocationTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    location = Column(String, nullable=False)
    value = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    transporterLocationKPIID = Column(Integer, ForeignKey("TransporterLocationTimeKPI.id"),nullable=True)


class TransporterLocationTimeKPI(Base):
    __tablename__ = 'TransporterLocationTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    transporterLocationTimeKPIValue = relationship(TransporterLocationTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)