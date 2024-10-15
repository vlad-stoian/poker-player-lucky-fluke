from collections import Counter

class HandEvaluator:
    
    RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    SUIT_ORDER = ['clubs', 'diamonds', 'hearts', 'spades']

    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        # Combine hole cards and community cards
        all_cards = hole_cards + community_cards
        ranks = [card['rank'] for card in all_cards]
        suits = [card['suit'] for card in all_cards]
        
        # Count ranks and suits
        rank_counts = Counter(ranks)
        suit_counts = Counter(suits)
        
        # Sort cards by rank in descending order
        sorted_ranks = sorted([HandEvaluator.RANK_ORDER[rank] for rank in ranks], reverse=True)
        
        # Check for combinations
        is_flush = HandEvaluator.is_flush(suit_counts)
        is_straight = HandEvaluator.is_straight(sorted_ranks)
        
        # Determine the hand rank
        if is_flush and is_straight:
            return 9  # Straight Flush
        if HandEvaluator.is_four_of_a_kind(rank_counts):
            return 8  # Four of a Kind
        if HandEvaluator.is_full_house(rank_counts):
            return 7  # Full House
        if is_flush:
            return 6  # Flush
        if is_straight:
            return 5  # Straight
        if HandEvaluator.is_three_of_a_kind(rank_counts):
            return 4  # Three of a Kind
        if HandEvaluator.is_two_pair(rank_counts):
            return 3  # Two Pair
        if HandEvaluator.is_one_pair(rank_counts):
            return 2  # One Pair
        
        return 1  # High Card

    @staticmethod
    def is_flush(suit_counts):
        # Flush: All cards in the same suit
        for suit, count in suit_counts.items():
            if count >= 5:
                return True
        return False

    @staticmethod
    def is_straight(sorted_ranks):
        # Straight: Five consecutive ranks
        sorted_unique_ranks = sorted(set(sorted_ranks), reverse=True)
        for i in range(len(sorted_unique_ranks) - 4):
            if sorted_unique_ranks[i] - sorted_unique_ranks[i + 4] == 4:
                return True
        # Special case: Ace can be part of a 5-high straight (A, 2, 3, 4, 5)
        if {14, 5, 4, 3, 2}.issubset(sorted_unique_ranks):
            return True
        return False

    @staticmethod
    def is_four_of_a_kind(rank_counts):
        # Four of a kind: Four cards of the same rank
        return 4 in rank_counts.values()

    @staticmethod
    def is_full_house(rank_counts):
        # Full House: Three of a kind and a pair
        has_three = False
        has_pair = False
        for count in rank_counts.values():
            if count == 3:
                has_three = True
            if count == 2:
                has_pair = True
        return has_three and has_pair

    @staticmethod
    def is_three_of_a_kind(rank_counts):
        # Three of a kind: Three cards of the same rank
        return 3 in rank_counts.values()

    @staticmethod
    def is_two_pair(rank_counts):
        # Two Pair: Two sets of two cards of the same rank
        pairs = [count for count in rank_counts.values() if count == 2]
        return len(pairs) >= 2

    @staticmethod
    def is_one_pair(rank_counts):
        # One Pair: Two cards of the same rank
        return 2 in rank_counts.values()
    
    
