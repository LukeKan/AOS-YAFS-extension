"""
    In this simulation, the device topology is meshed and the video-surveillance scenario is implemented.


    @author: Isaac Lera
"""
import os
import time
import json
import random
import logging.config

import networkx as nx
from pathlib import Path

from yafs.population import Statical

from fogExtension.Placement.LAVAnet import LAVANET
from fogExtension.devices.CPU import CPU
from fogExtension.devices.GPU import GPU
from fogExtension.power.Wired import Wired
from yafs.core import Sim
from yafs.application import create_applications_from_json, Application, Message, fractional_selectivity
from yafs.topology import Topology

from yafs.placement import JSONPlacement
from yafs.path_routing import DeviceSpeedAwareRouting
from yafs.distribution import deterministic_distribution,deterministicDistributionStartPoint
from collections import defaultdict




class CustomStrategy():

    def __init__(self,pathResults):
        self.activations = 0
        self.pathResults = pathResults

    def deploy_module(self,sim,service,node):
        app_name = int(service[0:service.index("_")])
        app = sim.apps[app_name]
        services = app.services
        idDES = sim.deploy_module(app_name, service, services[service], [node])
        # with this `identifier of the DES process` (idDES) you can control it

    def undeploy_module(self,sim,service,node):
        app_name = int(service[0:service.index("_")])
        des = sim.get_DES_from_Service_In_Node(node, app_name, service)
        sim.undeploy_module(app_name, service,des)

    def is_already_deployed(self,sim,service_name,node):
        app_name = service_name[0:service_name.index("_")]

        all_des = []
        for k, v in sim.alloc_DES.items():
            if v == node:
                all_des.append(k)

        # Clearing other related structures
        for des in sim.alloc_module[int(app_name)][service_name]:
            if des in all_des:
                return True


    def get_current_services(self,sim):
        """ returns a dictionary with name_service and a list of node where they are deployed
        example: defaultdict(<type 'list'>, {u'2_19': [15], u'3_22': [5]})
        """
        # it returns all entities related to a node: modules, sources/users, etc.
        current_services = sim.get_alloc_entities()
        # here, we only need modules (not users)
        current_services = dict((k, v) for k, v in current_services.items() if len(v)>0)
        deployed_services = defaultdict(list)
        for node,services in current_services.items():
            for service_name in services:
                if not "None" in service_name:
                     deployed_services[service_name[service_name.index("#")+1:]].append(node)


        return deployed_services


    def __call__(self, sim, routing):
        logging.info("Activating Custom process - number %i " % self.activations)
        self.activations += 1
        routing.invalid_cache_value = True # when the service change the cache of the Path.routing is outdated.

        # Current deployed services
        # print("Current deployed services> module:list(nodes)")
        current_services = self.get_current_services(sim)
        # print(current_services)

        # We move all the service to other random node
        for service in current_services:
            for currentNode in current_services[service]:
                newNode = random.sample(sim.topology.G.nodes(),1)[0]
                if not self.is_already_deployed(sim,service,newNode):
                    self.undeploy_module(sim,service,currentNode)
                    self.deploy_module(sim,service,newNode)
                    logging.info("Moving Service %s from %s to %s node"%(service,currentNode,newNode))

def fractional_selectivity(threshold):
    return random.random() <= threshold

def create_application():
    # APPLICATION
    a = Application(name="SmartSurveillance")

    modules = [
        {"MOTION_KERNEL": {"RAM": 10,"Type": "SOURCE"}}, #"video": 1, "screen": 0, "s": 1, "n": 0, "data_in": 0, "data_out": 519252}},
        {"CLASSIFIER_KERNEL": {"RAM": 10, "Type": "MODULE"}},# "video": 0, "screen": 0, "s": 1, "n": 1, "data_in": 519368, "data_out": 44}},
        {"TRACKER_KERNEL": {"RAM": 10, "Type": "MODULE"}},#, "video": 0, "screen": 0, "s": 0, "n": 0, "data_in": 519252, "data_out": 1038700}},
        {"GUI_KERNEL": {"Type": "SINK"}}#, "video": 0, "screen": 1, "s": 0, "n": 0, "data_in": 519376, "data_out": 0}}
    ]
    a.set_modules(modules)
    """
    Messages among MODULES (AppEdge in iFogSim)
    """
    m_mot_track = Message("M.M_T", "MOTION_KERNEL", "TRACKER_KERNEL", instructions=200*10 ^ 8, bytes=100000)
    m_track_class = Message("M.T_C", "TRACKER_KERNEL", "CLASSIFIER_KERNEL", instructions=300*10 ^ 8, bytes=50000)
    m_track_gui = Message("M.T_G", "TRACKER_KERNEL", "GUI_KERNEL", instructions=200 * 10 ^ 8, bytes=100000)
    m_class_gui = Message("M.C_G", "CLASSIFIER_KERNEL", "GUI_KERNEL", instructions=300 * 10 ^ 8, bytes=50000)

    """
    Defining which messages will be dynamically generated # the generation is controlled by Population algorithm
    """
    a.add_source_messages(m_mot_track)

    """
    MODULES/SERVICES: Definition of Generators and Consumers (AppEdges and TupleMappings in iFogSim)
    """
    # MODULE SERVICES
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
    a.add_service_module(module_name="TRACKER_KERNEL", message_in=m_mot_track, message_out=m_track_class, distribution=fractional_selectivity, threshold=1.0
                         )
    a.add_service_module(module_name="TRACKER_KERNEL", message_in=m_mot_track, message_out=m_track_gui, distribution=fractional_selectivity, threshold=1.0
                         )
    a.add_service_module(module_name="CLASSIFIER_KERNEL", message_in=m_track_class, message_out=m_class_gui, distribution=fractional_selectivity, threshold=1.0
                         )
    a.add_service_module(module_name="GUI_KERNEL", message_in=m_class_gui, distribution=fractional_selectivity, threshold=1.0
                         )

    a.add_service_source(module_name="MOTION_KERNEL", distribution=dDistribution, message=m_mot_track, module_dest=["TRACKER_KERNEL"]) #module_name="MOTION_KERNEL", distribution=fractional_selectivity(1.0), message=m_mot_track, module_dest=["TRACKER_KERNEL"],


    return a


def main(stop_time, it):

    folder_results = Path("results/")
    folder_results.mkdir(parents=True, exist_ok=True)
    folder_results = str(folder_results)+"/"

    """
    DEVICES DEFINITION
    Values are taken from the thesis work of dott. Filippo Sciamanna, chapter 6.1
    """
    free_scale = CPU(freq=1200.0, pm=Wired(1, 10000), cores=4)

    jetson_pm = Wired(1, 1000)
    jetson_cpu_1 = CPU(freq=2000.0, pm=jetson_pm, cores=4)
    jetson_gpu_1 = GPU(freq=2000.0, pm=jetson_pm, cuda=256, mem_freq=2000.0)

    odroid_cpu_1 = CPU(freq=2500.0, pm=Wired(1, 1000), cores=4)




    """
    TOPOLOGY
    """
    t = Topology()
    t.G = nx.complete_graph(10)
    attPR_BW = {x: 10000 for x in t.G.edges()}
    nx.set_edge_attributes(t.G, name="PR", values=attPR_BW)
    nx.set_edge_attributes(t.G, name="BW", values=attPR_BW)

    nodes_params = {}
    for x in range(0, 10):
        fs = CPU(freq=1200.0, pm=Wired(1, 10000), cores=4)
        fs_json = fs.jsonify()
        fs_json["video"] = 1
        fs_json["screen"] = 1
        fs_json["s"] = 0
        fs_json["cpu_tot"] = 400
        fs_json["name"] = "FREESCALE"
        fs_json["wireless"] = 0
        nodes_params[x] = fs_json
    nx.set_node_attributes(t.G, values=nodes_params)
    # print(t.G.nodes())
    # print(t.G.edges())

    """
    APPLICATION or SERVICES
    """
    apps = [create_application()]

    """
   PLACEMENT algorithm
   """
    placement = LAVANET(name="LAVANET")  # it defines the deployed rules: module-device
    placement.scaleService({"TRACKER_KERNEL": 1, "CLASSIFIER_KERNEL": 1})

    """
    POPULATION algorithm
    """
    # In ifogsim, during the creation of the application, the Sensors are assigned to the topology, in this case no. As mentioned, YAFS differentiates the adaptive sensors and their topological assignment.
    # In their case, the use a statical assignment.
    pop = Statical("Statical")
    # For each type of sink modules we set a deployment on some type of devices
    # A control sink consists on:
    #  args:
    #     model (str): identifies the device or devices where the sink is linked
    #     number (int): quantity of sinks linked in each device
    #     module (str): identifies the module from the app who receives the messages
    pop.set_sink_control({"model": "a", "number": 1, "module": apps[0].get_sink_modules()})

    # In addition, a source includes a distribution function:
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
    pop.set_src_control(
       {"model": "sensor-s", "number": 1, "message": apps[0].get_message("M.M_T"), "distribution": dDistribution})


    """
    Defining ROUTING algorithm to define how path messages in the topology among modules
    """
    selectorPath = DeviceSpeedAwareRouting()

    """
    SIMULATION ENGINE
    """
    s = Sim(t, default_results_path=folder_results+"sim_trace")
    # s.topology.load_all_node_attr(nodes_params)

    """
    Deploy services == APP's modules
    """
    for a in apps:
        s.deploy_app(a, placement, selectorPath)  # Note: each app can have a different routing algorithm
        s.deploy_source("SmartSurveillance", placement.lavanet_allocation_source(s, "MOTION_KERNEL"), a.get_message("M.M_T"), dDistribution)
    """
    RUNNING - last step
    """
    logging.info(" Performing simulation: %i " % it)
    s.run(stop_time)  # To test deployments put test_initial_deploy a TRUE



if __name__ == '__main__':

    logging.config.fileConfig(os.getcwd() + '/logging.ini')

    nIterations = 5  # iteration for each experiment
    simulationDuration = 100000

    # Iteration for each experiment changing the seed of randoms
    for iteration in range(nIterations):
        random.seed(iteration)
        logging.info("Running experiment it: - %i" % iteration)

        start_time = time.time()
        main(stop_time=simulationDuration,
             it=iteration)

        print("\n--- %s seconds ---" % (time.time() - start_time))

    print("Simulation Done!")
