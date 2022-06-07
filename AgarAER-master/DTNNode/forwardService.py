import queue

from forwarderPredictor import ForwarderPredictor
class ForwardService:

    def __init__(self):
        self.predictor = ForwarderPredictor()
        self.queueToForward = queue.PriorityQueue()


    def forward(self,packet,addr):
        pass
