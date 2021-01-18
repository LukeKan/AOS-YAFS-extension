from fogExtension.devices.GenericHardware import GenericDevice


class GPU(GenericDevice):
    """
        GPU node class, used for graphical or neural networks computation. It is defined by:
        RAM (int) : the ram parameters represent the actual GPU internal memory size,
        cuda_cores (int) : hardware parallelization level,
        tmu (int) : texture mapping units,
        rop (int) : rendering output units

    """
    def __init__(self, freq, cuda, tmu,  mem_freq, tensor_cores, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.cuda_cores = cuda
        self.tmu = tmu
        self.mem_freq = mem_freq
        self.tensor_cores = tensor_cores
        self._compute_ipt()

    def jsonify(self):
        json_string = super(GPU, self).jsonify()
        json_string["type"] = "GPU"
        json_string["cuda_cores"] = self.cuda_cores
        json_string["tmu"] = self.tmu
        json_string["tensor_cores"] = self.tensor_cores
        json_string["mem_freq"] = self.mem_freq
        return json_string

    def _compute_ipt(self):
        texture_filler_rate = self.freq * self.tmu
        tensor_op_rate = self.tensor_cores * self.freq
        self.IPT = min(self.cuda_cores * texture_filler_rate, self.mem_freq, tensor_op_rate)  # finding the bottleneck
