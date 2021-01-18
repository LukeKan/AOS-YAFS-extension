from fogExtension.devices.Accelerator import Accelerator
from fogExtension.devices.CPU import CPU
from fogExtension.devices.FPGA import FPGA
from fogExtension.devices.GPU import GPU
from fogExtension.devices.TPU import TPU
from fogExtension.power.Battery import Battery
from fogExtension.power.Solar import Solar
from fogExtension.power.Wired import Wired

battery_model = Battery(1.0, 10, 8000)
solar_model = Solar(1.0, 5, 7000, 8000, 0.5)
wired_model = Wired(1.0, 7)

cpu_batt = CPU(5.2, battery_model)
gpu_wired = GPU(30.8, 40, 20, 40.5, 8, wired_model)
fpga_solar = FPGA(140.3, 200, 12, solar_model)
tpu_wired = TPU(202.3, 7, 5, wired_model)
acc_solar = Accelerator(167.7, 4, 'crypto', solar_model)

print("CPU TEST :" + str(cpu_batt.jsonify()))
print("GPU TEST :" + str(gpu_wired.jsonify()))
print("FPGA TEST :" + str(fpga_solar.jsonify()))
print("TPU TEST :" + str(tpu_wired.jsonify()))
print("Accelerator TEST :" + str(acc_solar.jsonify()))
assert True
