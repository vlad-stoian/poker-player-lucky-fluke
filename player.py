class Player:
    VERSION = "B0rk3d"

    def betRequest(self, game_state):
        return game_state["current_buy_in"] - game_state["players"][game_state["in_action"]]["bet"] + game_state[
            "minimum_raise"] + 1

    def showdown(self, game_state):
        pass

    def pre_flop_strategy(self, hole_cards, current_buy_in, player_bet, minimum_raise):
        # Simple pre-flop strategy based on hole cards
        strong_hands = [('A', 'A'), ('K', 'K'), ('Q', 'Q'), ('A', 'K'), ('J', 'J')]
        moderate_hands = [('A', 'Q'), ('A', 'J'), ('K', 'Q'), ('K', 'J'), ('10', '10')]

        card_ranks = sorted([card["rank"] for card in hole_cards])

        if tuple(card_ranks) in strong_hands:
            # Raise with strong hands
            return current_buy_in - player_bet + minimum_raise  # Raise aggressively
        elif tuple(card_ranks) in moderate_hands:
            # Call with moderate hands
            return current_buy_in - player_bet  # Just call
        else:
            # Check or fold with weak hands
            if current_buy_in > player_bet:
                return 0  # Fold if the bet is raised too high
            return current_buy_in - player_bet  # Otherwise, check or call
        
    def post_flop_strategy(self, hand_strength, current_buy_in, player_bet, minimum_raise):
        # Simple post-flop, turn, and river strategy based on hand strength
        if hand_strength >= 8:
            # Strong hand (Two pair, three of a kind, straight, flush, etc.)
            return current_buy_in - player_bet + minimum_raise  # Raise
        elif hand_strength >= 5:
            # Medium strength (Top pair, second pair)
            return current_buy_in - player_bet  # Call or check
        else:
            # Weak hand (Nothing or low pairs)
            if current_buy_in > player_bet:
                return 0  # Fold if the bet is too high
            return current_buy_in - player_bet  # Otherwise, check or call
