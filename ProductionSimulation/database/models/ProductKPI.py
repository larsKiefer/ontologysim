from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, Float, TypeDecorator
from sqlalchemy.orm import relationship, backref

from ProductionSimulation.database.models.Base import Base
from sqlalchemy.ext.declarative import declarative_base

class ProductKPI(Base):
    __tablename__ = 'ProductKPI'
    id = Column(Integer, primary_key=True)
    ProductType = Column(String)
    WIP = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    ATTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AQMTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    APTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUPTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTnpp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    PBTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AOET = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    TR = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    NrP = Column(Integer, nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)

class AllProducts(Base):

    __tablename__ = 'AllProducts'
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    ProductType = Column(String)
    ATTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    TTRp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AQMTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    APTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUPTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTnpp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    PBTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AOET = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    start_time = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    end_time = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)

class ProductTimeKPIValue(Base):
    __tablename__ = 'ProductTimeKPIValue'
    id = Column(Integer, primary_key=True)
    time = Column(Float(decimal_return_scale=7,asdecimal=True), nullable=True)
    WIP = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    ATTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AQMTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    APTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUPTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AUSTnpp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    PBTp = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    AOET = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    TR = Column(Float(decimal_return_scale=7, asdecimal=True), nullable=True)
    NrP = Column(Integer, nullable=True)
    productTimeKPIID = Column(Integer, ForeignKey("ProductTimeKPI.id"),nullable=True)


class ProductTimeKPI(Base):
    __tablename__ = 'ProductTimeKPI'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    productTimeKPIValue = relationship(ProductTimeKPIValue)
    simulationRunID = Column(Integer, ForeignKey("SimulationRun.id"), nullable=True)