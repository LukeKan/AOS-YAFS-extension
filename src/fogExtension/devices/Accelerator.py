from fogExtension.devices.GenericHardware import GenericDevice


class Accelerator(GenericDevice):
    """
        Generic accelerator node class, used for generical purpose computation, it can be categorized with the
        purpose parameter.
    """
    def __init__(self, freq, exec_units, purpose, pm, ram=4000):
        """

        Args:
            exec_units (int) : number of execution units,
            purpose (str) : acceleration purpose, this parameter can be customized in order to create a custom accelerator
                for a specific function

        """
        super().__init__(freq, pm, ram)
        self.exec_units = exec_units
        self.purpose = purpose
        self._compute_ipt()

    def jsonify(self):
        """

        Returns: jsonified Accelerator object

        """
        json_string = super(Accelerator, self).jsonify()
        json_string["type"] = "Accelerator"
        json_string["exec_units"] = self.exec_units
        json_string["purpose"] = self.purpose
        return json_string

    def _compute_ipt(self):
        """
        It computes the IPT depending on the frequency and execution units of the device.
        """
        self.IPT = self.exec_units * self.freq

    @staticmethod
    def recompute_ipt(actual_exec_units, freq):
        """
        Static function used at simulation runtime in order to recompute the IPT parameter when changing the execution
        units and the device frequency.

        Args:
            actual_exec_units (int) : number of execution units,
            freq (float) : operating frequency of the device

        Returns:
            the recomputed IPT

        """
        return actual_exec_units * freq
