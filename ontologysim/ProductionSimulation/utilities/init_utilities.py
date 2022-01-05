import configparser
import ast
import logging
from enum import Enum


class Init(object):
    """
    transforms the ini into a dict
    """
    def __init__(self, filepath, time=0):
        """


        :param filepath:
        :param time: currently not used
        """
        self.time = time
        self.config = configparser.ConfigParser()
        if(filepath!=""):
            self.config.read(filepath)
        self.configs = dict()

        self.productionKeys = ['Type', 'Machine', 'ProductType', 'Process', 'Transporter', 'RandomSeed']
        self.owlKeys = ['OWL']
        self.controllerKeys = ['Controller']
        self.loggerKeys = ['Type', 'KPIs', 'ConfigIni', 'Plot']
        self.type = []
        # print("ini read")

    def read_ini_file(self):
        """
        transforms an ini file to a dict, which is saved in the variable configs
        """

        for sec in self.config.sections():

            self.configs[sec] = dict()
            for opt in self.config.options(sec):
                try:
                    helper = int(self.config[sec][opt])
                except ValueError:
                    try:
                        helper = float(self.config[sec][opt])
                    except ValueError:
                        try:
                            helper = ast.literal_eval(self.config[sec][opt])
                        except ValueError:
                            helper = str(self.config[sec][opt])
                        except SyntaxError:
                            logging.error(
                                'error while reading ' + str(sec) + " " + str(opt) + " " + str(self.config[sec][opt]))
                            helper = str(self.config[sec][opt])
                self.configs[sec][opt] = helper

    def identifyType(self):
        """
        identify type for given path, set type variable
        :return:
        """
        self.productionPossible = True
        self.owlPossible = True
        self.controllerPossible = True
        self.loggerPossible = True

        for key in self.productionKeys:
            if self.productionPossible:
                if key not in list(self.configs.keys()):
                    self.productionPossible = False
                    break

        for key in self.owlKeys:
            if self.owlPossible:
                if key not in list(self.configs.keys()):
                    self.owlPossible = False
                    break

        for key in self.controllerKeys:
            if self.controllerPossible:
                if key not in list(self.configs.keys()):
                    self.controllerPossible = False
                    break

        for key in self.loggerKeys:
            if self.loggerPossible:
                if key not in list(self.configs.keys()):
                    self.loggerPossible = False
                    break

        if not(self.loggerPossible or self.controllerPossible or self.owlPossible or self.productionPossible):
            self.type=[]
            return

        self.type=[]
        if self.productionPossible:
            self.type.append("production")
        elif self.loggerPossible:
            self.type.append("logger")
        elif self.owlPossible:
            self.type.append("owl")
        elif self.controllerPossible:
            self.type.append("controller")


class IniString(Init):

    def __init__(self, textString, time=0):
        """
        :param filepath:
        :param time: currently not used
        """
        super().__init__(filepath="",time=time)
        self.config = configparser.ConfigParser()
        self.config.read_string(textString)
        self.configs = dict()

class IniDict(Init):
    """
    read dict and transform into configparser
    """

    def __init__(self, dictInformation, time=0):
        """
        :param filepath:
        :param time: currently not used
        """
        super().__init__(filepath="",time=time)
        self.config = configparser.ConfigParser()
        self.config.read_dict(dictInformation)
        self.configs = dict()










