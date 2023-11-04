
from flask import Flask, Response, json, request
from owlready2 import destroy_entity

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.sim.Enum import Label


class ComponentAction(APIAction):
    """

    get: /component: get all objects from one type
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()
        type = request.args.get("type", default="all", type=str)
        response_dict = {}
        try:
            if (type == Label.Transporter.name or type == "all"):
                response_dict[Label.Transporter.name] = self.flaskApp.simCore.transport.transformToDict("all")

                if "error" in response_dict[Label.Transporter.name]:
                    response_dict["error"]={}

            if (type == Label.Machine.name or type == "all"):
                response_dict[Label.Machine.name] = self.flaskApp.simCore.machine.transformToDict("all")

                if "error" in response_dict[Label.Machine.name]:
                    response_dict["error"]={}

            if (type == Label.StartQueue.name or type == "all"):
                response_dict[Label.StartQueue.name]={}
                for queue_onto in self.flaskApp.simCore.central.start_queue_list:
                    response_dict[Label.StartQueue.name] = self.flaskApp.simCore.queue.transformToDict(
                        queue_onto.name)

                if "error" in response_dict[Label.StartQueue.name]:
                    response_dict["error"]={}

            if (type == Label.DeadlockQueue.name or type == "all"):
                response_dict[Label.DeadlockQueue.name] = {}
                for queue_onto in self.flaskApp.simCore.central.dead_lock_list:
                    response_dict[Label.DeadlockQueue.name] = self.flaskApp.simCore.queue.transformToDict(
                        queue_onto.name)

                if "error" in response_dict[Label.DeadlockQueue.name]:
                    response_dict["error"]={}

            if (type == Label.EndQueue.name or type == "all"):
                response_dict[ Label.EndQueue.name] = {}
                for queue_onto in self.flaskApp.simCore.central.end_queue_list:
                    response_dict[Label.EndQueue.name] = self.flaskApp.simCore.queue.transformToDict(
                        queue_onto.name)

                if "error" in response_dict[Label.EndQueue.name]:
                    response_dict["error"]={}

            if (type == "MachineQueue" or type == "all"):
                response_dict["MachineQueue"] = {}
                for queue_onto in self.flaskApp.simCore.central.machine_queue_list:
                    response_dict["MachineQueue"] = self.flaskApp.simCore.queue.transformToDict(
                        queue_onto.name)

                if "error" in response_dict["MachineQueue"]:
                    response_dict["error"]={}

            if type == "TransporterQueue" or type == "all":
                response_dict["TransporterQueue"] = {}
                for queue_onto_name in self.flaskApp.simCore.central.queue_to_transporter.keys():
                    response_dict["TransporterQueue"] = self.flaskApp.simCore.queue.transformToDict(
                        queue_onto_name)

                if "error" in response_dict["TransporterQueue"]:
                    response_dict["error"]={}

            if len(response_dict.keys()) == 0:
                response_dict["error"]={}

            if "error" in response_dict.keys():
                self.response = Response(status=401, headers={}, response={json.dumps({
                    "error": "400",
                    "name": "component/id",
                    "description": "type is not defined or programmed: " + type,
                })},
                                         mimetype="application/json")
            else:

                self.response = Response(status=200, headers={}, response={json.dumps(response_dict)},
                                         mimetype="application/json")
        except Exception as e:
            print(e)
            self.response = Response(status=500, headers={}, response={json.dumps({
                "code": '500',
                "name": 'getID',
                "description": "ontology not created",
            })})


        return self.response
