from hand_evaluator import HandEvaluator

class Player:
    VERSION = "B0rk3d AI Hero Aggressive Sophisticated 2"

    def betRequest(self, game_state):

        try:
            player_index = game_state["in_action"]
            player = game_state["players"][player_index]
            hole_cards = player["hole_cards"]
            community_cards = game_state["community_cards"]
            current_buy_in = game_state["current_buy_in"]
            player_bet = player["bet"]
            minimum_raise = game_state["minimum_raise"]
            stack = player["stack"]

            print("Current stack:", stack)

            # Determine your current hand strength
            hand_strength = HandEvaluator.evaluate_hand(hole_cards, community_cards)

            # Betting strategy based on hand strength and stage of the game
            if len(community_cards) == 0:
                # Pre-flop strategy
                return self.pre_flop_strategy(hole_cards, current_buy_in, player_bet, minimum_raise, stack)
            else:
                # Post-flop, Turn, River strategy
                return self.post_flop_strategy(hand_strength, current_buy_in, player_bet, minimum_raise, stack)
        except Exception as e:
            print("Error occured betting 0", e)
            return 0

    def showdown(self, game_state):
        pass

    def pre_flop_strategy(self, hole_cards, current_buy_in, player_bet, minimum_raise, stack):
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
        
    def post_flop_strategy(self, hand_strength, current_buy_in, player_bet, minimum_raise, stack):
        min_raise_amount = current_buy_in - player_bet + minimum_raise
        call_amount = current_buy_in - player_bet
        # Simple post-flop, turn, and river strategy based on hand strength
        if hand_strength >= 5:
            # Strong hand (Two pair, three of a kind, straight, flush, etc.)
            return min_raise_amount * 4  # Raise
        elif hand_strength >= 2:
            # Medium strength (Top pair, second pair)
            if hand_strength == 4 or call_amount < stack / 4:
                return call_amount
            return 0  # Call or check
        else:
            # Weak hand (Nothing or low pairs)
            if current_buy_in > player_bet:
                return 0  # Fold if the bet is too high
            return current_buy_in - player_bet  # Otherwise, check or call
