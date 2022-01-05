import unittest
import json
import inspect
import os
import sys

from ontologysim.ProductionSimulation.utilities.path_utilities import PathTest
from tests.util.ProductionGenerator import ProductionGenerator

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from ontologysim.ProductionSimulation.init.Initializer import Initializer

from ontologysim.Flask.FlaskApp import FlaskAppWrapper

BASE_URL = 'http://127.0.0.1:5000'



class TestFlaskApi(unittest.TestCase):
    """
    class which test all flask apis
    """
    def setUp(self):
        """
        mehtod which is called every time befor a test method
        create flask test_client
        """
        init = Initializer(current_dir)
        PathTest.current_main_dir = current_dir
        production_config_path = "/ontologysim/Flask/Assets/DefaultFiles/production_config_lvl3.ini"
        owl_config_path = "/ontologysim/Flask/Assets/DefaultFiles/owl_config.ini"
        controller_config_path = "/ontologysim/Flask/Assets/DefaultFiles/controller_config.ini"
        logger_config_path = "/ontologysim/Flask/Assets/DefaultFiles/logger_config_lvl3.ini"
        self.flaskWrapper = FlaskAppWrapper('wrap', init, {'production': production_config_path, 'owl': owl_config_path,
                                           'controller': controller_config_path, 'logger': logger_config_path})
        self.flaskWrapper.addSwaggerUI()

        self.testApp= self.flaskWrapper.app.test_client()

    def createProductionDict(self):
        """
        loading (reading) file from default falsk file list and add data iin dict
        :return: list[{path,content}]
        """
        fileList=[]
        pathProduction = PathTest.check_file_path(self.flaskWrapper.fileDict["production"])
        pathOWL = PathTest.check_file_path(self.flaskWrapper.fileDict["owl"])
        pathController = PathTest.check_file_path(self.flaskWrapper.fileDict["controller"])
        pathLogger = PathTest.check_file_path(self.flaskWrapper.fileDict["logger"])
        fileOWL = open(pathOWL, "r")
        fileController = open(pathController, "r")
        fileLogger = open(pathLogger, "r")
        fileProduction = open(pathProduction, "r")

        fileList.append({'path': 'owl_config.ini', 'content': fileOWL.read()})
        fileList.append({'path': 'controller.ini', 'content': fileController.read()})
        fileList.append({'path': 'logger.ini', 'content': fileLogger.read()})
        fileList.append({'path': 'production_config.ini', 'content': fileProduction.read()})

        fileOWL.close()
        fileController.close()
        fileLogger.close()
        fileProduction.close()
        return fileList

    def runSimulationUntil(self,time):
        """
        test "/startUntilTime"
        :param time: double
        :return:
        """
        url = BASE_URL + '/startUntilTime'
        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini',
                                     'production_config_lvl3.ini'], 'files': [], 'isDefaultSelected': True,
                    'isDragDropSelected': False, 'isLoading': False, "time": time, "onlyLastEvent": True}
        dataDict["files"] = self.createProductionDict()
        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())

        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("productionDict" in data.keys())
        self.assertTrue("eventOntoList" in data.keys())
        self.assertTrue(self.flaskWrapper.simCore.getCurrentTimestep() > time)

    def test_get_test_connection(self):
        """
        test "/test" (connection test)
        :return:
        """

        url = BASE_URL + '/test'
        response = self.testApp.get(url)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'OK')

    def test_item_not_exist(self):
        """
        test 404 errror
        :return:
        """
        response = self.testApp.get(BASE_URL)
        self.assertEqual(response.status_code, 404)

    def test_get_reset_be(self):
        """
        test "/reset_be", reset simulation run
        :return:
        """
        url = BASE_URL + '/reset_be'
        response = self.testApp.get(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data["alreadyStarted"], False)
        self.assertEqual(data["run"], False)
        self.assertEqual(data["production"], {})

    def test_get_database_connection(self):
        """
        test "/database/connect"
        :return:
        """
        url = BASE_URL + '/database/connect'
        response = self.testApp.get(url)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], 'OK')

    def test_get_database_simulation_runs(self):
        """
        test "/database/simulationrun"
        :return:
        """
        url = BASE_URL + '/database/simulationrun'
        response = self.testApp.get(url)
        data = json.loads(response.get_data())
        self.assertTrue(isinstance(data['result'],list))

    def test_get_database_simulation_runs(self):
        """
        test "/database/simulationrun"
        :return:
        """
        url = BASE_URL + '/database/simulationrun'
        response = self.testApp.get(url)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data['result'],list))

    def test_post_checkProductType_Process(self):
        """
        test "/process" with correct and wrong input
        :return:
        """
        item = {"list": [[1]]}
        url = BASE_URL + '/process'
        try:
            self.flaskWrapper.init.s.destroyOnto()
        except:
            print("onto not defined")
        response = self.testApp.post(url,
                                 data=json.dumps(item),
                                 content_type='application/json')
        data = response.get_data()
        data=json.loads(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['max_state'], 2)
        self.assertEqual(data['name'], "p_t0")
        self.assertTrue(isinstance(data['path'], list))

        item = {"list": [1]}
        url = BASE_URL + '/process'
        response = self.testApp.post(url,
                                     data=json.dumps(item),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_checkProduction_Production(self):
        """
        test "/production"
        :return:
        """
        try:
            self.flaskWrapper.init.s.destroyOnto()
        except:
            print("onto not defined")
        self.productGenerator = ProductionGenerator(seedParameter=1)
        productionDict = self.productGenerator.createConfigDict()

        d = dict(productionDict._sections)
        for k in d:
            d[k] = dict(productionDict._defaults, **d[k])
            d[k].pop('__name__', None)

        item = {"data": d }
        url = BASE_URL + '/production'
        response = self.testApp.post(url,
                                 data=json.dumps(item),
                                 content_type='application/json')
        data = response.get_data()
        data=json.loads(data)

        self.assertEqual(200,response.status_code)

    def test_get_default_files(self):
        """
        test "/load_files"
        :return:
        """
        url = BASE_URL + '/load_files'
        response = self.testApp.get(url)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data['files'],list))
        self.assertTrue(len(data['files']),4)

    def test_get_start_with_default_files(self):
        """
        test "/start" with default fiels form flask default app folder
        :return:
        """
        url = BASE_URL + '/start'
        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini', 'production_config_lvl3.ini'], 'files': [], 'isDefaultSelected': True, 'isDragDropSelected': False, 'isLoading': False}

        response = self.testApp.post(url,data=json.dumps(dataDict),content_type='application/json')
        data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 200)
        self.assertTrue("alreadyStarted" in data.keys())
        self.assertTrue("production" in data.keys())
        self.assertTrue("run" in data.keys())


    def test_get_start(self):
        """
        test "/start" with data in api request
        :return:
        """
        url = BASE_URL + '/start'

        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini',
                                     'production_config_lvl3.ini'], 'files': [],
                    'isDefaultSelected': False, 'isDragDropSelected': True, 'isLoading': False}
        dataDict["files"] = self.createProductionDict()
        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 200)
        self.assertTrue("alreadyStarted" in data.keys())
        self.assertTrue("production" in data.keys())
        self.assertTrue("run" in data.keys())

    def test_nextEvent(self):
        """
        test "/nextEvent" with default values and number=2&full=True&productionTrue
        :return:
        """
        self.test_get_start_with_default_files()

        url = BASE_URL + '/nextEvent'

        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["eventOntoList"]),1)
        self.assertTrue("productionDict" in data.keys())

        url = BASE_URL + '/nextEvent?number=2&full=True&productionTrue'

        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["eventOntoList"]), 2)
        self.assertTrue("productionDict" in data.keys())



    def test_startUnitTime_defaultFiles(self):
        """
        test "/startUntilTime" with default files from flask folder
        :return:
        """
        url = BASE_URL + '/startUntilTime'
        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini',
                                     'production_config_lvl3.ini'], 'files': [], 'isDefaultSelected': True,
                    'isDragDropSelected': False, 'isLoading': False,"time":100,"onlyLastEvent":True}

        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("productionDict" in data.keys())
        self.assertTrue("eventOntoList" in data.keys())
        self.assertTrue(self.flaskWrapper.simCore.getCurrentTimestep()>100)

    def test_startUnitTime(self):
        """
        test "/runSimulationUntil" with data in request and time ==100
        :return:
        """
        self.runSimulationUntil(100)

    def test_runSimulation(self):
        """
        test "/runSimulation" with files loaded form Flask folder
        :return:
        """
        url = BASE_URL + '/runSimulation'
        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini',
                                     'production_config_lvl3.ini'], 'files': [], 'isDefaultSelected': True,
                    'isDragDropSelected': False, 'isLoading': False, "eventData": False}
        dataDict["files"] = self.createProductionDict()
        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("eventOntoList" in data.keys())
        self.assertTrue("simulationFinished" in data.keys())


    def test_runSimulation_defaultFiles(self):
        """
        test "/runSimulation" with default files
        :return:
        """
        url = BASE_URL + '/runSimulation'
        dataDict = {'defaultFiles': ['controller_config.ini', 'logger_config_lvl3.ini', 'owl_config.ini',
                                     'production_config_lvl3.ini'], 'files': [], 'isDefaultSelected': True,
                    'isDragDropSelected': False, 'isLoading': False,"eventData":False}

        response = self.testApp.post(url, data=json.dumps(dataDict), content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("eventOntoList" in data.keys())
        self.assertTrue("simulationFinished" in data.keys())

    def test_kpi(self):
        """
        test "/kpi"
        :return:
        """
        self.runSimulationUntil(300)

        url = BASE_URL + '/kpi'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 200)
        keyList = ['machine', 'product', 'queue', 'sim', 'transporter', 'transporter_location']
        for key in keyList:
            self.assertTrue(key in data.keys())

    def test_kpiList(self):
        """
        test "/kpiList"
        :return:
        """
        self.runSimulationUntil(300)

        url = BASE_URL + '/kpiList'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())

        self.assertEqual(response.status_code, 200)
        keyList = ['machine', 'product', 'queue', 'sim', 'transporter', 'transporter_location']
        for key in keyList:
            self.assertTrue(key in data.keys())

    def test_getIds(self):
        """
        test "/getIds"
        :return:
        """
        url = BASE_URL + '/getIds'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500)

        self.test_get_start()

        url = BASE_URL + '/getIds'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        keyList = ['deadlock_queue', 'end_queue', 'machine', 'machine_queue', 'start_queue', 'transporter', 'transporter_queue']
        for key in keyList:
            self.assertTrue(key in data.keys())
        self.assertEqual(response.status_code, 200)

        url = BASE_URL + '/getIds?type=machine'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(len(data.keys()),1)
        self.assertEqual(response.status_code, 200)


    def test_component(self):
        """
        test "/component" with error 500 and working api
        :return:
        """
        url = BASE_URL + '/component'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500)

        self.test_get_start()

        url = BASE_URL + '/component'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertTrue(isinstance(data["Machine"]["m0"], dict))
        keyList = ['DeadlockQueue', 'EndQueue', 'Machine', 'MachineQueue', 'StartQueue', 'Transporter', 'TransporterQueue']
        for key in keyList:
            self.assertTrue(key in data.keys())
        self.assertEqual(response.status_code, 200)

    def test_componentId(self):
        """
        test "/component/id" , id=m0 and id=""
        :return:
        """
        url = BASE_URL + '/component/id?id=m0'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 500)

        self.test_get_start()

        url = BASE_URL + '/component/id?id=m0'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertTrue(isinstance(data["Machine"]["m0"],dict))
        self.assertEqual(response.status_code, 200)

        url = BASE_URL + '/component/id'
        response = self.testApp.get(url, content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()