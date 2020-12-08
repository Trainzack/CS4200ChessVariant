import math
class MCT():
    def __init__(self, game_state, parent=None, prior=0):
        self.game_state = game_state
        self.is_expanded = False
        self.parent = parent
        self.children = {}
        self.total_value = 0  # float
        self.number_visits = 0  # int
    def exploit(self):
        return self.total_value / (1 + self.number_visits)
    def explore(self):
        return (math.sqrt(self.parent.number_visits()) * self.prior/ (1 + self.number_visits))

