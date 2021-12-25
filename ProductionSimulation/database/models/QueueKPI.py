from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class QueueKPI(Base):
    __tablename__ = 'QueueKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    FillLevel = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class QueueTimeKPIValue(Base):
    __tablename__ = 'QueueTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    FillLevel = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    queueTimeKPIID = Column(Integer, ForeignKey("QueueTimeKPI.id"),nullable=True)


class QueueTimeKPI(Base):
    __tablename__ = 'QueueTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    queueTimeKPIValue = relationship(QueueTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)