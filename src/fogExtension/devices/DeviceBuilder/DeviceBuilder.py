from fogExtension.devices.CPU import CPU
from fogExtension.devices.GPU import GPU
from fogExtension.power.Wired import Wired


class DeviceBuilder:

    @staticmethod
    def wired_freescale():
        fs = CPU(freq=1200.0, pm=Wired(1, 10000), cores=4)
        freescale_cpu = fs.jsonify()
        freescale_cpu["video"] = 1
        freescale_cpu["screen"] = 1
        freescale_cpu["s"] = 0
        freescale_cpu["cpu_tot"] = 400
        freescale_cpu["name"] = "FREESCALE"
        freescale_cpu["wireless"] = 0
        return freescale_cpu

    @staticmethod
    def wired_jetson_cpu():
        jetson_pm = Wired(1, 1000)
        fs = CPU(freq=2000.0, pm=jetson_pm, cores=4)
        jetson_cpu = fs.jsonify()
        jetson_cpu["video"] = 0
        jetson_cpu["screen"] = 0
        jetson_cpu["s"] = 0
        jetson_cpu["cpu_tot"] = 400
        jetson_cpu["name"] = "JETSON_CPU"
        jetson_cpu["wireless"] = 0
        return jetson_cpu, jetson_pm

    @staticmethod
    def wired_jetson_full():
        jetson_cpu, jetson_pm = DeviceBuilder.wired_jetson_cpu()
        fs = GPU(freq=2000.0, pm=jetson_pm, cuda=256, mem_freq=2000.0)
        jetson_gpu = fs.jsonify()
        jetson_gpu["video"] = 0
        jetson_gpu["screen"] = 0
        jetson_gpu["s"] = 1
        jetson_gpu["cpu_tot"] = 400
        jetson_gpu["name"] = "JETSON_GPU"
        jetson_gpu["wireless"] = 0
        return jetson_cpu, jetson_gpu

    @staticmethod
    def wired_odroid():
        fs = CPU(freq=2500.0, pm=Wired(1, 1000), cores=4)
        odroid_cpu = fs.jsonify()
        odroid_cpu["video"] = 0
        odroid_cpu["screen"] = 1
        odroid_cpu["s"] = 0
        odroid_cpu["cpu_tot"] = 400
        odroid_cpu["name"] = "ODROID"
        odroid_cpu["wireless"] = 0
        return odroid_cpu
