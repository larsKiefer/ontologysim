import math

from ProductionSimulation.sim.Enum import Label


class Location:
    """
    python instance which handles the ontologysim location
    """
    def __init__(self,simCore):
        self.simCore=simCore
        self.distance_dict={}
        self.location_queue_dict={}

    def createLocation(self,location_list):
        """
        create ontologysim location

        :param location_list: [x,y,z]
        :return: onto
        """
        locationInstance = self.simCore.central.location_class(Label.Location.value + str(self.simCore.location_id))
        self.simCore.location_id += 1

        locationInstance.x, locationInstance.y, locationInstance.z = location_list

        return locationInstance

    def init_distance_dict(self):
        """
        calculates for every location the distance to all other location,
        used for better performance

        """
        location_list=self.simCore.onto.search(type=self.simCore.central.location_class)

        for location1 in location_list:
            self.distance_dict[location1.name]={}
            for location2 in location_list:
                self.distance_dict[location1.name][location2.name]=0

        a=len(location_list)-1
        b=a

        for i1 in range(a):

            for i2 in range(b):

                if i1==i2:
                    self.distance_dict[location_list[i1].name][location_list[i2].name]=0
                else:
                    distance=self.calculateDistance(location_list[i1],location_list[i2])
                    self.distance_dict[location_list[i1].name][location_list[i2].name]=distance
                    self.distance_dict[location_list[i2].name][location_list[i1].name] = distance
            b=b-1

        queue_list = self.simCore.onto.search(type=self.simCore.central.queue_class)
        self.location_queue_dict["location"]={}
        self.location_queue_dict["queue"]={}
        for queueOnto in queue_list:
            locationOntoList= queueOnto.has_for_queue_location

            if(len(locationOntoList)>0):
                locationOnto =locationOntoList[0]
                self.location_queue_dict["location"][locationOnto.name] = queueOnto.name
                self.location_queue_dict["queue"][queueOnto.name] = locationOnto.name

    def calculateDistance(self,location_1,location_2):
        """
        airline calculation of distance between to onto locations

        :param location_1: onto
        :param location_2: onto
        :return: double
        """

        return math.sqrt((location_1.x-location_2.x)**2+(location_1.y-location_2.y)**2+(location_1.z-location_2.z)**2)

    def transformToDict(self,id):
        """
        saves onto location to dict

        :param id: label from onto
        :return: dict{x,y,z}
        """
        response_dict={}

        location_onto = self.simCore.onto[id]
        response_dict['coordinates']=[location_onto.x,location_onto.y,location_onto.z]
        response_dict['queue'] = self.location_queue_dict["location"][location_onto.name]


        return response_dict

