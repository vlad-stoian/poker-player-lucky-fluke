class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):

        return max(p["bet"] for p in game_state["players"]) + 1

    def showdown(self, game_state):
        pass
