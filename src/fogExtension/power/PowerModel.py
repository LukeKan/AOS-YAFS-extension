class PowerModel:
    def __init__(self, en_throughput):
        self._en_throughput = en_throughput

    def get_en_throughput(self):
        return self._en_throughput

    def jsonify(self):
        return "en_throughput: " + self._en_throughput
