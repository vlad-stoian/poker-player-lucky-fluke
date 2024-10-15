from hand_evaluator import HandEvaluator

class Player:
    VERSION = "Agressive Porky returns"

    def betRequest(self, game_state):
        player_index = game_state["in_action"]
        player = game_state["players"][player_index]
        hole_cards = player["hole_cards"]
        community_cards = game_state["community_cards"]
        current_buy_in = game_state["current_buy_in"]
        player_bet = player["bet"]
        minimum_raise = game_state["minimum_raise"]
        stack = player["stack"]

        print("Current stack:", stack)

        agressiveness = self.compute_agressiveness(game_state)
        multiply_factor = self.get_multiply_factor(agressiveness)

        # Determine your current hand strength
        hand_strength = HandEvaluator.evaluate_hand(hole_cards, community_cards)

        # Betting strategy based on hand strength and stage of the game
        if len(community_cards) == 0:
            # Pre-flop strategy
            return self.pre_flop_strategy(hole_cards, current_buy_in, player_bet, minimum_raise, stack)
        else:
            # Post-flop, Turn, River strategy
            return self.post_flop_strategy(hand_strength, current_buy_in, player_bet, minimum_raise, stack)

    def showdown(self, game_state):
        pass

    def compute_agressiveness(self, game_state):
        player_index = game_state["in_action"]
        players = game_state["players"]
        player = players[player_index]
        
        # Sort players based on stack in descending order
        sorted_players = sorted(players, key=lambda p: p['stack'], reverse=True)
        
        # Find the position of the current player in the sorted list
        position = next(i for i, p in enumerate(sorted_players) if p['id'] == player['id'])
        
        # Calculate aggressiveness based on the player's position
        total_players = len(players)
        aggressiveness = (total_players - position) / total_players
        
        return aggressiveness
 
    def get_multiply_factor(self, aggressiveness):
        if aggressiveness < 0.2:
            return 1
        elif aggressiveness < 0.4:
            return 2
        elif aggressiveness < 0.6:
            return 3
        elif aggressiveness < 0.8:
            return 4
        else:
            return 5

    def pre_flop_strategy(self, hole_cards, current_buy_in, player_bet, minimum_raise, stack, multiply_factor):
        # Simple pre-flop strategy based on hole cards
        strong_hands = [('A', 'A'), ('K', 'K'), ('Q', 'Q'), ('A', 'K'), ('J', 'J')]
        moderate_hands = [('A', 'Q'), ('A', 'J'), ('K', 'Q'), ('K', 'J'), ('10', '10')]

        min_raise_amount = current_buy_in - player_bet + minimum_raise
        call_amount = current_buy_in - player_bet
        
        card_ranks = sorted([card["rank"] for card in hole_cards])

        if tuple(card_ranks) in strong_hands:
            # Raise with strong hands
            return min_raise_amount * multiply_factor  # Raise aggressively
        elif tuple(card_ranks) in moderate_hands:
            # Call with moderate hands
            return (current_buy_in - player_bet)  # Just call
        else:
            # Check or fold with weak hands
            if current_buy_in > player_bet:
                return 0  # Fold if the bet is raised too high
            return current_buy_in - player_bet  # Otherwise, check or call
        
    def post_flop_strategy(self, hand_strength, current_buy_in, player_bet, minimum_raise, stack, multiply_factor):
        min_raise_amount = current_buy_in - player_bet + minimum_raise
        call_amount = current_buy_in - player_bet
        # Simple post-flop, turn, and river strategy based on hand strength
        if hand_strength >= 5:
            # Strong hand (Two pair, three of a kind, straight, flush, etc.)
            return min_raise_amount * multiply_factor  # Raise
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
