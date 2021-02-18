"""
    In this simulation, the device topology is meshed and the video-surveillance scenario is implemented.


    @author: Luca Loria
"""
import json
import os
import time
import random
import logging.config

import networkx as nx
from pathlib import Path

from fogExtension.devices.DeviceBuilder.DeviceBuilder import DeviceBuilder

from fogExtension.Placement.LAVAnet import LAVANET
from yafs.core import Sim
from yafs.application import Application, Message, fractional_selectivity
from yafs.topology import Topology

from yafs.path_routing import DeviceSpeedAwareRouting
from yafs.distribution import deterministic_distribution


def fractional_selectivity(threshold):
    return random.random() <= threshold

def create_application():
    # APPLICATION
    a = Application(name="SmartSurveillance")

    modules = [
        {"MOTION_KERNEL": {"RAM": 10, "Type": "SOURCE"}},
        {"CLASSIFIER_KERNEL": {"RAM": 10, "Type": "MODULE"}},
        {"TRACKER_KERNEL": {"RAM": 10, "Type": "MODULE"}},
        {"GUI_KERNEL": {"Type": "SINK"}}
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
    a.add_service_module(module_name="TRACKER_KERNEL", message_in=m_mot_track, message_out=m_track_class, distribution=fractional_selectivity, threshold=1.0)
    a.add_service_module(module_name="TRACKER_KERNEL", message_in=m_mot_track, message_out=m_track_gui, distribution=fractional_selectivity, threshold=1.0)
    a.add_service_module(module_name="CLASSIFIER_KERNEL", message_in=m_track_class, message_out=m_class_gui, distribution=fractional_selectivity, threshold=1.0)
    a.add_service_module(module_name="GUI_KERNEL", message_in=m_class_gui, distribution=fractional_selectivity, threshold=1.0)
    # MODULE SOURCES
    a.add_service_source(module_name="MOTION_KERNEL", distribution=dDistribution, message=m_mot_track, module_dest=["TRACKER_KERNEL"])

    return a


def main(stop_time, it):

    folder_results = Path("results/")
    folder_results.mkdir(parents=True, exist_ok=True)
    folder_results = str(folder_results)+"/"

    """
    DEVICES DEFINITION
    Values are taken from the thesis work of dott. Filippo Sciamanna, chapter 6.1
    
    TOPOLOGY
    """
    t = Topology()
    t.G = nx.complete_graph(10)
    attPR_BW = {x: 10000 for x in t.G.edges()}
    nx.set_edge_attributes(t.G, name="PR", values=attPR_BW)
    nx.set_edge_attributes(t.G, name="BW", values=attPR_BW)

    nodes_params = {}
    for x in range(0, 8):
        freescale_cpu = DeviceBuilder.wired_freescale()
        freescale_cpu["wireless"] = (x + 1) % 2  # even id devices are wireless
        freescale_cpu["BW_down"] = 1 + (x % 5) * 10
        freescale_cpu["BW_up"] = 1 + (x % 5) * 20
        nodes_params[x] = freescale_cpu
    for x in range(8, 10):
        odroid_cpu = DeviceBuilder.wired_odroid()
        odroid_cpu["wireless"] = x % 2  # odd id devices are wireless
        odroid_cpu["BW_down"] = 1 + (x % 5) * 10
        odroid_cpu["BW_up"] = 1 + (x % 5) * 20
        nodes_params[x] = odroid_cpu
    nx.set_node_attributes(t.G, values=nodes_params)

    """
    APPLICATION or SERVICES
    """
    apps = [create_application()]

    """
    PLACEMENT algorithm
    """
    params = json.load(open('data/params.json'))
    placement = LAVANET(name="LAVANET", app_params=params)  # it defines the deployed rules: module-device
    placement.scaleService({"TRACKER_KERNEL": 1, "CLASSIFIER_KERNEL": 1})

    """
    Defining ROUTING algorithm to define how path messages in the topology among modules
    """
    selectorPath = DeviceSpeedAwareRouting()

    """
    SIMULATION ENGINE
    """
    s = Sim(t, default_results_path=folder_results+"sim_trace")

    """
    Deploy services == APP's modules
    """
    dDistribution = deterministic_distribution(name="Deterministic", time=100)
    for a in apps:
        s.deploy_app(a, placement, selectorPath)  # Note: each app can have a different routing algorithm
        s.deploy_source("SmartSurveillance", placement.source_allocation(s, "MOTION_KERNEL"), a.get_message("M.M_T"), dDistribution)
    """
    RUNNING - last step
    """
    logging.info(" Performing simulation: %i " % it)
    s.run(stop_time)


if __name__ == '__main__':

    logging.config.fileConfig(os.getcwd() + '/logging.ini')

    nIterations = 1  # iteration for each experiment
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
