from fogExtension.power.PowerModel import PowerModel


class Wired(PowerModel):
    def __init__(self, en_throughput, ppi):
        super(Wired, self).__init__(en_throughput, ppi)
        self._charged = True

    def toggle(self):
        self._charged = 1 - self._charged

    def is_plugged(self):
        return self._charged

    def jsonify(self):
        json_string = super(Wired, self).jsonify()
        json_string["type"] = "Wired"
        json_string["en_budget"] = 0
        return json_string
