from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class TransporterKPI(Base):
    __tablename__ = 'TransporterKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    TTFp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    TTRp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    FE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    CMTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUITp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    ADOTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUTTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class TransporterTimeKPIValue(Base):
    __tablename__ = 'TransporterTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    TTFp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    TTRp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    FE = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    CMTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUITp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    ADOTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUTTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    transporterTimeKPIID = Column(Integer, ForeignKey("TransporterTimeKPI.id"),nullable=True)


class TransporterTimeKPI(Base):
    __tablename__ = 'TransporterTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    transporterTimeKPIValue = relationship(TransporterTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)