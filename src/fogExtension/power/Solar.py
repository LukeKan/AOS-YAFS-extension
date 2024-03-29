from fogExtension.power.PowerModel import PowerModel


class Solar(PowerModel):
    def __init__(self, en_throughput, ppi, solar_power, battery, react_coeff):
        super(Solar, self).__init__(en_throughput, ppi)
        self._solar_power = solar_power
        self._battery_power = battery
        self._react_coeff = react_coeff
        self._compute_power()

    def regulate(self, react_coeff):
        self._react_coeff = react_coeff
        self._compute_power()

    def _compute_power(self):
        self._power = self._solar_power + self._react_coeff * self._battery_power

    def get_power(self):
        return self._power

    def jsonify(self):
        json_string = super(Solar, self).jsonify()
        json_string["type"] = "Solar"
        json_string["battery_power"] = self._battery_power
        json_string["solar_power"] = self._solar_power
        json_string["react_coeff"] = self._react_coeff
        json_string["en_budget"] = self.get_power()
        return json_string
