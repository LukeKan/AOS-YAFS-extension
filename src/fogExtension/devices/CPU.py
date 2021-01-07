from fogExtension.devices.GenericDevice import GenericDevice


class CPU(GenericDevice):
    """
        CPU node class, used for generical purpose computation. It is defined by:
        cores (int) : hardware parallelization level,
        threads (int) : software parallelization level

    """
    def __init__(self, cores, freq, threads, pm, ram=4000):

        super().__init__(freq, pm, ram)
        self.cores = cores
        self.threads = threads
        self._compute_ipt()

    def jsonify(self):
        jsonString = super(CPU, self).jsonify()
        jsonString["type"] = "CPU"
        jsonString["cores"] = self.cores
        jsonString["threads"] = self.threads
        return jsonString

    def _compute_ipt(self):
        self.IPT = self.freq * self.cores * self.threads
