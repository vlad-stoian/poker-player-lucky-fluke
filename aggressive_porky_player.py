class Player:
    VERSION = "Turbo Aggressive Porky"

    def rank_to_value(self, rank):
        if rank == 'J':
            return 11
        elif rank == 'Q':
            return 12
        elif rank == 'K':
            return 13
        elif rank == 'A':
            return 14
        else:
            return int(rank)

    def calculate_c_score(self, hole_cards, highest_card, lowest_card):
        is_pair = highest_card == lowest_card
        is_suited = hole_cards[0]['suit'] == hole_cards[1]['suit']
        gap = highest_card - lowest_card

        if highest_card > 10:
            score = highest_card - 1
        else:
            score = highest_card / 2

        if is_pair:
            score = max(5, score * 2)

        if is_suited:
            score += 2

        if gap == 1:
            score -= 1
        elif gap == 2:
            score -= 2
        elif gap == 3:
            score -= 4
        elif gap >= 4:
            score -= 5

        if gap <= 1 and highest_card < 12 and not is_pair:
            score += 1

        return int(score + 0.5)

    def betRequest(self, game_state):
        try:
            me = game_state['players'][game_state['in_action']]
            hole_cards = me['hole_cards']
            me_stack = me['stack']
            me_bet = me['bet']
            dealer = game_state['dealer']

            out_players_count = len([player for player in game_state['players'] if player['status'] == 'out'])
            am_i_mid = (dealer + 1 + out_players_count) == game_state['in_action']
            am_i_late = (dealer + 2 + out_players_count) == game_state['in_action']

            other_large_bet = len([player for player in game_state['players'] if
                                   player['name'] != me['name'] and player['stack'] < player['bet'] and player[
                                       'status'] == 'active'])

            me_large_bet = 1 if me_stack < me_bet else 0

            card1 = self.rank_to_value(hole_cards[0]['rank'])
            card2 = self.rank_to_value(hole_cards[1]['rank'])
            highest_card = max(card1, card2)
            lowest_card = min(card1, card2)

            matching_community_low = len(
                [card for card in game_state['community_cards'] if self.rank_to_value(card['rank']) == highest_card])
            matching_community_high = len(
                [card for card in game_state['community_cards'] if self.rank_to_value(card['rank']) == lowest_card])
            card1_matching_suit = len(
                [card for card in game_state['community_cards'] if card['suit'] == hole_cards[0]['suit']])
            card2_matching_suit = len(
                [card for card in game_state['community_cards'] if card['suit'] == hole_cards[1]['suit']])

            big_raise = me_stack // 2
            minimum_raise = game_state['current_buy_in'] - me_bet + game_state['minimum_raise']
            if big_raise < minimum_raise:
                big_raise = me_stack

            small_raise = game_state['current_buy_in'] - me_bet + game_state['minimum_raise']
            call = game_state['current_buy_in'] - me_bet

            if other_large_bet == 0 and am_i_late:
                print('Late position all in')
                return 10000

            c_score = self.calculate_c_score(hole_cards, highest_card, lowest_card)

            positional_adjustment = 0
            if am_i_late:
                positional_adjustment = 3
            elif am_i_mid:
                positional_adjustment = 1

            adjusted_score = c_score + out_players_count - other_large_bet + me_large_bet + matching_community_low + matching_community_high + positional_adjustment + card1_matching_suit + card2_matching_suit

            b = 0
            if adjusted_score >= 11:
                b = 10000
                print('all in', b)
            elif adjusted_score >= 9:
                b = big_raise
                print('big raise', b)
            elif adjusted_score >= 8:
                b = min(small_raise, me_stack // 5)
                print('small raise', b)
            elif adjusted_score >= 7:
                b = min(call, me_stack // 5)
                print('call', b)

            print('returning bet', b)
            return int(b)

        except Exception as e:
            print('exception', e)
            return 0

    def showdown(self, game_state):
        pass


if __name__ == "__main__":

    game_state = {
        "tournament_id": "550d1d68cd7bd10003000003",
        "game_id": "550da1cb2d909006e90004b1",
        "round": 3,
        "bet_index": 2,
        "small_blind": 10,
        "current_buy_in": 320,
        "pot": 600,
        "minimum_raise": 240,
        "dealer": 1,
        "orbits": 7,
        "in_action": 0,
        "players": [
            {
                "id": 0,
                "name": "lalala",
                "status": "active",
                "version": "Ultimate Chan Killer",
                "stack": 1500,
                "bet": 320,
                "hole_cards": [{"rank": "A", "suit": "hearts"}, {"rank": "K", "suit": "hearts"}],
            },
            {
                "id": 1,
                "name": "Bob",
                "status": "active",
                "version": "Default random player",
                "stack": 900,
                "bet": 240,
                "hole_cards": [{"rank": "10", "suit": "spades"}, {"rank": "J", "suit": "clubs"}],
            },
            {
                "id": 2,
                "name": "Chuck",
                "status": "folded",
                "version": "Default random player",
                "stack": 0,
                "bet": 0,
                "hole_cards": [],
            },
        ],
        "community_cards": [
            {"rank": "Q", "suit": "hearts"},
            {"rank": "5", "suit": "diamonds"},
            {"rank": "6", "suit": "hearts"},
        ],
    }
    player = Player()
    player.betRequest(game_state)
