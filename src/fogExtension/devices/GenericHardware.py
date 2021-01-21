class GenericDevice:
    """
    Base abstract class of a generic device with its mandatory parameters.
    """

    def __init__(self, freq, pm, ram=4):
        """
        Generic definition of mandatory parameters and power model.

        Args:
                freq (float): frequency of the device in MHz,
                ram (int): memory size of the device in MB, it is a constant set at 4 (default value),
                pm (PowerModel) : defines the power-model of the device [Wired, Battery, Solar]
        """
        self.pm = pm
        self.freq = freq
        self.ram = ram

    def jsonify(self):
        """

        Returns: jsonified GenericHardware object

        """
        return {"IPT": self.IPT,
                "RAM": self.ram,
                "PM": self.pm.jsonify()
                }

    def _compute_ipt(self):
        """
        It computes the IPT depending on the specific device feature
        Function to be overridden.
        """
        return

    @staticmethod
    def recompute_ipt(**params):
        """
        It recomputes the ipt given a set of parameters.
        Function to be overridden.
        Returns: None

        """
        return
