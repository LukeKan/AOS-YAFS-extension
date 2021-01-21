from fogExtension.devices.GenericHardware import GenericDevice


class FPGA(GenericDevice):
    """
        FPGA node class, used for specific applications. It is defined by:
    """
    def __init__(self, freq, lut, ff, pm, ram=4000):
        """

        Args:
            lut (int) : number of look-up tables,
            ff (int) : number of flip-flops

        """
        super().__init__(freq, pm, ram)
        self.lut = lut
        self.ff = ff
        self._compute_ipt()

    def jsonify(self):
        """

        Returns: jsonified FPGA object

        """
        json_string = super(FPGA, self).jsonify()
        json_string["type"] = "FPGA"
        json_string["lut"] = self.lut
        json_string["ff"] = self.ff
        return json_string

    def _compute_ipt(self):
        """
        It computes the IPT depending on the frequency of the FPGA.
        """
        self.IPT = self.freq

    @staticmethod
    def recompute_ipt(freq):
        """
        Static function used at simulation runtime in order to recompute the IPT parameter when changing the device
        frequency. Currently, the function is useless but it has been implemented only for further possible
        modifications.

        Args:
            freq (float) : operating frequency of the device

        Returns:
            the recomputed IPT

        """
        return freq
