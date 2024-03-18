import math
import statistics
import random

class Game:

    def __init__(self, boxes=100):
        self.boxes = [i for i in range(boxes)]
        random.shuffle(self.boxes)
        self.revealed = boxes * [None]
        self.revealed_most_recently = None

    def guess(self, player, number: int):
        self.revealed[number] = self.boxes[number]
        self.revealed_most_recently = self.boxes[number]
        if self.boxes[number] == player:
            return True
        else:
            return False

    def play(self, strategy):
        """
        For each player, execute the strategy. Tot up the results.
        """
        prisoners_succeeded = 0

        # each prisoner goes in one at a time
        for prisoner in range(len(self.boxes)):

            # guess a sequence of numbers, according to the pre-arranged strategy
            for i in range(math.floor(len(self.boxes)/2)):
                guess = strategy.get_next_guess(prisoner, i, self)
                if self.guess(prisoner, guess):
                    prisoners_succeeded = prisoners_succeeded + 1
                    break

            # hide all the boxes again, ready for the next prisoner
            self.revealed = len(self.boxes) * [None]
            self.revealed_most_recently = None

        print(prisoners_succeeded)
        return prisoners_succeeded

