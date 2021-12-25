import logging

from owlready2 import *

from ProductionSimulation.analyse.TimeAnalyse import TimeAnalyse
from ProductionSimulation.sim.Enum import Label, Transporter_Enum, Machine_Enum
from ProductionSimulation.sim.Machine import Machine
import time
import math


class Event:
    """
    manages and creates event in ontology
    """

    def __init__(self, simCore):
        """

        :param simCore:
        """
        self.simCore = simCore

        self.number_logger = 0
        self.csv_writer_type = 'w'

        self.property_dict = {}
        self.property_dict_logger = {}
        self.event_storage = []

        self.number_of_events_in_logger = 2000
        self.first_run = True

    def createEvent(self, time, type, time_diff):
        """
        creates an event in onto

        :param time: double
        :param type: str
        :param time_diff: double
        :return: onto
        """
        if len(self.event_storage) == 0:

            eventInstance = self.simCore.central.event_class(Label.Event.value + str(self.simCore.event_id))

            self.simCore.event_id += 1
        elif self.simCore.run_as_api:

            eventName = self.event_storage.pop(0)

            eventInstance = self.simCore.onto[eventName]
            if(eventInstance==None):
                eventInstance = self.simCore.central.event_class(Label.Event.value + str(self.simCore.event_id))

            else:
                try:
                    self.simCore.onto[eventName].name = Label.Event.value + str(self.simCore.event_id)
                except:
                    pass

            self.simCore.event_id += 1
        else:
            eventInstance = self.simCore.onto[self.event_storage.pop(0)]
            beforeValue = ""
            try:

                beforeValue = str(eventInstance)+ " " + str(self.simCore.onto[Label.Event.value + str(self.simCore.event_id)])
                eventInstance.name = Label.Event.value + str(self.simCore.event_id)

            except:
                logging.error(str([event for event in self.simCore.onto[Label.EventList.value + "0"].has_for_event]))
                logging.error("beforeValue "+str(beforeValue))
                logging.error(Label.Event.value + str(self.simCore.event_id))
                raise Exception
            self.simCore.event_id += 1

        eventInstance.additional_type=""

        eventInstance.time = time

        eventInstance.type = type.value
        eventInstance.time_diff = time_diff

        self.simCore.onto[Label.EventList.value + "0"].has_for_event.append(eventInstance)

        #print(self.simCore.onto[Label.EventList.value + "0"].has_for_event)
        return eventInstance

    #TODO save store event
    def store_event(self, event_onto):
        """
        resets all values of an event, does not delete the event

        :param event_onto: onto
        """
        eventList=["e16","e13","e15","e23","e43","e45","e46","e47"]


        if event_onto.type in self.property_dict.keys():
            for prop_name in self.property_dict[event_onto.type]:
                self.removeProperties_Event(prop_name, event_onto)

        else:

            properties = event_onto.get_properties()
            self.property_dict[event_onto.type] = []
            for prop in properties:
                prop_name = prop.name
                self.property_dict[event_onto.type].append(prop_name)
                self.removeProperties_Event(prop_name, event_onto)





        #event_onto.time= 0
        #event_onto.time_diff = -1
        #event_onto.type = ""
        event_onto.additional_type = ""

        self.event_storage.append(event_onto.name)



        #print("store event",event_onto.name)

    def getNextEvent(self):
        """
        calculates next event

        :return:
        """
        event_list = self.simCore.onto[Label.EventList.value + "0"].has_for_event

        # short version
        #event = [[event, event.time] for event in event_list if event.time >= self.simCore.getCurrentTimestep()]
        #event.sort(key=lambda x: x[1])

        time = self.simCore.getCurrentTimestep()
        next_event = None
        next_time = math.inf
        for event in event_list:
            if event.time >= time and event.time<next_time:

                next_time = event.time
                next_event = event
            elif event.time==next_time:
                if int(event.name[1:])<int(next_event.name[1:]):
                    next_time = event.time
                    next_event = event


        #print(next_event.time,next_event.type)
        if next_event != None:
            return next_event, next_event.type
        else:
            return None, None

    def getNumberOfEvents(self):
        """
        returns the number of events, which have a time > current time

        :return: int
        """
        event_list = self.simCore.onto[Label.EventList.value + "0"].has_for_event
        number_of_events = len([event.time for event in event_list if event.time >= self.simCore.getCurrentTimestep()])
        return number_of_events

    def add_product_to_event(self, event_onto, product_onto):
        """
        adding a product onto to event

        :param event_onto:
        :param product_onto:
        """
        event_onto.has_for_product_event.append(product_onto)

    def add_transport_to_event(self, event_onto, transport_onto):
        """
        adding transport onto to event

        :param event_onto:
        :param transport_onto:
        """
        event_onto.has_for_transport_event.append(transport_onto)

    def add_machine_to_event(self, event_onto, machine_onto):
        """
        add machine onto to event

        :param event_onto:
        :param machine_onto:
        """
        event_onto.has_for_machine_event.append(machine_onto)

    def add_process_to_event(self, event_onto, prod_process_onto):
        """
        add process onto to event

        :param event_onto:
        :param prod_process_onto:
        """
        event_onto.has_for_process_event.append(prod_process_onto)

    def add_position_to_event(self, event_onto, position_onto):
        """
        adding position onto to event

        :param event_onto:
        :param position_onto:
        """
        event_onto.has_for_position_event.append(position_onto)

    def add_location_to_event(self, event_onto, location_onto):
        """
        adding a location onto to event

        :param event_onto:
        :param location_onto:
        """
        event_onto.has_for_location_event.append(location_onto)

    def add_task_to_event(self, event_onto, task_onto):
        """
        adding a task onto to event

        :param event_onto:
        :param task_onto:
        """
        event_onto.has_for_task_event.append(task_onto)

    def add_service_to_event(self, event_onto, service_onto):
        """
        add service to event

        :param event_onto:
        :param service_onto:
        """
        event_onto.has_for_service_event.append(service_onto)

    def add_to_short_term_logger(self, event_onto, position_onto):
        """
        adding an event to a short term logger and removes another event if the position is already registered add the logger

        :param event_onto:
        :param position_onto:
        """
        self.simCore.onto[Label.ShortTermLogger.value + "0"].has_for_event_short_term_logger.append(event_onto)
        #event_list_of_position = [event for event in position_onto.is_position_event_of if self.simCore.onto[
         # Label.ShortTermLogger.value + "0"] in event.is_event_short_term_logger_of]
        number_of_events=0
        event_list=position_onto.is_position_event_of

        for event_onto in event_list:
            if self.simCore.onto[Label.ShortTermLogger.value + "0"] in event_onto.is_event_short_term_logger_of:
                number_of_events+=1
            if number_of_events>=2:

                break

        if number_of_events>=2:
            if event_list[0].time>event_list[1].time:
                event_onto = event_list[1]
            else:
                event_onto=event_list[0]
            position_onto.is_position_event_of.remove(event_onto)
            self.simCore.onto[Label.ShortTermLogger.value + "0"].has_for_event_short_term_logger.remove(event_onto)
            self.store_event(event_onto)



    def delete_event(self, event_onto):
        """
        destroy an event onto

        :param event_onto:
        """
        destroy_entity(event_onto)

    def add_to_logger(self, event_onto):
        """
        adds a event_onto to a logger, transforms event onto to event_logger onto
        when the logger holds more than 2000 values, then the values are saved in a csv or database

        :param event_onto:
        """
        if "csv" in self.simCore.event_logger.type or "database" in self.simCore.event_logger.type:
            event_label = event_onto.name
            logger_event_label = Label.LoggerEvent.value + event_label.replace(Label.Event.value, "")
            if self.first_run == True:
                eventInstance = self.simCore.central.event_of_logger_class(logger_event_label)
                self.simCore.onto[Label.Logger.value + "1"].has_for_event_of_logger.append(eventInstance)
            else:
                eventInstance = self.simCore.onto[Label.Logger.value + "1"].has_for_event_of_logger[self.number_logger]

            old_event_instance_type = eventInstance.type_logger
            eventInstance.time_logger = event_onto.time
            eventInstance.time_diff_logger = event_onto.time_diff
            eventInstance.type_logger = event_onto.type
            eventInstance.additional_type_logger = event_onto.additional_type
            if self.first_run == False:
                if old_event_instance_type in self.property_dict_logger.keys():
                    for prop_name in self.property_dict_logger[old_event_instance_type]:
                        self.removeProperties_EventLogger(prop_name, eventInstance)

                else:
                    properties = event_onto.get_properties()
                    self.property_dict_logger[old_event_instance_type] = []
                    for prop in properties:
                        prop_name = prop.name
                        self.property_dict_logger[old_event_instance_type].append(prop_name)
                        self.removeProperties_EventLogger(prop_name, eventInstance)

            if event_onto.type in self.property_dict.keys():
                for prop_name in self.property_dict[event_onto.type]:
                    self.swapProperties_EventLogger(prop_name, eventInstance, event_onto)
            else:
                properties = event_onto.get_properties()
                self.property_dict[event_onto.type] = []
                for prop in properties:
                    prop_name = prop.name
                    self.property_dict[event_onto.type].append(prop_name)
                    self.swapProperties_EventLogger(prop_name, eventInstance, event_onto)

            self.number_logger += 1
            if self.number_logger > self.number_of_events_in_logger:
                # print("delete logger events")
                if "database" in self.simCore.event_logger.type and self.simCore.event_logger.is_activated:
                    self.simCore.event_logger.insertData()
                if "csv" in self.simCore.event_logger.type and self.simCore.event_logger.is_activated:
                    self.simCore.event_logger.save_to_csv(self.csv_writer_type)
                    self.csv_writer_type = 'a'

                self.first_run = False
                self.number_logger = 0

    def swapProperties_EventLogger(self, prop_name, eventInstance, event_onto):
        """
        transforming all connection of the event onto to a event_logger

        :param prop_name: str
        :param eventInstance: event_logger
        :param event_onto: event_instance
        """
        if prop_name == "has_for_machine_event":
            for machine in event_onto.has_for_machine_event:
                eventInstance.has_for_machine_event_of_logger.append(machine)
        elif prop_name == "has_for_position_event":
            for position in event_onto.has_for_position_event:
                eventInstance.has_for_position_event_of_logger.append(position)
        elif prop_name == "has_for_location_event":
            for location in event_onto.has_for_location_event:
                eventInstance.has_for_location_event_of_logger.append(location)
        elif prop_name == "has_for_transport_event":
            for transport in event_onto.has_for_transport_event:
                eventInstance.has_for_transport_event_of_logger.append(transport)
        elif prop_name == "has_for_product_event":
            for product in event_onto.has_for_product_event:
                eventInstance.has_for_product_event_of_logger.append(product)
        elif prop_name == "has_for_process_event":
            for process in event_onto.has_for_process_event:
                eventInstance.has_for_process_event_of_logger.append(process)
        elif prop_name == "has_for_task_event":
            for task in event_onto.has_for_task_event:
                eventInstance.has_for_task_event_of_logger.append(task)
            eventInstance.number_of_products_logger = event_onto.number_of_products



    def removeProperties_EventLogger(self, prop_name, eventInstance):
        """
        removes connection with prop_name of a eventLogger

        :param prop_name: str
        :param eventInstance: event_logger
        """
        if prop_name == "has_for_machine_event_logger":
            eventInstance.has_for_machine_event_logger = []
        elif prop_name == "has_for_position_event_logger":
            eventInstance.has_for_position_event_logger = []
        elif prop_name == "has_for_location_event_logger":
            eventInstance.has_for_location_event_logger = []
        elif prop_name == "has_for_transport_event_logger":
            eventInstance.has_for_transport_event_logger = []
        elif prop_name == "has_for_product_event_logger":
            eventInstance.has_for_product_event_logger = []
        elif prop_name == "has_for_process_event_logger":
            eventInstance.has_for_process_event_logger = []
        elif prop_name == "has_for_task_event_logger":
            eventInstance.has_for_task_event_logger = []
            eventInstance.number_of_products_logger = 0

    def removeProperties_Event(self, prop_name, event_onto):
        """
        removes connection with prop_name, properties of event_onto

        :param prop_name: type
        :param event_onto: event onto
        """
        if prop_name == "has_for_machine_event":
            event_onto.has_for_machine_event = []
        elif prop_name == "has_for_position_event":
            event_onto.has_for_position_event = []
        elif prop_name == "has_for_location_event":
            event_onto.has_for_location_event = []
        elif prop_name == "has_for_transport_event":
            event_onto.has_for_transport_event = []
        elif prop_name == "has_for_product_event":
            event_onto.has_for_product_event = []
        elif prop_name == "has_for_process_event":
            event_onto.has_for_process_event = []
        elif prop_name == "has_for_task_event":
            event_onto.has_for_task_event = []
        elif prop_name == "has_for_service_event":
            event_onto.has_for_service_event = []
        elif prop_name == "is_event_short_term_logger_of":
            event_onto.is_event_short_term_logger_of = []
        elif prop_name == "is_event_list_of":
            event_onto.is_event_list_of = []
        elif prop_name == "number_of_products":
            event_onto.number_of_products = 0
        elif prop_name == "waiting_time":
            event_onto.waiting_time=0
        elif prop_name == "time_diff" or prop_name == "time" or prop_name=="additional_type" or prop_name=="type":
            pass
        else:
            raise Exception(prop_name+" not defined")

    def remove_from_event_list(self, event_onto):
        """
        removes event form event list

        :param event_onto: event onto
        """
        event_onto.is_event_list_of = []
