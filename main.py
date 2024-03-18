import statistics
from game import Game
from prisoner import Strategy

def simulate_many_attempts(game_size, strategy, attempts):
   # array to hold the output of each simulation
    results = []
    # out of all these attempts, how many times were the prisoners pardoned?
    pardoned = 0
    # for this attempt, what proportion of prisoners correctly guessed their number
    proportions = []

    for attempt in range(attempts):
        game = Game(game_size)
        prisoners_succeeded = game.play(strategy)
        proportions.append(prisoners_succeeded / game_size)
        results.append(prisoners_succeeded)
        if prisoners_succeeded == game_size:
            pardoned += 1

    print(f"out of {attempts} attempts, the prisoners were pardoned {pardoned} times")
    print(
        f"Average proportion of players suceeeding = {statistics.mean(proportions)}"
    )


if __name__ == '__main__':

    game_size= 100

    # create 100 players
    players = [i for i in range(game_size)]

    # print("\n==== naive ====")
    # # simulate strategy many times
    # simulate_many_attempts(game_size, Strategy.naive(game_size), 1000)

    print("\n==== chain====")
    simulate_many_attempts(game_size, Strategy.chain(), 1000)

    # print("\n==== prime ====")
    # simulate_many_attempts(game_size, Strategy.prime(game_size), 1000)

    # print("\n==== recursive ====")
    # simulate_many_attempts(game_size, Strategy.recursive(game_size), 1000)

