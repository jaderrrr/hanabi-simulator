class Card:
    def __init__(self, number, colour):
        self.number = number
        self.colour = colour
        self.known_number = None
        self.known_colour = None

    def is_colour(self, colour):
        return colour == self.colour
    
    def is_number(self, number):
        return number == self.number