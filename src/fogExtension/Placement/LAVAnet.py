from math import ceil

from fogExtension.devices.CPU import CPU
from yafs.placement import Placement


class LAVANET(Placement):
    """
        This implementation locates the services accordingly to the LAVANET algorithm descibed in the work of dott. Filippo Sciamanna.
        A set of metrics has been included in protected field for computation purposes.
        Args:
            name: name of the application to be simulated
            app_params: dictionary containing the custom parameters of the application modules
    """
    def __init__(self, name, app_params):

        super(LAVANET, self).__init__(name)
        self.assignments = []
        self.app_params = app_params

    def _compute_load(self, device):
        '''
        Calculates the load of a device from the ratio between available and total cores.
        Args:
            device: device on which the load must be computed

        Returns: the current load percentage

        '''
        load = (1.0 - device["c_available"] / device["c_tot"]) * 100.0
        if load == 0:
            return 0
        elif load <= 10:
            return 10
        elif load <= 25:
            return 25
        elif load <= 50:
            return 50
        elif load <= 75:
            return 75
        return 100

    def _compute_latency(self, task, task_name, device):
        '''
        Calculates the latency of a  task scheduled on a device.
        Args:
            task: task on which the latency must be computed
            task_name: name of the task
            device: device on which the latency must be computed

        Returns: the calculated latency

        '''
        load = str(self._compute_load(device))
        latency = self.app_params["_load_lat"][device["name"]][task_name][load] * (1-task["n"] * self.app_params["_beta"][device["type"]])

        # LAVA implementation ends here, the next part is the net extension
        if device["wireless"] == 1:
            count = 1
            for a in self.assignments:
                if a["device"] == device:
                    count += 1
            wireless_value = task["data_in"] / device["BW_down"] + task["data_out"] / device["BW_up"]
            latency += count * wireless_value
        return latency

    def _compatibility_check(self, device, task, task_name):
        '''
                Compute whether the device and the task are compatible in terms of features
                Args:
                    task: task
                    task_name: name of the task
                    device: device
                Returns: boolean value
        '''
        if device["c_available"] * 100 >= self.app_params["_creq"][device["name"]][task_name]:
            if device["video"] >= task["video"] and device["screen"] >= task["screen"]:
                return True
        return False

    def _allocate_cores(self, device, task_name):
        '''
            Allocates the cores on the device accordingly to the task to be allocated and recomputes the IPT.
            Args:
                task_name: name of the task
                device: device
        '''
        core_to_remove = ceil(self.app_params["_creq"][device["name"]][task_name] / 100)
        device["c_available"] -= core_to_remove
        if device["type"] == "CPU":
            device["IPT"] = CPU.recompute_ipt(active_cores=device["c_available"], active_threads=device["threads"], freq=device["freq"])

    def _find_best_device_on_taskname(self, sim, task_name):
        '''
            Insert inside the assignment array the best device with respect to the task name.
            Args:
                sim: simulation YAFS class
                task_name: name of the task
        '''
        module = self.app_params["_task_param"][task_name]
        min_d_cost = -1
        for dev in sim.topology.G.nodes():
            d = sim.topology.G.nodes[dev]
            d["id"] = dev
            r_cost = 0
            if self._compatibility_check(d, module, task_name):
                r_cost = self._compute_latency(module, task_name, d)
                if min_d_cost <= 0 or r_cost < min_d_cost:
                    min_d_cost = r_cost

                    # adding/updating the scheduled activity
                    if len(self.assignments) == 0 or self.assignments[len(self.assignments) - 1]["task"] != module:
                        self.assignments.append({"task": module, "device": d})
                    else:
                        self.assignments[len(self.assignments) - 1]["device"] = d
        if min_d_cost == -1:
            Exception("Cannot allocate the module " + task_name + " on this network.")

    def initial_allocation(self, sim, app_name):
        '''
            Function called at the beginning of the simulation that allocates all the application module to the best devices.
            Args:
                sim: simulation YAFS class
                app_name: name of the application to be allocated
        '''
        app = sim.apps[app_name]

        services = app.services

        for task_name, m in services.items():
            self._find_best_device_on_taskname(sim=sim, task_name=task_name)
            curr_device = self.assignments[len(self.assignments) - 1]["device"]
            self._allocate_cores(device=curr_device, task_name=task_name)
            idDES = sim.deploy_module(app_name, task_name, m, [curr_device["id"]])

    def source_allocation(self, sim, task_name):
        '''
            Function called before the simulation that allocates all the source module to the best devices.
            Args:
                sim: simulation YAFS class
                task_name: name of the source task to be allocated
        '''
        self._find_best_device_on_taskname(sim=sim, task_name=task_name)
        device = self.assignments[len(self.assignments) - 1]["device"]
        self._allocate_cores(device=device, task_name=task_name)
        return device["id"]
