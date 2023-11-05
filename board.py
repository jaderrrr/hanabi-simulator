import random

from utils import Colours
from stack import Stack
from card import Card

class Board:
    def __init__(self, is_rainbow):
        included_colours = [Colours.WHITE, Colours.RED, Colours.BLUE, Colours.GREEN, Colours.YELLOW]
        if (is_rainbow):
            included_colours.append(Colours.RAINBOW)

        self.stacks = []
        for colour in included_colours:
            self.stacks.append(Stack(colour))
        
        self.deck = []
        for i in range(3):
            for colour in included_colours:
                self.deck.append(Card(1, colour))
        
        for i in range(2):
            for colour in included_colours:
                self.deck.append(Card(2, colour))
                self.deck.append(Card(3, colour))
                self.deck.append(Card(4, colour))

        for colour in included_colours:
            self.deck.append(Card(5, colour))
        
        random.shuffle(self.deck)
        
        self.time_remaining = 8
        self.explosions = 0
        self.discarded = []
    
    def get_relevant_stack(self, card):
        for stack in self.stacks:
            if stack.colour == card.colour:
                return stack
        
        return None

    def deal_cards(self, player_count):
        deal = []

        for player in range(player_count):
            cards = []
            for i in range(4):
                cards.append(self.deck.pop())
            
            deal.append(cards)
        
        return deal

    def get_next_card(self):
        if (len(self.deck) > 0):
            return self.deck.pop()
        else:
            return Card(None, None)

    def is_playable(self, card):
        for stack in self.stacks:
            if card.is_colour(stack.colour):
                if card.number == stack.score + 1:
                    return True
                else:
                    return False
        
        return False
    
    def is_playable_number(self, number):
        for stack in self.stacks:
            if stack.score < number - 1:
                return False
            
            if stack.score >= number:
                number_of_same_card = 0
                for c in self.discarded:
                    if c.colour == stack.colour and c.number == number:
                        number_of_same_card += 1

                if number == 1:
                    if number_of_same_card < 2:
                        return False
                
                elif number == 2 or number == 3 or number == 4:
                    if number_of_same_card < 1:
                        return False
            
        return True

    def is_playable_colour(self, colour):
        # TODO pretty rare case i think
        return False

    def play_card(self, card):
        for stack in self.stacks:
            if card.is_colour(stack.colour):
                result = stack.play_to_stack(card)
                if result == 0:
                    self.discard_card(card, False)
                    self.explosions += 1
                else:
                    if card.number == 5:
                        self.time_remaining += 1
                        if self.time_remaining > 8:
                            self.time_remaining = 8
            
                return result

    def discard_card(self, discarded_card, is_purposeful):
        if not self.can_discard(discarded_card):
            print(f"DISCARDING LAST CARD OF TYPE {discarded_card.colour.value} {discarded_card.number}")
        self.discarded.append(discarded_card)

        if is_purposeful:
            self.time_remaining += 1
            if self.time_remaining > 8:
                self.time_remaining = 8
    
    def can_discard(self, card):
        # TODO deal with unreachable states (i.e. discardable cards because we can't ever get up to there)
        relevant_stack = self.get_relevant_stack(card)
        if not relevant_stack:
            return False

        if relevant_stack.score >= card.number:
            return True
        
        if card.number == 5:
            return False

        number_of_same_card = 0
        for c in self.discarded:
            if c.colour == card and c.number == card:
                number_of_same_card += 1
        
        if card.number == 1:
            if number_of_same_card == 2:
                return False
            else:
                return True
        
        if card.number == 2 or card.number == 3 or card.number == 4:
            if number_of_same_card == 1:
                return False
            else:
                return True

    def get_time_remaining(self):
        return self.time_remaining
    
    def print_board(self):
        print("****")
        for stack in self.stacks:
            print(f"{stack.colour.value}: {stack.score} ", end="")
        print()
        print("****")
        print(f"Time Remaining: {self.time_remaining}")
        print(f"Explosions: {self.explosions}")
        print(f"Board deck length: {len(self.deck)}")
        print("****")