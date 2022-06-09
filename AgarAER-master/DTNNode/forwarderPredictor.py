class ForwarderPredictor:

    def __init__(self,neighbors):
        self.neighbors = neighbors
        self.stats_helper = {}

    def predict(self):
        min = 100000
        predictedaddr = None
        for addr,metric in self.stats_helper:
            (x,y) = metric
            res = abs(x) + abs(y) # CONFIRMAR ISTO, SEM ABS? a soma?
            if res < min:
                min = res
                predictedaddr = addr
        return self.neighbors[predictedaddr]



    def update_stats_helper(self):
        for k,neigh in self.neighbors:
            self.stats_helper[k] = self.averageDelayDiff(neigh)



    def averageDelayDiff(self,neigh):
        stats = neigh.get_stats()
        time_diff = stats.get_time_diff()
        average_delay = stats.get_average_delay()
        average_delay_overlay, lastupdate_ADO = stats.get_average_delay_overlay()
        return ((average_delay-time_diff),average_delay_overlay-lastupdate_ADO)