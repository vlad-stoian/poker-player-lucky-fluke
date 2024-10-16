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

    def calculate_chen_score(self, hole_cards, highest_card, lowest_card):
        is_pair = highest_card == lowest_card
        is_suited = hole_cards[0]['suite'] == hole_cards[1]['suite']
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
                                   player['name'] != me['name'] and game_state['stack'] < player['bet'] and player[
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
                [card for card in game_state['community_cards'] if card['suite'] == hole_cards[0]['suite']])
            card2_matching_suit = len(
                [card for card in game_state['community_cards'] if card['suite'] == hole_cards[1]['suite']])

            big_raise = me_stack // 2
            minimum_raise = game_state['current_buy_in'] - me_bet + game_state['minimum_raise']
            if big_raise < minimum_raise:
                big_raise = me_stack

            small_raise = game_state['current_buy_in'] - me_bet + game_state['minimum_raise']
            call = game_state['current_buy_in'] - me_bet

            if other_large_bet == 0 and am_i_late:
                print('Late position all in')
                return self.bet(10000)

            chen_score = self.calculate_chen_score(hole_cards, highest_card, lowest_card)

            positional_adjustment = 0
            if am_i_late:
                positional_adjustment = 3
            elif am_i_mid:
                positional_adjustment = 1

            adjusted_score = chen_score + out_players_count - other_large_bet + me_large_bet + matching_community_low + matching_community_high + positional_adjustment + card1_matching_suit + card2_matching_suit

            b = 0
            if adjusted_score >= 11:
                print('all in')
                b = 10000
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
            return self.bet(b)

        except Exception as e:
            print('exception', e)
            return self.bet(0)

    def bet(self, amount):
        print('betting', amount)
        return int(amount)

    def showdown(self, game_state):
        pass
