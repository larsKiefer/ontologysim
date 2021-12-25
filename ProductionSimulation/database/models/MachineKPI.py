from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base


class MachineKPI(Base):
    __tablename__ = 'MachineKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=True)
    TTFp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    TTRp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    FE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    CMTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUITp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUBTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    ADOTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    APTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUPTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUSTTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    PBTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AUBLTp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    PRIp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    A = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    AE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    TE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    UE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    SeRp = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    E = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    OEE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    NEE = Column(Float(decimal_return_scale=7,asdecimal=True),nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"),nullable=True)

class MachineTimeKPIValue(Base):
    __tablename__ = 'MachineTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    TTFp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    TTRp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    FE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    CMTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUITp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUBTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    ADOTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    APTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUPTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUSTTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    PBTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AUBLTp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    PRIp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    A = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    AE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    TE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    UE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    SeRp = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    E = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    OEE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    NEE = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    machineTimeKPIID = Column(Integer, ForeignKey("MachineTimeKPI.id"),nullable=True)


class MachineTimeKPI(Base):
    __tablename__ = 'MachineTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    machineTimeKPIValue = relationship(MachineTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)