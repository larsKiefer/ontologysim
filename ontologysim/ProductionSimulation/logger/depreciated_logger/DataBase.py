import math

import pyodbc
import datetime
import pandas as pd

from ontologysim.ProductionSimulation.sim.Enum import Machine_Enum, Transporter_Enum


class DataBase:
    """

    """
    def __init__(self,connStr,dataBaseName):
        self.dataBaseName=dataBaseName
        self.connectionStr=connStr

        self.cnxn = pyodbc.connect(connStr, autocommit=True)
        self.crsr = self.cnxn.cursor()
        print("database created")
        self.schema_name_list=""
        self.table_name_list=""

        self.createDataBase()

    def execute_querry(self,string):
        """

        :param string:
        :return:
        """
        return self.crsr.execute(string)

    def createTabel(self):
        """

        """
        pass

    def createTable_EventLogger(self):
        """

        """
        schema_name = "log"
        table_name = "all_events"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            time_logger FLOAT,
                            time_diff_logger FLOAT,
                            type_logger VARCHAR (50) NOT NULL,
                            additional_type_logger VARCHAR (50),
                            product_name VARCHAR (50),
                            position_name VARCHAR (50),
                            position_info_name VARCHAR (50),
                            machine_name VARCHAR (50),
                            transport_name VARCHAR (50),
                            process_id INT,
                            location_name VARCHAR (50),
                            task_name VARCHAR (50),
                            number_of_parts INT,  
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""
        self.crsr.execute(s)

    def createSchema_log(self):
        """

        """
        schema_name = "log"
        self.crsr.execute("""IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = """ + "'" + schema_name + "'" + """ ) 
                                BEGIN

                                EXEC( 'CREATE SCHEMA """ + schema_name + """' );
                            END
                            """)

    def createSchema_simulation(self):
        """

        """
        schema_name = "simulation"
        self.crsr.execute("""IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = """ + "'" + schema_name + "'" + """ ) 
                                BEGIN

                                EXEC( 'CREATE SCHEMA """ + schema_name + """' );
                            END
                            """)

    def createDataBase(self):
        """

        """
        self.crsr.execute("IF NOT EXISTS(select * from sys.databases where name = "+"'"+self.dataBaseName+"'"+" ) CREATE DATABASE "+ self.dataBaseName )
        self.crsr.execute("USE "+ self.dataBaseName)

    def createTableRun(self):
        """

        """
        table_name = "run"
        s = """IF (NOT EXISTS (SELECT * 
                                 FROM INFORMATION_SCHEMA.TABLES 
                                 WHERE TABLE_NAME = """ + "'" + table_name + "'" + """))
                                 CREATE TABLE """  + table_name + """ (
                                    id INT PRIMARY KEY IDENTITY (1, 1),
                                    date datetime NOT NULL,
                                    number_of_parts INT,
                                    comment VARCHAR(50),
                                    
                                );"""
        self.crsr.execute(s)

    def insertCurrentRun(self,number_of_parts,comment):
        """

        :param number_of_parts:
        :param comment:
        """
        table_name="run"
        column_list="date,number_of_parts,comment"
        insert_string = """INSERT INTO """ + table_name + """ (""" + column_list + """) VALUES  """
        insert_string+= "( GETDATE(), "+str(number_of_parts)+", "+"'"+str(comment)+"'"+")"


        self.crsr.execute(insert_string)


    def createTable_MachineLog(self):
        """

        """
        schema_name = "log"
        table_name = "machine"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            machineID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            type INT FOREIGN KEY REFERENCES enum.machine(id),
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""
        self.crsr.execute(s)

    def getLastID(self,table_name):
        """

        :param table_name:
        :return:
        """
        s="""SELECT IDENT_CURRENT(""" +"'"+table_name +"'" +") AS ID"
        sql_query = pd.read_sql_query(s, self.cnxn)
        return int(sql_query['ID'][0])

    def createTable_MachineTimeLog(self):
        """

        """
        schema_name = "log"
        table_name = "machine_time"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            machineID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            time FLOAT,
                            type INT FOREIGN KEY REFERENCES enum.machine(id),
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""

        self.crsr.execute(s)

    def createTable_MachineEnum(self):
        """

        """
        schema_name = "enum"
        table_name = "machine"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            machine_enum VARCHAR (50) NOT NULL,  
                                                      
                        );"""
        self.crsr.execute(s)

    def createSchema_enum(self):
        """

        """
        schema_name = "enum"
        self.crsr.execute("""IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = """ + "'" + schema_name + "'" + """ ) 
                                BEGIN

                                EXEC( 'CREATE SCHEMA """ + schema_name + """' );
                            END
                            """)

    def insertTable_MachineEnum(self):
        """

        """
        schema_name = "enum"
        table_name = "machine"
        sql_query = pd.read_sql_query("""SELECT * FROM """+schema_name+"."+table_name, self.cnxn)

        if sql_query.shape[0]==0:

            column_list = """ machine_enum """

            insert_string = """INSERT INTO """ + schema_name + "." + table_name + """ (""" + column_list + """) VALUES  """
            i=0
            for element in Machine_Enum:
                if i!=len(Machine_Enum)-1:
                    insert_string += "( "+"'"+element.value+"'" +" )" + ","
                else:
                    insert_string += "( " +"'"+ element.value+"'" + " )"
                i+=1

            self.crsr.execute(insert_string)



    def createTable_TransportLog(self):
        """

        """
        schema_name = "log"
        table_name = "transport"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            transportID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            type VARCHAR (50) NOT NULL,
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""
        self.crsr.execute(s)

    def createTable_TransportTimeLog(self):
        """

        """
        schema_name = "log"
        table_name = "transport_time"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            transportID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            time FLOAT,
                            type VARCHAR (50) NOT NULL,
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""

        self.crsr.execute(s)

    def createTable_QueueLog(self):
        """

        """
        schema_name = "log"
        table_name = "queue"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            queueID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,          
                            run_id INT FOREIGN KEY REFERENCES run(id)                 
                        );"""
        self.crsr.execute(s)

    def createTable_QueueTimeLog(self):
        """

        """
        schema_name = "log"
        table_name = "queue_time"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            queueID VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            time FLOAT,
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""

        self.crsr.execute(s)

    def createTable_AllProductFinishedLog(self):
        """

        """
        schema_name = "log"
        table_name = "all_product_finished"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            product_id VARCHAR (50) NOT NULL,
                            start_time FLOAT,
                            finished_time FLOAT,
                            product_type VARCHAR (50) NOT NULL,
                            production_time FLOAT   ,
                            run_id INT FOREIGN KEY REFERENCES run(id)                                          
                        );"""
        self.crsr.execute(s)

    def createTable_ProductFinishedTimeLog(self):
        """

        """
        schema_name = "log"
        table_name = "product_finished_time"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            product_type_id VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,
                            time FLOAT,
                            run_id INT FOREIGN KEY REFERENCES run(id)
                        );"""

        self.crsr.execute(s)

    def createTable_ProductFinishedLog(self):
        """

        """
        schema_name = "log"
        table_name = "product_finished"
        s="""IF (NOT EXISTS (SELECT * 
                         FROM INFORMATION_SCHEMA.TABLES 
                         WHERE TABLE_SCHEMA = """+"'"+schema_name+"'"+ \
                        """AND  TABLE_NAME = """+"'"+table_name+"'"+"""))
                         CREATE TABLE """+schema_name+"."+table_name+""" (
                            id INT PRIMARY KEY IDENTITY (1, 1),
                            product_type_id VARCHAR (50) NOT NULL,
                            kpi_value FLOAT,   
                            run_id INT FOREIGN KEY REFERENCES run(id)                         
                        );"""

        self.crsr.execute(s)


    def close(self):
        """

        """
        self.crsr.close()
        self.cnxn.close()



