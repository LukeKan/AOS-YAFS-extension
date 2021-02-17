from fogExtension.power.PowerModel import PowerModel


class Battery(PowerModel):
    def __init__(self, en_throughput, ppi, size):
        super(Battery, self).__init__(en_throughput, ppi)
        self._battery_power = size
        self.charge = size
        return

    def discharge(self, amount):
        self.charge -= amount

    def recharge(self):
        self.charge = self._battery_power

    def jsonify(self):
        json_string = super(Battery, self).jsonify()
        json_string["type"] = "Battery"
        json_string["battery_power"] = self._battery_power
        json_string["charge"] = self.charge
        json_string["en_budget"] = self._battery_power
        return json_string
