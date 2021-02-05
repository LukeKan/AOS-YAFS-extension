from fogExtension.devices.GenericHardware import GenericDevice


class CPU(GenericDevice):
    """
        CPU node class, used for generic purpose computation.
    """
    def __init__(self, freq, pm, ram=4000, cores=1,  threads=1,):
        """

        Args:
            cores (int): hardware parallelization level,
            threads (int): software parallelization level

        """
        super().__init__(freq, pm, ram)
        self.cores = cores
        self.threads = threads
        self._compute_ipt()

    def jsonify(self):
        """

        Returns: jsonified CPU object

        """
        json_string = super(CPU, self).jsonify()
        json_string["type"] = "CPU"
        json_string["c_tot"] = self.cores
        json_string["c_available"] = self.cores
        json_string["threads"] = self.threads
        return json_string

    def _compute_ipt(self):
        """
        It computes the IPT depending on the frequency and hw/sw parallelization levels of the CPU.
        """
        self.IPT = self.freq * self.cores * self.threads

    @staticmethod
    def recompute_ipt(active_cores, active_threads, freq):
        """
        Static function used at simulation runtime in order to recompute the IPT parameter when changing the cores,
        threads and the device frequency.

        Args:
            active_cores (int): hardware parallelization level,
            active_threads (int): software parallelization level,
            freq (float) : operating frequency of the device

        Returns:
            the recomputed IPT

        """
        return freq * active_cores * active_threads
