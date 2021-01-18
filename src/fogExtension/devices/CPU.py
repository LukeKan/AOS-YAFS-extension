from fogExtension.devices.GenericHardware import GenericDevice


class CPU(GenericDevice):
    """
        CPU node class, used for generical purpose computation. It is defined by:
        cores (int) : hardware parallelization level,
        threads (int) : software parallelization level

    """
    def __init__(self, freq, pm, ram=4000, cores=1,  threads=1,):

        super().__init__(freq, pm, ram)
        self.cores = cores
        self.threads = threads
        self._compute_ipt()

    def jsonify(self):
        json_string = super(CPU, self).jsonify()
        json_string["type"] = "CPU"
        json_string["cores"] = self.cores
        json_string["threads"] = self.threads
        return json_string

    def _compute_ipt(self):
        self.IPT = self.freq * self.cores * self.threads
