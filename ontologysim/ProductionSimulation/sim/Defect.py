from ontologysim.ProductionSimulation.sim.Enum import Label


class Defect:
    """
    python instance for changing the defect onto
    """

    def __init__(self, simCore):
        """
        set defect_possible variables
        :param simCore:
        """
        self.simCore = simCore
        self.machine_defect_possible = False
        self.transport_defect_possible = False

    def createDefect(self, random_dict, normal_distribution_list):
        """
        creates defect in ontology
        :param random_dict: responsible for the probability of which type of defect will occur next
        :param normal_distribution_list: sets the distribution function for "when does the next defect occur"
        :return: defect_onto
        """
        defect_onto = self.simCore.central.defect_class(Label.Defect.value + str(self.simCore.defect_id))
        random_distribution = self.simCore.distribution.createDistribution(random_dict, defect_onto.name)

        defect_onto.has_for_defect_type_distribution.append(random_distribution)
        self.simCore.defect_id += 1
        for normal_distribution in normal_distribution_list:
            sub_defect_onto = self.createSubDefect(normal_distribution["defect_type"])
            defect_distribution_onto = self.simCore.distribution.createDistribution(normal_distribution['defect'],
                                                                                    sub_defect_onto.name)
            repair_distribution_onto = self.simCore.distribution.createDistribution(normal_distribution['repair'],
                                                                                    sub_defect_onto.name + "1")
            defect_onto.has_for_sub_defect.append(sub_defect_onto)
            sub_defect_onto.has_for_sub_defect_distribution.append(defect_distribution_onto)
            sub_defect_onto.has_for_repair_distribution.append(repair_distribution_onto)

        return defect_onto

    def createSubDefect(self, defect_type):
        """
        sub defect saves the distribution function for "when does the next defect occur"
        :param defect_type: string
        :return: sub_defect (onto)
        """
        sub_defect = self.simCore.central.sub_defect_class(Label.SubDefect.value + str(self.simCore.sub_defect_id))
        sub_defect.defect_type = defect_type
        self.simCore.sub_defect_id += 1
        return sub_defect

    def getNextDefectTime(self, defect_onto):
        """
        calculates the value of the distribution function
        :param defect_onto: onto
        :return: next defect time (int), defect type (str)
        """
        if len(defect_onto.is_defect_of_machine) > 0:
            random_distribution = defect_onto.has_for_defect_type_distribution.__getitem__(0)
            random_value = self.simCore.distribution.getRandomTimefromOnto(random_distribution)
            sub_defect = defect_onto.has_for_sub_defect[random_value]
            distribution_onto = sub_defect.has_for_sub_defect_distribution.__getitem__(0)
            next_defect_time = self.simCore.getCurrentTimestep() + self.simCore.distribution.getTimefromOnto(
                distribution_onto)
        elif len(defect_onto.is_defect_of_transporter) > 0:
            random_distribution = defect_onto.has_for_defect_type_distribution.__getitem__(0)
            random_value = self.simCore.distribution.getRandomTimefromOnto(random_distribution)
            sub_defect = defect_onto.has_for_sub_defect[random_value]
            distribution_onto = sub_defect.has_for_sub_defect_distribution.__getitem__(0)
            next_defect_time = self.simCore.getCurrentTimestep() + self.simCore.distribution.getTimefromOnto(
                distribution_onto)

        return next_defect_time, sub_defect.defect_type
