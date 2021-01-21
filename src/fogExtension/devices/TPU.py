from fogExtension.devices.GenericHardware import GenericDevice


class TPU(GenericDevice):
    """
        TPU node class, tensor processing unit are accelerators designed for neural networks computation.
    """
    def __init__(self, freq, tensor_cores, pm, ram=4000):
        """

        Args:
            tensor_cores (int): number of cores used for tensor operations

        """
        super().__init__(freq, pm, ram)
        self.tensor_cores = tensor_cores
        self._compute_ipt()

    def jsonify(self):
        """

        Returns: jsonified TPU object

        """
        json_string = super(TPU, self).jsonify()
        json_string["type"] = "TPU"
        json_string["tensor_cores"] = self.tensor_cores
        return json_string

    def _compute_ipt(self):
        """
        It computes the IPT depending on the tensor_cores and the device frequency.
        """
        self.IPT = self.freq * self.tensor_cores

    @staticmethod
    def recompute_ipt(active_tensor_cores, freq):
        """
        Static function used at simulation runtime in order to recompute the IPT parameter when changing the
        tensor_cores and the device frequency.

        Args:
            active_tensor_cores (int): number of cores used for tensor operations,
            freq (float) : operating frequency of the device

        Returns:
            the recomputed IPT

        """
        return active_tensor_cores * freq
