class SubClassUtility:
    """
    given a parent class and it finds all sub classes
    """
    @classmethod
    def get_all_subclasses(cls, python_class):
        """
        Helper function to get all the subclasses of a class.

        :param python_class: Any Python class that implements __subclasses__()
        :return: []
        """

        subclasses = set()
        check_these = [python_class]

        while check_these:
            parent = check_these.pop()
            for child in parent.__subclasses__():

                if child not in subclasses:
                    subclasses.add(child)
                    check_these.append(child)

        return sorted(subclasses, key=lambda x: x.__name__)

    @classmethod
    def get_all_subclasses_dict(self, python_class):
        """
        Helper function to get all the subclasses of a class.

        :param python_class: Any Python class that implements __subclasses__()
        :return: dict
        """
        class_dict = {}
        for subclass in self.get_all_subclasses(python_class):
            class_dict[subclass.__name__] = subclass
        class_dict[python_class.__name__] = python_class

        return class_dict
