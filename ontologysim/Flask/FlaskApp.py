
from flask import Flask

from flask_swagger_ui import get_swaggerui_blueprint

from ontologysim.Flask.Actions.CommentIdAction import ComponentIdAction
from ontologysim.Flask.Actions.ComponentAction import ComponentAction
from ontologysim.Flask.Actions.DataBase.ConnectDataBaseAction import ConnectDataBaseAction
from ontologysim.Flask.Actions.DataBase.GetSimulationRunAction import GetSimulationRunAction
from ontologysim.Flask.Actions.Simulation.EventAction import EventAction
from ontologysim.Flask.Actions.GetIdsAction import GetIdsAction
from ontologysim.Flask.Actions.Simulation.KPIAction import KPIAction
from ontologysim.Flask.Actions.CheckProductType.ProcessAction import ProcessAction
from ontologysim.Flask.Actions.CheckProduction.ProductionAction import ProductionAction
from ontologysim.Flask.Actions.Simulation.KPIListAction import KPIListAction
from ontologysim.Flask.Actions.Simulation.OwlDonwloadAction import OwlDownloadAction
from ontologysim.Flask.Actions.ResetBEAction import ResetBEAction
from ontologysim.Flask.Actions.Simulation.RunSimulationAction import RunSimulationAction
from ontologysim.Flask.Actions.Simulation.SimulationLoadAction import FileLoadAction
from ontologysim.Flask.Actions.Simulation.StartAction import StartAction
from ontologysim.Flask.Actions.Simulation.StartUntilTimeAction import StartUntilTimeAction
from ontologysim.Flask.Actions.TestAction import TestAction
from flask_cors import CORS

from ontologysim.Flask.instance.config import config_dict
from ontologysim.ProductionSimulation.database.DataBase import DataBase


class FlaskAppWrapper(object):
    """

    wrapper object with handels database connection
    """

    def __init__(self, name, init, fileDict):
        """

        saves all routes, connects to database

        :param name: flask name
        :param init: Initializer
        :param fileDict: default dict of files
        """
        self.fileDict = fileDict
        self.app = Flask(name, static_url_path=None)

        try:
            app_config = config_dict["DebugDataBase"]
            self.app.config.from_object(app_config)

        except KeyError:
            exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


        #self.app.config.from_mapping(app_config.__dict__)
        self.app.static_folder = self.app.root_path + "/Flask/static"
        self.app.static_url_path = "static"

        if self.app.config["DATABASE"]:
            self.db = DataBase(self.app.config["SQLALCHEMY_DATABASE_URI"])
            self.db.create_db_tables()

        else:
            self.db = None

        # Cors
        config = {
            'ORIGINS': [
                'http://localhost:3000',
                'http://127.0.0.1:3000',
            ],

            'SECRET_KEY': 'Test'
        }
        CORS(self.app, resources={r'/*': {'origins': config['ORIGINS']}}, supports_credentials=True)

        self.init = init
        self.init.initSimCore()
        self.simCore = None
        self.stateStorage = None

        self.startAlready = False

        # defines all routings
        self.add_endpoint_get(endpoint='/nextEvent', endpoint_name='nextEvent', handler=EventAction(action, self))
        self.add_endpoint_get(endpoint='/getIds', endpoint_name='simulation', handler=GetIdsAction(action, self))
        self.add_endpoint_get(endpoint='/component', endpoint_name='component', handler=ComponentAction(action, self))
        self.add_endpoint_get(endpoint='/component/id', endpoint_name='component_kpi_id',
                              handler=ComponentIdAction(action, self))
        self.add_endpoint_post(endpoint='/start', endpoint_name='start',
                               handler=StartAction(action, self))
        self.add_endpoint_post(endpoint="/startUntilTime", endpoint_name="startUntilTime",
                               handler=StartUntilTimeAction(action, self))

        self.add_endpoint_post(endpoint="/process", endpoint_name="process", handler=ProcessAction(action, self))
        self.add_endpoint_post(endpoint="/production", endpoint_name="production",
                               handler=ProductionAction(action, self))
        self.add_endpoint_get(endpoint='/load_files', endpoint_name='load_files',
                              handler=FileLoadAction(action, self))
        self.add_endpoint_get(endpoint="/simulation/download/owl", endpoint_name="owlDownload",
                              handler=OwlDownloadAction(action, self))
        self.add_endpoint_post(endpoint="/runSimulation", endpoint_name="runSimulation",
                               handler=RunSimulationAction(action, self))
        self.add_endpoint_get(endpoint="/test", endpoint_name="test", handler=TestAction(action, self))

        self.add_endpoint_get(endpoint="/kpi", endpoint_name="kpi", handler=KPIAction(action, self))
        self.add_endpoint_get(endpoint="/kpiList", endpoint_name="kpiList", handler=KPIListAction(action, self))
        self.add_endpoint_get(endpoint="/reset_be", endpoint_name="reset_be", handler=ResetBEAction(action, self))

        self.add_endpoint_get(endpoint="/database/connect", endpoint_name="database_connection",
                              handler=ConnectDataBaseAction(action, self))
        self.add_endpoint_get(endpoint="/database/simulationrun", endpoint_name="getSimulationRun",
                              handler=GetSimulationRunAction(action, self))

    def addSwaggerUI(self):
        """

        adding swaggerUI to flask
        """
        SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
        # API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)
        API_URL = '/static/swagger.json'
        # Call factory function to create our blueprint
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Ontologysim Flask application"
            },
            # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
            #    'clientId': "your-client-id",
            #    'clientSecret': "your-client-secret-if-required",
            #    'realm': "your-realms",
            #    'appName': "your-app-name",
            #    'scopeSeparator': " ",
            #    'additionalQueryStringParams': {'test': "hello"}
            # }
        )

        self.app.register_blueprint(swaggerui_blueprint)

    def run(self):
        """

        starting flask server
        """
        self.app.run(debug=True,host="0.0.0.0", use_debugger=True, use_reloader=True)

    def add_endpoint_get(self, endpoint=None, endpoint_name=None, handler=None):
        """

        allow get request
        :param endpoint: rule
        :param endpoint_name: unique name
        :param handler: ActionInstance
        """
        self.app.add_url_rule(rule=endpoint, endpoint=endpoint_name, view_func=handler, provide_automatic_options=True,
                              methods=["GET", "OPTIONS"])

    def add_endpoint_post(self, endpoint=None, endpoint_name=None, handler=None):
        """

        allow post request
        :param endpoint: rule
        :param endpoint_name: unique name
        :param handler: ActionInstance
        """
        self.app.add_url_rule(rule=endpoint, endpoint=endpoint_name, view_func=handler, provide_automatic_options=True,
                              methods=["POST", "OPTIONS"])

    def addCors(self, response):
        """
        allowing cors

        :param response:
        :return: response
        """
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response


def action():
    """

    needed when using this kind of flask routing
    """
    pass
    # Execute anything
