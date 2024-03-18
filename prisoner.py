import math
import statistics
import random

from _ctypes_test import func


class Strategy:

    def __init__(self, get_next_guess: func):
        self.get_next_guess = get_next_guess

    def get_next_guess(self, player, i, game):
        raise NotImplementedError()

    @classmethod
    def naive(cls, players=100):
        """
        Just guess numbers in any ole order
        """
        guesses = [x for x in range(players)]
        random.shuffle(guesses)
        def guess_generator(player, i,  game):
            return guesses[i]


        return cls(guess_generator)

    @classmethod
    def chain(cls):
        """
        guess your own number first, then guess each revealed number
        """
        def guess_generator(player, i,  game):
            if game.revealed_most_recently is None:
                return player
            else:
                return game.revealed_most_recently

        return cls(guess_generator)

    @classmethod
    def prime(cls):
        # guess your own number first, then guess multiples of it
        raise NotImplementedError()
        def guess_generator(player, i, game):
            if player == 0:
                return i
            for x in range(i+1*player, 100):
                if math.gcd(player+1, x+1) > 1:
                    return x
            #return ((player+1) * (i+1)) % players

        for p in range(players):
            strat[p] = guess_generator

        return cls(strat)

    @classmethod
    def recursive(cls, players=100):
        """
        After half of players have gone, subsequent players can be sure.
        """
        # This doesn't work because the probability of the first half gets worse
        def guess_generator(player, i, game):
            if player < players / 2:
                return 2*i
            else:
                return 2*i+1

        return cls(guess_generator)


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

