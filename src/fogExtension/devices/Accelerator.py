from fogExtension.devices.GenericHardware import GenericDevice


class Accelerator(GenericDevice):
    """
        Generic accelerator node class, used for generical purpose computation, it can be categorized with the
        purpose parameter. It is defined by:
        exec_units (int) : number of execution units,
        purpose (str) : acceleration purpose, this parameter can be customized in order to create a custom accelerator
        for a specific function
    """
    def __init__(self, freq, exec_units, purpose, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.exec_units = exec_units
        self.purpose = purpose
        self._compute_ipt()

    def jsonify(self):
        jsonString = super(Accelerator, self).jsonify()
        jsonString["type"] = "Accelerator"
        jsonString["exec_units"] = self.exec_units
        jsonString["purpose"] = self.purpose
        return jsonString

    def _compute_ipt(self):
        self.IPT = self.exec_units * self.freq
