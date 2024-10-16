from hand_evaluator import HandEvaluator

class Player:
    VERSION = "B0rk3d AI Alpha 0.2"

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
            small_blind = game_state["small_blind"]

            print("Small blind:", small_blind)
            print("Current stack:", stack)
            print("Hole cards:", hole_cards)

            # Determine your current hand strength
            hand_strength = HandEvaluator.evaluate_hand(hole_cards, community_cards)

            num_community_cards = len(community_cards)
            print("Num community cards:", num_community_cards)

            # Betting strategy based on hand strength and stage of the game
            if num_community_cards == 0:
                # Pre-flop strategy
                return self.pre_flop_strategy(hole_cards, current_buy_in, player_bet, minimum_raise, stack)
            else:
                # Post-flop, Turn, River strategy
                value = self.post_flop_strategy(
                    hand_strength, current_buy_in, player_bet, minimum_raise, stack, num_community_cards)
                return int(value)
        except Exception as e:
            print("Error occured betting 0", e)
            return 0

    def showdown(self, game_state):
        pass

    def pre_flop_strategy(self, hole_cards, current_buy_in, player_bet, minimum_raise, stack):
        # Simple pre-flop strategy based on hole cards
        strong_hands = [('A', 'A'), ('K', 'K'), ('Q', 'Q'), ('A', 'K'), ('J', 'J')]
        moderate_hands = [('A', 'Q'), ('A', 'J'), ('K', 'Q'), ('J', 'K'), ('10', '10')]

        call_amount = current_buy_in - player_bet

        card_ranks = sorted([card["rank"] for card in hole_cards])

        if tuple(card_ranks) in strong_hands:
            # Raise with strong hands
            return call_amount + minimum_raise  # Raise aggressively
        elif tuple(card_ranks) in moderate_hands:
            # Call with moderate hands
            return call_amount  # Just call
        else:
            # Check or fold with weak hands
            if current_buy_in > player_bet:
                return 0  # Fold if the bet is raised too high
            return current_buy_in - player_bet  # Otherwise, check or call
        
    def post_flop_strategy(self, hand_strength, current_buy_in, player_bet, minimum_raise, stack, num_community_cards):
        call_amount = current_buy_in - player_bet
        if hand_strength >= 5:
            if hand_strength >= 9:
                return call_amount + max(stack, minimum_raise)  # All-in
            elif hand_strength >= 8:
                return call_amount + max(stack / 2, minimum_raise)
            return call_amount + minimum_raise  # Raise
        elif hand_strength >= 2:
            if hand_strength == 4 or call_amount < stack / 4:
                return call_amount
            return 0
        else:
            if call_amount > 0:
                return 0  # Fold if the bet is too high
            return call_amount  # Otherwise, check or call
