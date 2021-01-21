from fogExtension.devices.GenericHardware import GenericDevice


class FPGA(GenericDevice):
    """
        FPGA node class, used for specific applications. It is defined by:
        lut (int) : number of look-up tables,
        ff (int) : number of flip-flops

    """
    def __init__(self, freq, lut, ff, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.lut = lut
        self.ff = ff
        self._compute_ipt()

    def jsonify(self):
        json_string = super(FPGA, self).jsonify()
        json_string["type"] = "FPGA"
        json_string["lut"] = self.lut
        json_string["ff"] = self.ff
        return json_string

    def _compute_ipt(self):
        self.IPT = self.freq
