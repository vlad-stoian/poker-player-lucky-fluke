from aggressive_porky_player import AggressivePorky
from player import Conservative_Player

class PlayerRunner:
    def __init__(self):
        self.aggressive_porky = AggressivePorky()
        self.player = Conservative_Player()

    def bet(self, *args, **kwargs):

        try:
            print('Porky tries to rule the world')
            return self.aggressive_porky.bet(*args, **kwargs)
        except:
            print('Error in Aggressive Porky defaulting to boring player')
            return self.player.bet(*args, **kwargs)