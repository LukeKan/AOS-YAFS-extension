class PowerModel:
    """
    Base abstract class of a generic power model with its mandatory parameters.
    """

    def __init__(self, en_throughput, ppi):
        """
        Generic definition of mandatory parameters.

        Args:
                en_throughput (float): limitation in terms of throughput that the power model applies correspondingly,
                    to the power management policy;
                ppi (int): power per instruction representing the amount of power (mW) consumed by each instruction
        """
        self._en_throughput = en_throughput
        self._PPI = ppi

    def get_en_throughput(self):
        return self._en_throughput

    def jsonify(self):
        json_string = {"en_throughput": self._en_throughput, "PPI": self._PPI}
        return json_string
