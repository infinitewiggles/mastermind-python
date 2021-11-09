import row, color, peg
import random

class Game:
    def __init__(self, debug=False):

        ### Create Color Objects

        self.colors = {
            "Red" : color.Color(255, 80, 80),
            "Orange" : color.Color(255, 165, 0),
            "Yellow" : color.Color(255, 255, 0),
            "Green" : color.Color(60, 255, 60),
            "Blue" : color.Color(100, 100, 255),
            "White" : color.Color(255, 255, 255)
        }
        
        self.guesses_remaining = 10
        
        self.initial_colors = {}
        
        for key, value in self.colors.items():
            self.initial_colors[key[0]] = value

        ### Generate randomised correct pattern

        self.correct_pattern = [random.choice(list(self.colors.values())) for _ in range(4)]

        ### Print help text

        green = color.color_text(*self.colors["Green"].rgb, "green")
        orange = color.color_text(*self.colors["Orange"].rgb, "orange")
        print(f"""\
MASTERMIND - HOW TO PLAY:
To change the color of an individual peg enter the index of the peg (1-4), 
followed by the initial of a color (see below).

For example: To make the first peg green, enter 1G.

Alternatively, you can enter all the colours at once, e.g. 'RGBY'.

Once you've completed your guess, type F to (F)inish the go.

MARKING:
{green} = Correct Color & Place 
{orange} = Correct Color Only

You have {self.guesses_remaining} attempts to guess the correct pattern, Good luck! \
\n\n""", end="")
        
        print("Colors: ", end="")
        for key, value in self.colors.items():
            print("(" + color.color_text(*value.rgb, key[0]) + ")" + key[1:], end=" ")

        ### DEBUG - print solution
        
        if debug:
            print("- DEBUG Correct Pattern: " + self.get_correct_pattern_string(), end="")
        
        ### Print first row

        self.new_row()

        ### Start game

        while True:
            self.game_input()
            
    def replace_line(self, new_line):
        """Function that uses carrige return to replace the previous row"""
        print("\r"+" "*30 + f"\r{new_line}", end="")
        
    def print_line(self, line):
        """Function that prints a line without a newline in order for the above function to work"""
        print(f"\n{line}", end="")
        
    def game_input(self):
        """Function that takes the user's input and does the appropiate action"""
        selector = input()
        
        # Delete input line
        print("\033[A" + "\b"*len(selector), end="")
        
        selector = selector.upper()
        
        if selector == "F":
            self.auto_mark()
        
        if len(selector) == 4:
            for i in range(4):
                initial = selector[i].upper()
                
                if initial not in self.initial_colors.keys():
                    return
                
                color_change = self.initial_colors[initial]
                
                self.cur_row.set_peg(i, peg.Peg(color_change))
            self.update_row()
            return
        elif len(selector) != 2:
            self.update_row()
            return
        
        try:
            index = int(selector[0])
        except ValueError:
            self.update_row()
            return
        
        if index not in range(1, 5):
            self.update_row()
            return
        
        index -= 1
        
        initial = selector[1]
        
        if initial not in self.initial_colors.keys():
            self.update_row()
            return
        
        color_change = self.initial_colors[initial]
        
        self.cur_row.set_peg(index, peg.Peg(color_change))
        self.update_row()
        
    def update_row(self):
        """Function that re-prints the current row when required to update it"""
        self.replace_line(self.cur_row.get_text())
        
    def new_row(self):
        """Initialises a new row and prints it"""
        self.cur_row = row.Row()
        self.print_line(self.cur_row.get_text())
        
    def auto_mark(self):
        """Calculates the current row's score, displays it, and prints a new row if the user has not won or lost"""
        # Same color, same place
        green = 0
        # Same color, wrong place
        orange = 0
        
        correct_buffer = [color for color in self.correct_pattern]
        guess_buffer = [peg.color for peg in self.cur_row.row]
        
        for index, guess in enumerate(guess_buffer):
            if guess != None and correct_buffer[index] != None and guess.equals(correct_buffer[index]):
                green += 1
                correct_buffer[index] = None
                guess_buffer[index] = None
        
        for index, guess in enumerate(guess_buffer):
            if guess != None:
                for correct_index, item in enumerate(correct_buffer):
                    if item != None and item.equals(guess):
                        orange += 1
                        correct_buffer[correct_index] = None
                        guess_buffer[index] = None
                        break
        
        self.cur_row.mark(green, orange)
        self.update_row()
        
        if green == 4:
            self.win()
        else:
            self.check_if_lost()
            self.new_row()
            
    def win(self):
        """Function is run on win"""
        print("\nYou win!")
        exit()
    
    def get_correct_pattern_string(self):
        """Creates row object based off correct pattern in order to display that pattern to the user"""
        r = row.Row()
        for index, color in enumerate(self.correct_pattern):
            r.set_peg(index, peg.Peg(color))
        return r.get_text()

    def check_if_lost(self):
        """Gets run at the end of each round, decreases the number of guesses remaining and if that reaches zero it ends the game"""
        self.guesses_remaining -= 1
        if self.guesses_remaining < 1:
            print(f"\nYou lost!\nThe correct pattern was: {self.get_correct_pattern_string()}")
            exit()