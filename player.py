from collections import Counter
from hand_evaluator import HandEvaluator

class Player:
    VERSION = "Agressive Porky"

    def betRequest(self, game_state):
        player_index = game_state["in_action"]
        player = game_state["players"][player_index]
        hole_cards = player["hole_cards"]
        community_cards = game_state["community_cards"]
        current_buy_in = game_state["current_buy_in"]
        player_bet = player["bet"]
        minimum_raise = game_state["minimum_raise"]

        # Determine your current hand strength
        hand_strength = HandEvaluator.evaluate_hand(hole_cards, community_cards)

        # Betting strategy based on hand strength and stage of the game
        if len(community_cards) == 0:
            # Pre-flop strategy
            return self.pre_flop_strategy(hole_cards, current_buy_in, player_bet, minimum_raise)
        else:
            # Post-flop, Turn, River strategy
            return self.post_flop_strategy(hand_strength, current_buy_in, player_bet, minimum_raise)

    def showdown(self, game_state):
        pass

    def post_flop_strategy(self, hole_cards, community_cards, hand_strength, current_buy_in, player_bet, minimum_raise):
        # Combine hole cards and community cards
        all_cards = hole_cards + community_cards
        
        # Extract ranks and suits from all cards
        ranks = [card['rank'] for card in all_cards]
        suits = [card['suit'] for card in all_cards]

        # Convert ranks to numerical values for easier comparison
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                    '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        sorted_ranks = sorted([rank_order[rank] for rank in ranks], reverse=True)

        # Count the occurrence of each suit
        suit_counts = Counter(suits)

        # Now proceed with the strategy using sorted_ranks and suit_counts
        if hand_strength >= 8:
            # Strong hand (e.g., trips or better), raise aggressively
            return current_buy_in - player_bet + 3 * minimum_raise
        elif hand_strength >= 5:
            # Medium strength hand (e.g., top pair), play moderately
            return current_buy_in - player_bet + minimum_raise
        elif self.is_straight_draw(sorted_ranks) or self.is_flush_draw(suit_counts):
            # Semi-bluff when you have a strong draw (straight or flush draw)
            return current_buy_in - player_bet + minimum_raise
        else:
            # Fold if you have a weak hand
            return 0 if current_buy_in > player_bet else current_buy_in - player_bet
        
    def is_straight_draw(self, sorted_ranks):
    # Check for a straight draw (4 consecutive cards)
        for i in range(len(sorted_ranks) - 3):
            if sorted_ranks[i] - sorted_ranks[i + 3] == 3:
                return True
        return False

    def is_flush_draw(self, suit_counts):
        # Check for a flush draw (4 cards of the same suit)
        for suit, count in suit_counts.items():
            if count == 4:
                return True
        return False
