from distutils.util import strtobool

from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.sim.Enum import Label


class ComponentIdAction(APIAction):
    """

    get: /component/id: getting information over a owl-object
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()
        id = request.args.get('id', default='', type=str)

        if id=='':
            self.response = Response(status=400, headers={}, response={json.dumps({
                "code": '400',
                "name": 'component/id',
                "description": "type is not definied or programmed: " + id,
            })},
                                     mimetype='application/json')

        else:
            try:
                label= self.flaskApp.simCore.central.fromIdGetType(id)

                if label=="id not found":

                    self.response = Response(status=400, headers={}, response={json.dumps({
                        "code": '400',
                        "name": 'component/id',
                        "description": "type is not defined or programmed: " + id,
                    })},
                                             mimetype='application/json')
                else:

                    response_dict={}

                    if label == Label.Machine.name:
                        response_dict[Label.Machine.name]=self.flaskApp.simCore.machine.transformToDict(id)
                    elif label == Label.Transporter.name:
                        response_dict[Label.Transporter.name]=self.flaskApp.simCore.transport.transformToDict(id)
                    elif label == Label.Queue.name or label == Label.StartQueue.name or label == Label.EndQueue.name or label == Label.DeadlockQueue.name:
                        if label == Label.Queue.name:
                            response_dict[Label.Queue.name] = self.flaskApp.simCore.queue.transformToDict(id)
                        elif label == Label.StartQueue.name:
                            response_dict[Label.StartQueue.name] = self.flaskApp.simCore.queue.transformToDict(id)
                        elif label == Label.EndQueue.name:
                            response_dict[Label.EndQueue.name] = self.flaskApp.simCore.queue.transformToDict(id)
                        elif label == Label.DeadlockQueue.name:
                            response_dict[Label.DeadlockQueue.name] = self.flaskApp.simCore.queue.transformToDict(id)

                    if 'error' in response_dict.keys():
                        self.response = Response(status=401, headers={}, response={json.dumps({
                                    "error": '400',
                                    "name": 'component/id',
                                    "description": "type is not defined or programmed: " + id,
                                })},
                                                 mimetype='application/json')
                    else:

                        self.response = Response(status=200, headers={}, response={json.dumps(response_dict)} ,
                                             mimetype='application/json')

            except Exception as e:
                print(e)
                self.response = Response(status=500, headers={}, response={json.dumps({
                    "code": '500',
                    "name": 'getID',
                    "description": "ontology not created",
                })})

        return self.response