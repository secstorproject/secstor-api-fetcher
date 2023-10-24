class Timing:
    def __init__(self, algorithm, thread, register, timings):
        self.algorithm = algorithm
        self.thread = thread
        self.register = register
        self.timings = timings
        


class SplitTiming(Timing):
    pass


class ReconstructTiming(Timing):
    def __init__(self, algorithm, thread, register, timings, keys):
        super().__init__(algorithm, thread, register, timings)
        self.keys = keys
