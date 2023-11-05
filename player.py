class Player:
    def __init__(self, hand, board):
        self.hand = hand
        self.next_players = None
        self.can_play = []
        self.board = board

        self.card_to_discard_idx = 3
    
    def set_next_players(self, next_players):
        self.next_players = next_players
    
    def next_player_will_make_a_bad_move(self):
        if (len(self.next_players[0].can_play)) > 0:
            return False
        else:
            card_they_will_discard = self.next_players[0].hand.cards[self.next_players[0].card_to_discard_idx]

            if self.board.can_discard(card_they_will_discard):
                return False
            else:
                return True

    def update_can_play(self):
        for card in self.hand.cards:
            if card not in self.can_play:
                if card.known_number and card.known_colour:
                    if self.board.is_playable(card):
                        self.can_play.append(card)
                elif card.known_number:
                    if self.board.is_playable_number(card.known_number):
                        self.can_play.append(card)
                elif card.known_colour:
                    if self.board.is_playable_colour(card.colour):
                        self.can_play.append(known_colour)

    def tell_player_to_play_a_card(self, player):
        relevant_cards = list(set(player.hand.cards).symmetric_difference(player.can_play))

        playable_cards = []
        for card in relevant_cards:
            if self.board.is_playable(card):
                playable_cards.append(card)
        
        if len(playable_cards) == 0:
            return 0
        
        for card in playable_cards:
            indexes_with_same_number = []
            indexes_with_same_colour = []
            index_of_card = -1

            for index, hand_card in enumerate(player.hand.cards):
                if card.number == hand_card.number:
                    indexes_with_same_number.append(index)
                if card.colour == hand_card.colour:
                    indexes_with_same_colour.append(index)
                if card.number == hand_card.number and card.colour == hand_card.colour:
                    index_of_card = index

            # if card is right most of the number in the player hand, give that clue
            if index_of_card == max(indexes_with_same_number):
                player.hand.update_number_info(indexes_with_same_number, card.number)
                player.can_play.append(card)
                return 1

            # if the card is not the card they were about to discard, and it is the right most colour, tell them the colour
            if index_of_card != player.card_to_discard_idx and index_of_card == max(indexes_with_same_colour):
                player.hand.update_colour_info(indexes_with_same_colour, card.colour)
                player.can_play.append(card)
                return 1
        
        return 0

    def tell_player_not_to_discard(self, player):
        player.hand.update_colour_info([player.card_to_discard_idx], player.hand.cards[player.card_to_discard_idx].colour)
        player.card_to_discard_idx -= 1
        if player.card_to_discard_idx < 0:
            player.card_to_discard_idx = 0

    def play_turn(self):
        print("What I know about my hand: ", end="")
        self.hand.get_info()
        print(f"card to discard idx: {self.card_to_discard_idx}")

        # if there is one information left, and the next player will discard a unique card, give information to the next player
        if self.board.get_time_remaining() == 1 and self.next_player_will_make_a_bad_move():
            result = self.tell_player_to_play_a_card(self.next_players[0])
            if result == 0:
                # signal not okay to discard = give colour of last card
                self.tell_player_not_to_discard(self.next_players[0])
                print("# stopped player from discarding bad move card")
            else:
                print("# gave information to next player")
            
            self.next_players[0].update_can_play()
            self.board.time_remaining -= 1
        
        # if there is a card they can definitely play, they should play it
        elif len(self.can_play) > 0:
            print("# played a card")
            card_to_play = self.can_play.pop()
            card_to_play_idx = self.hand.cards.index(card_to_play)

            new_card = self.board.get_next_card()
            self.hand.choose_card(card_to_play, new_card)
            self.board.play_card(card_to_play)

            if card_to_play_idx > self.card_to_discard_idx:
                self.card_to_discard_idx += 1

            for player in self.next_players:
                player.update_can_play()
            self.update_can_play()

        # if there is no information available, they should discard
        elif self.board.get_time_remaining() == 0:
            print("# discarded")
            new_card = self.board.get_next_card()

            discarded_card = self.hand.discard(self.card_to_discard_idx, new_card)
            self.board.discard_card(discarded_card, True)


        # give information to the next player who can play a card based on info given
        else:
            for player in self.next_players:
                result = self.tell_player_to_play_a_card(player)
                if result == 1:
                    print("# gave information to a player")
                    player.update_can_play()
                    self.board.time_remaining -= 1
                    return
            
            # give the number of their last card to the next player
            """
            self.next_players[0].hand.update_number_info([3], player.hand.cards[3].number)
            print("# gave random information")
            player.update_can_play()
            self.board.time_remaining -= 1
            """
            print(f"# discarded")
            new_card = self.board.get_next_card()

            discarded_card = self.hand.discard(self.card_to_discard_idx, new_card)
            self.board.discard_card(discarded_card, True)
            

    def print_hand(self):
        for card in self.hand.cards:
            if card.colour:
                print(f"({card.colour.value}, {card.number}) ", end = "")
            else:
                print("(blank) ", end="")
        
        print("")
