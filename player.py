class Player:
    VERSION = "Default Python folding player"

    def betRequest(self, game_state):
        return game_state["current_buy_in"] - game_state["players"][game_state["in_action"]]["bet"] + game_state[
            "minimum_raise"]

    def showdown(self, game_state):
        pass
