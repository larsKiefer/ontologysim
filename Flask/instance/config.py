# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os



class Config(object):

    # Set up the App SECRET_KEY
    SECRET_KEY = 'S#perS3crEt_007'

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ProductionSimulation/database/SimulationRun.db'


class ProductionConfig(Config):
    DEBUG = False
    DATABASE = False

class ProductionDataBaseConfig(Config):
    DEBUG = False
    DATABASE = True

class DebugConfig(Config):
    DEBUG = True
    DATABASE = False

class DebugConfigDataBase(Config):
    DEBUG = True
    DATABASE = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'ProductionDataBase': ProductionDataBaseConfig,
    'Debug': DebugConfig,
    'DebugDataBase': DebugConfigDataBase
}
