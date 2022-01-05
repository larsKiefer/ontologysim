import json

from ontologysim.Flask.Actions.APIAction import APIAction


class TestAction(APIAction):
    """

    /test: get: test connection
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        self.response=self.response200OK(json.dumps({"message":"OK"}))

        return self.response