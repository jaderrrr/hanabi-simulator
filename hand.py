class Hand:
    def __init__(self, cards):
        self.cards = cards
    
    def choose_card(self, old_card, new_card):
        # draw to the left and shift all cards along
        chosen_card = self.cards.remove(old_card)
        self.cards.insert(0, new_card)

        return chosen_card
    
    def discard(self, idx, new_card):
        discarded_card = self.cards.pop(idx)
        self.cards.insert(0, new_card)

        return discarded_card
    
    def update_colour_info(self, indices, colour):
        for i in indices:
            self.cards[i].known_colour = colour

    def update_number_info(self, indices, number):
        for i in indices:
            self.cards[i].known_number = number
    
    def get_info(self):
        for idx, card in enumerate(self.cards):
            if card.known_colour:
                print(f"{idx}: {card.known_colour.value} {card.known_number} ", end = " ")
            else:
                print(f"{idx}: None {card.known_number} ", end = " ")