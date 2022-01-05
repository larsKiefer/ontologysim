from flask import json, request

from ontologysim.Flask.Actions.APIAction import APIAction
from ontologysim.ProductionSimulation.init.API.IntitializerProducttypeAPI import InitializerProducttypeAPI


class ProcessAction(APIAction):
    """

    /process: post: process list to product type
    """

    def __call__(self, *args):
        """

        :param args:
        :return:
        """
        self.action()

        requestBody=request.data
        if (len(requestBody) == 0):
            return self.response400BadRequest("request body is not correct")
        requestDict =json.loads(requestBody)
        if("list" in requestDict.keys()):

            process_list=requestDict["list"]

            if(not self.checkInputProcessList(process_list)):
                self.response = self.response400BadRequest("process list is not correct")
            else:

                allProcesses = list(set([item for sublist in process_list for item in sublist]))
                process_config = []
                for process in allProcesses:
                    process_config.append({"id":process,"mean":1,"deviation":1,"type":"normal"})

                initializer = InitializerProducttypeAPI()

                for process in process_config:
                    initializer.s.process.createProcess(process)

                initializer.s.product_type.createProductType({'id':0,'config':process_list}, {})

                product_type_config = initializer.s.product_type.getCompleteProductTypePath(initializer.s.onto.search(type=initializer.s.central.product_type_class)[0].name)

                initializer.s.destroyOnto()

                self.response = self.response200OK(json.dumps((product_type_config)))

        else:
            self.response = self.response400BadRequest("request body is not correct")

        return self.response

    def checkInputProcessList(self,prcessList):
        """
        check if process list is correctly give
        :param prcessList: list
        :return: bool, true=correct
        """

        isCorrect = False
        if(len(prcessList)>0):
            for processSubList in prcessList:
                if(not isinstance(processSubList,list)):
                    return isCorrect
                else:
                    for process in processSubList:
                        if (not isinstance(process, int)):
                            return isCorrect

        isCorrect = True
        return isCorrect


