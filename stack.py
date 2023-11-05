class Stack:
    def __init__(self, colour):
        self.colour = colour
        
        self.score = 0
    
    def play_to_stack(self, card):
        if card.is_colour(self.colour) and card.is_number(self.score + 1):
            self.score += 1
            return 1
        else:
            return 0
