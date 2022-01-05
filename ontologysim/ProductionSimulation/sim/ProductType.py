from deprecated.sphinx import deprecated

from ontologysim.ProductionSimulation.sim.Enum import Label


class ProductType:
    """
    handles the petri nets and the production process onto
    """
    def __init__(self,simCore):
        """

        :param simCore:
        """
        self.simCore=simCore
        self.dict= {}
        self.percentageDict ={} #[productTypeName][stateName]


    def init_percentage_dict(self):
        """
        initialize percentage dict of how far the product is processed, given a state
        :return:
        """
        #TODO merge
        product_type_list = self.simCore.onto.search(type=self.simCore.central.product_type_class)

        for productTypeOnto in product_type_list:
            self.percentageDict[productTypeOnto.name]= {}
            stateOntoList = productTypeOnto.is_product_type_of_state

            for stateOnto in stateOntoList:
                self.percentageDict[productTypeOnto.name][stateOnto.state_name] = self.iterateAverageProductTree(stateOnto)

            for stateOnto in stateOntoList:

                if(stateOnto.state_name!="source"):
                    self.percentageDict[productTypeOnto.name][stateOnto.state_name] = 1 - \
                                                                                 self.percentageDict[productTypeOnto.name][
                                                                                     stateOnto.state_name] / \
                                                                                 self.percentageDict[productTypeOnto.name][
                                                                                     "source"]

            self.percentageDict[productTypeOnto.name]["source"] = 0

        print(self.percentageDict)

    def iterateAverageProductTree(self,state):
        """
        get the average product tree length
        :param state: onto
        :return:
        """
        if (state.state_name=="sink"):
            return 0;

        nextStateList=[]
        for processOnto in state.has_for_prod_type_process_state:
            nextState = processOnto.is_prod_type_process_of_state[0]
            nextStateList.append(nextState)

        return min([self.iterateAverageProductTree(state) for state in nextStateList]) + 1

    def iterateMinProductTree(self,state):
        """
        get the min product type tree
        :param state: onto
        :return:
        """
        if (state.state_name=="sink"):
            return 0;

        nextStateList=[]
        for processOnto in state.has_for_prod_type_process_state:
            nextState = processOnto.is_prod_type_process_of_state[0]
            nextStateList.append(nextState)

        return min([self.iterateMinProductTree(state) for state in nextStateList]) + 1;

    def iterateMaxProductTree(self,state):
        """
        get max product tree
        :param state:
        :return:
        """

        if (state.state_name == "sink"):
            return 0

        nextStateList = []
        for processOnto in state.has_for_prod_type_process_state:
            nextState = processOnto.is_prod_type_process_of_state[0]


        return max([self.iterateMaxProductTree(state) for state in nextStateList]) + 1;

    def createProductType(self,product_type_config,process_config):
        """
        create product type and the product tree
        :param product_type_config:
        :param process_config:
        :return:
        """
        product_typeInstance=self.simCore.central.product_type_class(Label.ProductType.value+str(self.simCore.product_type_id))

        process_product_type_config=product_type_config['config']
        sinkStateInstance = self.simCore.central.state_class(
            Label.State.value + str(self.simCore.state_id))
        sinkStateInstance.state_name="sink"
        product_typeInstance.is_product_type_of_state.append(sinkStateInstance)
        self.simCore.state_id += 1

        sourceStateInstance = self.simCore.central.state_class(
            Label.State.value + str(self.simCore.state_id))
        product_typeInstance.is_product_type_of_state.append(sourceStateInstance)
        sourceStateInstance.state_name = "source"
        product_typeInstance.is_product_type_of_source = [sourceStateInstance]
        self.simCore.state_id += 1

        for process_list in process_product_type_config:
            if len(process_list)==1:

                processInstance = self.simCore.central.prod_type_process_class(
                    Label.ProdTypeProcess.value + str(self.simCore.prod_type_process_id))
                self.simCore.prod_type_process_id += 1
                process_onto = self.simCore.onto[Label.Process.value + str(process_list[0])]
                processInstance.is_for_prod_type_process_of.append(process_onto)
                sourceStateInstance.has_for_prod_type_process_state.append(processInstance)
                processInstance.is_prod_type_process_of_state.append(sinkStateInstance)

                if "merged" in process_config.keys():

                    for element in process_config["merged"]["in"]:
                        #print(product_typeInstance.name.replace(Label.ProductType.value, ""), element["product_type"])
                        if process_onto.process_id == process_list[0]:
                            for combine_process_data_onto in process_onto.has_for_input_combine:
                                #print(int(product_typeInstance.name.replace(Label.ProductType.value, "")) == int(element["product_type"]),product_typeInstance.name.replace(Label.ProductType.value, ""),element["product_type"])
                                if int(product_typeInstance.name.replace(Label.ProductType.value, "")) == int(element["product_type"]) and len(combine_process_data_onto.has_for_state_combine_process_data) ==0 :
                                    #combine_process_data_onto.number_state = int(element["number"])
                                    combine_process_data_onto.has_for_state_combine_process_data.append(sourceStateInstance)
                                    break

                    for element in process_config["merged"]["out"]:
                        if process_onto.process_id == process_list[0]:
                            # print(product_typeInstance.name.replace(Label.ProductType.value, ""), element["product_type"])
                            for combine_process_data_onto in process_onto.has_for_output_combine:
                                if int(product_typeInstance.name.replace(Label.ProductType.value, "")) == int(element[
                                    "product_type"])  and len(combine_process_data_onto.has_for_state_combine_process_data) ==0 :
                                    #combine_process_data_onto.number_state = int(element["number"])
                                    combine_process_data_onto.has_for_state_combine_process_data.append(sourceStateInstance)
                                    break

            else:

                processInstance = self.simCore.central.prod_type_process_class(
                    Label.ProdTypeProcess.value + str(self.simCore.prod_type_process_id))
                self.simCore.prod_type_process_id += 1

                processInstance.is_for_prod_type_process_of.append(
                    self.simCore.onto[Label.Process.value + str(process_list[0])])
                sourceStateInstance.has_for_prod_type_process_state.append(processInstance)

                stateInstance = self.simCore.central.state_class(
                    Label.State.value + str(self.simCore.state_id))
                stateInstance.state_name = stateInstance.name
                product_typeInstance.is_product_type_of_state.append(stateInstance)
                self.simCore.state_id += 1
                processInstance.is_prod_type_process_of_state.append(stateInstance)

                for process in process_list[1:-1]:
                    processInstance = self.simCore.central.prod_type_process_class(
                        Label.ProdTypeProcess.value + str(self.simCore.prod_type_process_id))
                    processInstance.is_for_prod_type_process_of.append(
                        self.simCore.onto[Label.Process.value + str(process)])
                    self.simCore.prod_type_process_id += 1

                    stateInstance.has_for_prod_type_process_state.append(processInstance)

                    stateInstance = self.simCore.central.state_class(
                        Label.State.value + str(self.simCore.state_id))
                    stateInstance.state_name = stateInstance.name
                    product_typeInstance.is_product_type_of_state.append(stateInstance)
                    processInstance.is_prod_type_process_of_state.append(stateInstance)
                    self.simCore.state_id += 1

                processInstance = self.simCore.central.prod_type_process_class(
                    Label.ProdTypeProcess.value + str(self.simCore.prod_type_process_id))
                processInstance.is_for_prod_type_process_of.append(
                    self.simCore.onto[Label.Process.value + str(process_list[-1])])
                self.simCore.prod_type_process_id += 1

                stateInstance.has_for_prod_type_process_state.append(processInstance)
                processInstance.is_prod_type_process_of_state.append(sinkStateInstance)


        self.simCore.product_type_id += 1

    @deprecated(version='0.1.0', reason="pm4py excluded")
    def loadPetriNet(self,path):
        """
        depreciated
        loads petri net from path (pnml-file) and adds the date to product type onto
        checks the pnml net
        saves the net in the dict variable, for faster acess

        :param path:
        """

        """
        with open(path, 'r') as file:
            data = file.read()

            product_typeInstance=self.simCore.central.product_type_class(Label.ProductType.value+str(self.simCore.product_type_id))
            product_typeInstance.pnml=data


        net, initial_marking, final_marking = pnml_importer.apply(path)

        PnmlTest.check_pnml(net)
        #self.plotPetriNet(net,initial_marking,final_marking)
        self.dict.update( {Label.ProductType.value+str(self.simCore.product_type_id) : net})

        self.simCore.product_type_id += 1
        """
    @deprecated(version='0.1.0', reason="pm4py excluded")
    def loadPetrNetFromString(self,product_type_onto):
        """
        deprecated
        when loading an existing owl file, then the data from the onto are added to the dict

        :param product_type_onto:
        """
        """
        data=product_type_onto.pnml
        net, initial_marking, final_marking=pnml_importer.pnml.petri.importer.versions.pnml.import_petri_from_string(data)
        PnmlTest.check_pnml(net)

        self.dict.update({product_type_onto.name: net})
        """

    @deprecated(version='0.1.0', reason="pm4py excluded")
    def plotPetriNet(self,net,final_marking,initial_marking):
        """
        deprecated
        method for plotting the pnml

        :param net: pm4py-net
        :param final_marking: pm4py marking
        :param initial_marking: pm4py marking
        """
        """
        from pm4py.visualization.petrinet import factory as pn_vis_factory

        gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
        pn_vis_factory.view(gviz)
        """

    def getProdProcessId(self):
        """
        all process ids in the pnml net

        :return: [process ids]
        """

        """
        transistion_id_list=[]
        for label_prodType, net in self.dict.items():
            transistion_id_list.append([trans.label for trans in net.transitions])

        return list(set( [int(item) for sublist in transistion_id_list for item in sublist] ))
        """


        process_id_list = []
        for prod_type in self.simCore.onto.search(type=self.simCore.central.product_type_class):
            state_list = prod_type.is_product_type_of_state

            for state in state_list:
                prod_process_list = state.has_for_prod_type_process_state

                for prod_process in prod_process_list:
                    process_id_list.append(prod_process.is_for_prod_type_process_of[0].process_id)

        return process_id_list

    def transformToDict(self,id ):
        """
        transform to dict
        :param id: string one label or "all"
        :return:
        """

        response_dict={}
        if(id=="all"):
            product_type_list=[product_type_onto for product_type_onto  in self.simCore.onto.search(type=self.simCore.central.product_type_class)]
        else:
            product_type_list=[self.simCore.onto[id]]
        if product_type_list==[None]:
            return {'error':"id_not_found"}
        for product_type_onto in product_type_list:

            response_dict[product_type_onto.name]={}
            response_dict[product_type_onto.name]['state']=[state_onto.name for state_onto in product_type_onto.is_product_type_of_state ]
            response_dict[product_type_onto.name]['source_state']=[state_onto.name for state_onto in product_type_onto.is_product_type_of_source ]

        return response_dict

    def getCompleteProductTypePath(self,label):
        """
        get complete product type path for api
        :param label: string
        :return: dict
        """
        response_dict = {}
        product_type_onto = self.simCore.onto[label]
        response_dict["name"] = product_type_onto.name
        response_dict["source_state"] = [state_onto.name for state_onto in product_type_onto.is_product_type_of_source ]
        response_dict["path"] =[]
        response_dict["process_info"] =[]
        product_type_process_list=[]
        state_list = [state_onto for state_onto in product_type_onto.is_product_type_of_state]

        for state_onto in state_list:

            product_type_process_list.append(state_onto.has_for_prod_type_process_state)
        flat_list = [item for sublist in product_type_process_list for item in sublist]
        product_type_process_list = list(set(flat_list))
        for state_onto in state_list:
            response_dict["path"].append({"state":state_onto.name,"forward_process":[prod_type_process_onto.name for prod_type_process_onto in state_onto.has_for_prod_type_process_state],
                                          "reverse_process":[prod_type_process_onto.name for prod_type_process_onto in state_onto.has_for_reverse_prod_type_process_state]})

        for product_type_process_onto in product_type_process_list:

            process_onto=product_type_process_onto.is_for_prod_type_process_of[0]
            response_dict["process_info"].append({"product_type_process_name":product_type_process_onto.name,"name": process_onto.name,"state_onto":product_type_process_onto.is_prod_type_process_of_state[0].name, "process_id":  process_onto.process_id})

        sourceState = product_type_onto.is_product_type_of_source[0]
        stateNumberDict={}
        iterationFinished =False
        stateNumberDict[sourceState.name]=1
        stateList=[sourceState]
        stateListNextIteration=[]
        i=0
        while(not iterationFinished):

            for state_onto in stateList:
                process_list = state_onto.has_for_prod_type_process_state

                for process_onto in process_list:
                    state_onto2 = process_onto.is_prod_type_process_of_state[0]
                    stateNumberDict[state_onto2.name] = stateNumberDict[state_onto.name]+1

                    stateListNextIteration.append(state_onto2)


            if(len(stateListNextIteration)==0):
                iterationFinished=True
            else:
                stateList = [state_onto for state_onto in  stateListNextIteration if state_onto.has_for_prod_type_process_state!=[]]
                stateListNextIteration=[]

            i+=1

        response_dict["max_state"] =stateNumberDict[max(stateNumberDict, key=stateNumberDict.get)]


        return response_dict