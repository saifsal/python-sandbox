
from random import randint

MAX = 10
ROUNDS = 10


class Bonus:
    NO = 0
    STRIKE = 1
    SPARE = -1


def bonus(f: tuple, n: int) -> int:
    if max(f) == MAX:
        r = n + Bonus.STRIKE
        return r, r
    elif sum(f) == MAX:
        return Bonus.SPARE, 0
    else:
        return Bonus.NO, 0


def play_frame() -> tuple:
    one = randint(0, MAX)
    two = randint(0, MAX - one)

    assert(one + two <= MAX)

    return (one, two)


def play_game() -> list:
    game = [play_frame() for _ in range(ROUNDS)]

    r, _ = bonus(game[-1], 0)

    if r != Bonus.NO:
        three = randint(0, MAX)
        game[-1] = (game[-1][0], game[-1][1], three)

    return game


def compute_bonuses(p: list) -> list:
    b = [0] * (len(p) - 1)
    c = 0

    for i in range(len(p) - 2, -1, -1):
        b[i], c = bonus(p[i], c)

    return b


def count_points(p: list) -> int:
    total = 0
    b = compute_bonuses(p)

    for i in range(len(p) - 1):
        if b[i] >= 3:
            total += 30
        elif b[i] == 2:
            total += 20 + sum(p[i + 2])
        elif b[i] == 1:
            total += 10 + sum(p[i + 1])
        elif b[i] == Bonus.SPARE:
            total += 10 + p[i + 1][0]
        else:
            total += sum(p[i])

    total += sum(p[-1])

    return total


# game = [(10, 0), (10, 0), (10, 0), (10, 0), (10, 0), (10, 0),
#        (10, 0), (10, 0), (10, 0), (10, 0, 10)]

game = play_game()

print(game)

print(count_points(game))
