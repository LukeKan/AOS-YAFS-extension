from math import ceil

from fogExtension.devices.CPU import CPU
from yafs.placement import Placement


class LAVANET(Placement):
    """
        This implementation locates the services accordingly to the LAVANET algorithm descibed in the work of dott. ---.

        It only runs once, in the initialization.

    """
    def __init__(self, name):

        super().__init__(name)

        # self._load_lat is the e matrix
        self._load_lat = {
        "FREESCALE":
            {
                "MOTION_KERNEL":
                    {
                         "0": 210.18,
                         "10": 222.96,
                         "25": 242.29,
                         "50": 347.76,
                         "75": 678.24,
                         "100": 846.09
                    },
                "CLASSIFIER_KERNEL":
                     {
                         "0": 38881.97,
                         "10": 44136.19,
                         "25": 54469.3,
                         "50": 79937.4,
                         "75": 166112,
                         "100": 184479
                     },
                "TRACKER_KERNEL":
                    {
                        "0": 0.47,
                        "10": 0.47,
                        "25": 0.47,
                        "50": 0.49,
                        "75": 0.51,
                        "100": 0.91
                    },
                "GUI_KERNEL":
                    {
                        "0": 24.05,
                        "10": 24.47,
                        "25": 25.23,
                        "50": 27.12,
                        "75": 36.66,
                        "100": 50.31
                    }
            },
        "ODROID":
            {
                "MOTION_KERNEL":
                    {
                        "0": 54.04,
                        "10": 54.66,
                        "25": 56.33,
                        "50": 62.90,
                        "75": 88.80,
                        "100": 189.781
                    },
                "CLASSIFIER_KERNEL":
                    {
                        "0": 2022.62,
                        "10": 2292.45,
                        "25": 3034.47,
                        "50": 3984.49,
                        "75": 7764.74,
                        "100": 9687.35
                    },
                "TRACKER_KERNEL":
                    {
                        "0": 0.13,
                        "10": 0.1229,
                        "25": 0.1,
                        "50": 0.1,
                        "75": 0.1,
                        "100": 0.17
                    },
                "GUI_KERNEL":
                    {
                        "0": 5.19,
                        "10": 5.14,
                        "25": 4.96,
                        "50": 6.2604,
                        "75": 15.09,
                        "100": 23.74
                    }
            },
        "JETSON_CPU":
            {
                "MOTION_KERNEL":
                    {
                        "0": 19.18,
                        "10": 22.5,
                        "25": 30.61,
                        "50": 36.54,
                        "75": 41.2,
                        "100": 42.141
                    },
                "CLASSIFIER_KERNEL":
                    {
                        "0": 2932.62,
                        "10": 3310.68,
                        "25": 4130.79,
                        "50": 5001.77,
                        "75": 5933.91,
                        "100": 5770.17
                    },
                "TRACKER_KERNEL":
                    {
                        "0": 0.14,
                        "10": 0.14,
                        "25": 0.14,
                        "50": 0.14,
                        "75": 0.14,
                        "100": 0.16
                    },
                "GUI_KERNEL":
                    {
                        "0": 6.75,
                        "10": 6.78,
                        "25": 6.85,
                        "50": 7.23,
                        "75": 7.79,
                        "100": 16.08
                    }
            },
        "JETSON_GPU":
            {
                "MOTION_KERNEL":
                    {
                        "0": 10.01,
                        "10": 10.7,
                        "25": 10.8,
                        "50": 12.4,
                        "75": 17.8,
                        "100": 23
                    },
                "CLASSIFIER_KERNEL":
                    {
                        "0": 287,
                        "10": 215.22,
                        "25": 208,
                        "50": 208,
                        "75": 210,
                        "100": 226.8
                    },
                "TRACKER_KERNEL":
                    {
                        "0": 0.14,
                        "10": 0.14,
                        "25": 0.14,
                        "50": 0.14,
                        "75": 0.14,
                        "100": 0.16
                    },
                "GUI_KERNEL":
                    {
                        "0": 6.75,
                        "10": 6.78,
                        "25": 6.85,
                        "50": 7.23,
                        "75": 7.79,
                        "100": 16.08
                    }
            }
        }

        self._beta = {"CPU": 0.9, "GPU": 0.65}

        self._creq = {
            "FREESCALE":
                {
                    "MOTION_KERNEL": 250,
                    "CLASSIFIER_KERNEL": 250,
                    "TRACKER_KERNEL": 50,
                    "GUI_KERNEL": 150
                },
            "ODROID":
                {
                    "MOTION_KERNEL": 150,
                    "CLASSIFIER_KERNEL": 350,
                    "TRACKER_KERNEL": 50,
                    "GUI_KERNEL": 150
                },
            "JETSON_CPU":
                {
                    "MOTION_KERNEL": 350,
                    "CLASSIFIER_KERNEL": 250,
                    "TRACKER_KERNEL": 50,
                    "GUI_KERNEL": 150
                },
            "JETSON_GPU":
                {
                    "MOTION_KERNEL": 150,
                    "CLASSIFIER_KERNEL": 50,
                    "TRACKER_KERNEL": 1000,
                    "GUI_KERNEL": 1000
                }
        }

    def _compute_load(self, device):
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

    def _compute_latency(self, task, task_name, device, assignments):

        load = str(self._compute_load(device))
        latency = self._load_lat[device["name"]][task_name][load] * (1-task["n"] * self._beta[device["type"]])

        # LAVA implementation ends here, the next part is the net extension
        if device["wireless"] == 1:
            count = 0
            for a in assignments:
                if a["device"] == device:
                    count += 1
            wireless_value = task["data_in"] / device["BW_down"] + task["data_out"] / device["BW_up"]
            latency += count * wireless_value
        return latency

    def _compatibility_check(self, device, task, task_name):
        if device["c_available"] * 100 >= self._creq[device["name"]][task_name]:
            if device["video"] >= task["video"] and device["screen"] >= task["screen"]:# and device["s"] >= task["s"]:
                return True
        return False

    def _allocate_cores(self, device, task_name):
        core_to_remove = ceil(self._creq[device["name"]][task_name] / 100)
        device["c_available"] -= core_to_remove
        if device["type"] == "CPU":
            device["IPT"] = CPU.recompute_ipt(active_cores=device["c_available"], active_threads=device["threads"], freq=device["freq"])

    def initial_allocation(self, sim, app_name):
        app = sim.apps[app_name]

        services = app.services
        assignments = []
        for task_name, m in services.items():
            min_d_cost = -1
            for mod in m:
                module = mod["param"]["params"]
                for dev in sim.topology.G.nodes():
                    d = sim.topology.G.nodes[dev]
                    r_cost = 0
                    if self._compatibility_check(d, module, task_name):
                        r_cost = self._compute_latency(module, task_name, d, assignments)
                        if min_d_cost <= 0 or r_cost < min_d_cost:
                            min_d_cost = r_cost

                            # adding/updating the scheduled activity
                            if len(assignments) == 0 or assignments[len(assignments)-1]["task"] != module:
                                assignments.append({"task": mod, "device": d})
                            else:
                                assignments[len(assignments)-1]["device"] = d
                if min_d_cost == -1:
                    Exception("Cannot allocate the module "+module["name"]+" on this network.")
                curr_device = assignments[len(assignments) - 1]["device"]
                self._allocate_cores(device=curr_device, task_name=task_name)
                idDES = sim.deploy_module(app_name, task_name, services[task_name], curr_device)
