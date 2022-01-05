from distutils.util import strtobool

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.sim.Enum import Label


class GetIdsAction(APIAction):
    """

    get: /getIds: get list of ontologysim labels
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        type = request.args.get('type', default='all', type=str)

        try:
            dictIDs = self.flaskApp.simCore.central.getIds(type)

            # all, machine, transporter, product
            if (len(dictIDs) > 0):
                self.response = Response(status=200, headers={}, response={json.dumps(dictIDs)},
                                         mimetype='application/json')
            else:
                self.response = Response(status=400, headers={}, response={json.dumps({
                    "code": '400',
                    "name": 'getID',
                    "description": "type is not definied: " + type,
                })},
                                         mimetype='application/json')
        except Exception as e:
            print(e)
            self.response = Response(status=500,headers={}, response={json.dumps({
                    "code": '500',
                    "name": 'getID',
                    "description": "ontology not created",
                })})

        return self.response