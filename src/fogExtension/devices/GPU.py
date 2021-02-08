from fogExtension.devices.GenericHardware import GenericDevice


class GPU(GenericDevice):
    """
        GPU node class, used for graphical or neural networks computation.


    """
    def __init__(self, freq, pm, cuda, mem_freq, tmu=1, tensor_cores=1, ram=4000):
        """

        Args:
            cuda (int) : hardware parallelization level,
            tmu (int) : texture mapping units,
            mem_freq (float) : memory communication frequency,
            tensor_cores (int) : number of cores used for tensor operations

        """
        super().__init__(freq, pm, ram)
        self.cuda_cores = cuda
        self.tmu = tmu
        self.mem_freq = mem_freq
        self.tensor_cores = tensor_cores
        self._compute_ipt()

    def jsonify(self):
        """

        Returns: jsonified GPU object

        """
        json_string = super(GPU, self).jsonify()
        json_string["type"] = "GPU"
        json_string["c_tot"] = self.cuda_cores
        json_string["c_available"] = self.cuda_cores
        json_string["tmu"] = self.tmu
        json_string["tensor_cores"] = self.tensor_cores
        json_string["mem_freq"] = self.mem_freq
        return json_string

    def _compute_ipt(self):
        """
        It computes the IPT depending on the cuda _ores, tensor_cores,the device frequency, tmu and the memory frequency.
        """
        texture_filler_rate = self.freq * self.tmu
        tensor_op_rate = self.tensor_cores * self.freq
        self.IPT = min(self.cuda_cores * texture_filler_rate, self.mem_freq, tensor_op_rate)  # finding the bottleneck

    @staticmethod
    def recompute_ipt(active_cuda_cores, active_tensor_cores, freq, tmu, mem_freq):
        """
        Static function used at simulation runtime in order to recompute the IPT parameter when changing the cuda _ores,
        tensor_cores,the device frequency, tmu and the memory frequency.

        Args:
            active_cuda_cores (int) : hardware parallelization level,
            tmu (int) : texture mapping units,
            mem_freq (float) : memory communication frequency,
            active_tensor_cores (int) : number of cores used for tensor operations,
            freq (float) : operating frequency of the device

        Returns:
            the recomputed IPT

        """
        texture_filler_rate = freq * tmu
        tensor_op_rate = active_tensor_cores * freq
        return min(active_cuda_cores * texture_filler_rate, mem_freq, tensor_op_rate)
