from fogExtension.devices.GenericHardware import GenericDevice


class TPU(GenericDevice):
    """
        TPU node class, tensor processing unit are accelerators designed for neural networks computation.
        It is defined by:

        RAM (int) : the ram parameters represent the actual TPU local unified buffer size for activation,
        MMU (int) : matrix multiply units,
        accumulators (int) : units for accumulating convolution results and aggregating matrix multiplication results

    """
    def __init__(self, freq, mmu, accumulators, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.mmu = mmu
        self.accumulators = accumulators
        self._compute_ipt()

    def jsonify(self):
        jsonString = super(TPU, self).jsonify()
        jsonString["type"] = "TPU"
        jsonString["MMU"] = self.mmu
        jsonString["accumulators"] = self.accumulators
        return jsonString

    def _compute_ipt(self):
        self.IPT = self.freq
        # TODO
