from fogExtension.devices.GenericHardware import GenericDevice


class TPU(GenericDevice):
    """
        TPU node class, tensor processing unit are accelerators designed for neural networks computation.
        It is defined by:

        RAM (int) : the ram parameters represent the actual TPU local unified buffer size for activation,
        MMU (int) : matrix multiply units,
        accumulators (int) : units for accumulating convolution results and aggregating matrix multiplication results

    """
    def __init__(self, freq, tensor_cores, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.tensor_cores = tensor_cores
        self._compute_ipt()

    def jsonify(self):
        json_string = super(TPU, self).jsonify()
        json_string["type"] = "TPU"
        json_string["tensor_cores"] = self.tensor_cores
        return json_string

    def _compute_ipt(self):
        self.IPT = self.freq * self.tensor_cores

    @staticmethod
    def recompute_ipt(active_tensor_cores, freq):
        return active_tensor_cores * freq
