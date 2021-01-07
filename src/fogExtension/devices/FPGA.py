from fogExtension.devices.GenericDevice import GenericDevice


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
        jsonString = super(FPGA, self).jsonify()
        jsonString["type"] = "FPGA"
        jsonString["lut"] = self.lut
        jsonString["ff"] = self.ff
        return jsonString

    def _compute_ipt(self):
        self.IPT = self.freq
