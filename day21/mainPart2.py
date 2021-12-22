#!/usr/bin/env python3
import itertools as it
from functools import cache, lru_cache
import timeit

diceOutcomes = []
playersNb = [0, 1]

def loadPlayers():
    playerList = []
    with open('input.txt', 'r') as inputFile:
        for index, line in enumerate(inputFile):
            line = line.rstrip().split()
            playerList.append({"name": index, "pos": int(line[-1]), "score":0})
    return playerList

def initDiceOutcomes():
    global diceOutcomes
    throws = list(it.product(*[[1, 2, 3] for _ in range(3)])) # Create each possible outcome for 3 times rolled Dice
    diceOutcomes = [sum(x) for x in throws] # get each outcome possible

def updatePos(position, diceOutcome):
    return (position + diceOutcome) % 10

def updateScore(score, position):
    return score + position + 1

@cache
def simulateGame(player, p1Score, p2Score, p1Pos, p2Pos):
    if p1Score >= 21:
        return (1, 0)
    if p2Score >= 21:
        return (0, 1)

    p1Win, p2Win = 0, 0

    for outcome in diceOutcomes:
        if player == 0:
            tmpP1Pos = (p1Pos + outcome - 1) % 10 + 1
            tmpP1Score = p1Score + tmpP1Pos

            scores = simulateGame(playersNb[player-1], tmpP1Score, p2Score, tmpP1Pos, p2Pos)
            p1Win += scores[0]
            p2Win += scores[1]
        else:
            tmpP2Pos = (p2Pos + outcome - 1) % 10 + 1
            tmpP2Score = p2Score + tmpP2Pos

            scores = simulateGame(playersNb[player-1], p1Score, tmpP2Score, p1Pos, tmpP2Pos)
            p1Win += scores[0]
            p2Win += scores[1]
    return (p1Win, p2Win)

def main():
    initDiceOutcomes()
    playerList = loadPlayers()
    print(f"{diceOutcomes=}")
    print(f"{playerList=}")
    p1Win, p2Win = simulateGame(0, playerList[0]['score'], playerList[1]['score'], playerList[0]['pos'], playerList[1]['pos'])
    print(f"{p1Win=}")
    print(f"{p2Win=}")


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    print("Time : ", timeit.default_timer() - start)
