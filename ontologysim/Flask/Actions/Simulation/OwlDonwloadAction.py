from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest
from flask import Flask, Response, json, request

class OwlDownloadAction(APIAction):
    """
    get: /simulation/download/owl: sending owl file via string
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        if(self.flaskApp.startAlready):
            defaultPath="/ontologysim/Flask/Assets/DefaultSaveFolder/saved.owl"
            print(PathTest.check_dir_path(defaultPath))
            self.flaskApp.simCore.save_ontology(defaultPath)
            f = open(PathTest.check_file_path(defaultPath), "r")
            fString= f.read()

            self.response=self.response200OK(json.dumps({"file":fString}))

        else:
            self.response= self.response400BadRequest("simulation not started")

        return self.response