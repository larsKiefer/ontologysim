import json
from flask import Flask, Response, json, request

class APIAction(object):
    """

    Main action class
    """

    def __init__(self, action, flaskApp):
        """

        :param action:
        :param flaskApp: FlaskApp
        """

        self.action = action
        self.flaskApp = flaskApp


    def __call__(self, *args):
        """

        parent entry point class
        :param args:
        """
        pass

    def addCors(self,response):
        """
        allowing cors

        :param response:
        :return: response
        """
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response

    def response400BadRequest(self,message):
        """

        sends 401 error if bad request

        :param message: string
        :return: response
        """
        return Response(status=400, headers={}, response={json.dumps({"message":message})},
                                 mimetype='application/json')

    def response500InternalServerError(self):
        """

        sends 500 error if internal server

        :return: response
        """
        return Response(status=400, headers={}, response={json.dumps({"message":"internal server appears"})},
                                 mimetype='application/json')

    def response200OK(self,json):
        """

        sends 200 successful response

        :param json
        :return: response
        """
        return Response(status=200, headers={}, response={json},
                                 mimetype='application/json')