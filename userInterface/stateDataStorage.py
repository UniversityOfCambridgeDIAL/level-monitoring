#!/usr/bin/env python3

from opcua import Server, ua, uamethod
# from opcua.common.ua_utils import value_to_datavalue
# from opcua.ua.attribute_ids import AttributeIds
# from opcua.ua.uatypes import ValueRank
import time
from random import randint
import datetime
import csv
import socket

class ExtendedServer(Server):
    def __init__(self,port):
        super().__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip = s.getsockname()[0]
        s.close()
        self.url = "opc.tcp://" + str(ip) + ":" + str(port)
        self.set_endpoint(self.url)
        name = "opcua_simulation_server"
        self.addspace = self.register_namespace(name)
#         print("namespace is:", self.addspace)

def opcuaserver_settings(objectname = "Parameters" , variablename = "Variable"):
    global Temp
    node = server.get_objects_node()
#     print("node is:", node)
    param = node.add_object(server.addspace, objectname)
#     print("param is:",param)
    Temp = param.add_variable (server.addspace, variablename, 0)
    server.start()
    print("Server is started at {}".format(server.url))

class Communication:  #try to wrap
    def __init__(self, port=None):
        self.server = ExtendedServer(port)
    
    def opcuaserver_pub(self,objectname = "Parameters" , variablename = "Variable"):
        global Temp1
        node = self.server.get_objects_node()
#         print("node is:", node)
        param = node.add_object(self.server.addspace, objectname)
#         print("param is:",param)
        Temp1 = param.add_variable (self.server.addspace, variablename, 0)
        self.server.start()
        print("Server is started at {}".format(self.server.url))

def start():
    global Temp1, Temp2, Temp3, Temp4, Temp5, Temp6, Temp21, Temp22, Temp23, Temp24, myevgen, mysecondevgen 
    server = ExtendedServer(4840)
    node = server.get_objects_node()
#     print("node is:", node)
    param = node.add_object(server.addspace, "Parameters")
    param2 = node.add_object(server.addspace, "SensorReading")
#     print("param is:",param)
    Temp1 = param.add_variable (server.addspace, "Time stamp", 0)
    Temp2 = param.add_variable (server.addspace, "Item code", 0)
    Temp3 = param.add_variable (server.addspace, "Remaining stock", 0)
    Temp4 = param.add_variable (server.addspace, "Remaining stock trigger", 0)
    Temp5 = param.add_variable (server.addspace, "Expiry date", 0)
    Temp6 = param.add_variable (server.addspace, "Date created/updated", 0)
    Temp21 = param2.add_variable (server.addspace, "Sensor 1", 0)
    Temp22 = param2.add_variable (server.addspace, "Sensor 2", 0)
    Temp23 = param2.add_variable (server.addspace, "Sensor 3", 0)
    Temp24 = param2.add_variable (server.addspace, "Sensor 4", 0)
    # The custom event object automatically will have members from its parent (BaseEventType)
    etype = server.create_custom_event_type(server.addspace, 'MyEvent',
                                            ua.ObjectIds.BaseEventType,
                                            [('TimeStamp', ua.VariantType.String),
                                             ('ItemCode', ua.VariantType.String),
                                             ('RemainingStock', ua.VariantType.Double),
                                             ('RemainingStockTrigger', ua.VariantType.Double),
                                             ('ExpiryDate', ua.VariantType.String),
                                             ('DateCreatedUpdated', ua.VariantType.String)])
    myevgen = server.get_event_generator(etype, param)
    server.start()
    # enable history for myobj events; must be called after start since it uses subscription
    server.iserver.enable_history_event(param, period=None)
    # enable history for server events; must be called after start since it uses subscription
    server_node = server.get_node(ua.ObjectIds.Server)
    server.historize_node_event(server_node, period=None)
    print("Server is started at {}".format(server.url))
    
def write_csv(filename = None, **kwargs):
    if filename == None:
        print("File name not found.")
    else:
        time_stamp = datetime.datetime.now()
        with open(filename + ".csv" , 'a',newline='') as file:
            fields = [time_stamp, kwargs]
            writer = csv.writer(file)
            writer.writerow(fields)
        return 0
            
if __name__ == "__main__":
    print('state and data storage main')
    #try event
    start()
    count = 0
    while True:
        time.sleep(5)
        myevgen.event.Message = ua.LocalizedText("MyFirstEvent %d" % count)
        myevgen.event.Severity = count
        myevgen.event.MyNumericProperty = count
        myevgen.event.MyStringProperty = "Property " + str(count)
        myevgen.trigger()
        count += 1
        print(count)
    #***** try wrapper***
#     opc = Communication(port = 4840)
#     opc.opcuaserver_pub("test_para","test_var")

    #***** without wrapper***
    # server = ExtendedServer(4840)
    # opcuaserver_settings("test_para","test_var")

    # node = server.get_objects_node()
    # print("node is:", node)
    # param = node.add_object(server.addspace, "Parameters")
    # print("param is:",param)
    # Temp = param.add_variable (server.addspace, "Temperature", 0)
    # server.start()
    # print("Server is started at {}".format(server.url))

#     while True:  
#         Temperature = randint(10, 50)
#         print("Temperature:",Temperature)
#         Temp1.set_value(Temperature)
#         time.sleep(2)
