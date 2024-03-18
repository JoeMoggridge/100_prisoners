# This is a sample Python script.
import math
import statistics
import random


class JohnKramer:

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

    def ply(self, player, guess_generator):
        self.revealed = len(self.boxes) * [None]
        self.revealed_most_recently = None
        # guess a sequence of numbers
        for i in range(math.floor(len(self.boxes)/2)):
            guess = guess_generator(player, i, self.revealed_most_recently)
            if self.guess(player, guess):
                return True

        return False


class Strategy:

    def __init__(self, sequence_for_each_player: dict):
        self.strat = sequence_for_each_player

    def execute(self, game: JohnKramer):
        successes = 0
        failures = 0
        for player, guess_generator in self.strat.items():
            if game.ply(player, guess_generator):
                successes += 1
            else:
                failures +=1

        print(f"correct: {successes}, incorrect: {failures}")

        if successes == len(self.strat.keys()):
            print("strategy succeeded!")

        return successes, failures

    @classmethod
    def naive(cls, players=100):
        # build a naive strategy
        strat = {}
        for p in range(players):
            guesses = [x for x in range(players)]
            random.shuffle(guesses)
            def guess_generator(player, i,  revealed_most_recently):
                return guesses[i]

            strat[p] = guess_generator

        return cls(strat)

    @classmethod
    def chain(cls, players=100):
        # guess your own number first, then guess each revealed number
        strat = {}

        def guess_generator(player, i,  revealed_most_recently):
            if revealed_most_recently is None:
                return player
            else:
                return revealed_most_recently

        for p in range(players):
            strat[p] = guess_generator

        return cls(strat)

    @classmethod
    def prime(cls, players=100):
        # guess your own number first, then guess multiples of it
        strat = {}

        def guess_generator(player, i, revealed_most_recently):
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
        # split the problem in half. Each subsequent player can be sure.
        # This doesn't work because the probability of the first half gets worse
        strat = {}

        def guess_generator(player, i, revealed_most_recently):
            if player < players / 2:
                return 2*i
            else:
                return 2*i+1

        for p in range(players):
            strat[p] = guess_generator

        return cls(strat)


class Player:

    def __init__(self, number, strat):
        self.number = number
        self.strat = strat

    def get_next_guess(self, i, game:JohnKramer):
        return self.strat


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


def simulate_many_attempts(game_size, strategy, attempts):

    passed = 0
    results = []
    proportions = []
    for attempt in range(attempts):
        game = JohnKramer(game_size)
        results.append(strategy.execute(game))
        if results[attempt][0] == game_size:
            passed += 1

        proportions.append(results[attempt][0]/game_size)

    print(f"out of {attempts} attempts, {passed} succeeded")
    print(f"average proportion of players suceeeding = {statistics.mean(proportions)}")


if __name__ == '__main__':

    game_size= 100
    # create 100 players
    players = [i for i in range(game_size)]

    # print("\n==== naive ====")
    # # simulate strategy many times
    # simulate_many_attempts(game_size, Strategy.naive(game_size), 1000)

    print("\n==== chain====")
    simulate_many_attempts(game_size, Strategy.chain(game_size), 1000)

    # print("\n==== prime ====")
    # simulate_many_attempts(game_size, Strategy.prime(game_size), 1000)

    # print("\n==== recursive ====")
    # simulate_many_attempts(game_size, Strategy.recursive(game_size), 1000)

