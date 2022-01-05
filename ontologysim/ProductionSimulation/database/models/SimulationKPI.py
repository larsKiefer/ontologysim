from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ontologysim.ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class SimulationKPI(Base):
    __tablename__ = 'SimulationKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    WIP = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    logging_time = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AR = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    PR = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class SimulationTimeKPIValue(Base):
    __tablename__ = 'SimulationTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    WIP = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    logging_time = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AR = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    PR = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    simulationTimeKPIID = Column(Integer, ForeignKey("SimulationTimeKPI.id"),nullable=True)


class SimulationTimeKPI(Base):
    __tablename__ = 'SimulationTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    simulationTimeKPIValue = relationship(SimulationTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)