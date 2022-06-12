import logging


class ForwarderPredictor:

    def __init__(self, peer):
        self.peer = peer
        self.stats_helper = {}

    def predict(self):  ## DAR LOGO O RESULTADO DE UM NO OVERLAY SE TIVER LIGADO A UM
        self.update_stats_helper()

        neighbors = self.peer.get_online_neighbors()

        overlaynode, addr = self.checkIfConnectedToOverlayNode(neighbors)

        if overlaynode is not None:
            #logging.debug(f'predicted overlay node : {overlaynode.ip}')
            return overlaynode

        min = 100000
        predictedaddr = None
        for addr, metric in self.stats_helper.items():
            (x, y) = metric
            res = abs(x) + abs(y)  # CONFIRMAR ISTO, SEM ABS? a soma?
            #logging.debug(f'im here {res}')
            if res < min:
                min = res
                predictedaddr = addr

        return self.peer.neighbors[predictedaddr]

    def checkIfConnectedToOverlayNode(self, neighborslist):
        for n in neighborslist:
            if n.isOverlay():
                return n, n.ip
        return None, None

    def update_stats_helper(self):
        lst = list(self.peer.neighbors.items())
        for k, neigh in lst:
            self.stats_helper[k] = self.averageDelayDiff(neigh)

    def averageDelayDiff(self, neigh):
        stats = neigh.get_stats()
        time_diff = stats.get_time_diff()
        average_delay = stats.get_average_delay()
       # logging.debug(f'neigh : {neigh.ip} , average_delay : {average_delay} , time_diff: {time_diff}')
        average_delay_overlay, overlay_time_diff = stats.get_average_delay_withTimeDiff()

        if overlay_time_diff is None:
            return average_delay - time_diff, 1000
        return (average_delay - time_diff), average_delay_overlay - overlay_time_diff
