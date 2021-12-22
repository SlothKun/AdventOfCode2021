#!/usr/bin/env python3
from player import Player
from dice import Dice

class Board:
    def __init__(self, dice):
        self.playerList = []
        self.dice = dice

    def loadPlayers(self):
        with open('input.txt', 'r') as inputFile:
            for line in inputFile:
                line = line.rstrip().split()
                print(line[1], " - ", line[-1])
                self.playerList.append(Player(line[1], int(line[-1]), self.dice))

    def run(self):
        while True:
        #for i in range(3):
            for playerIndex, player in enumerate(self.playerList):
                print("-----")
                if player.play():
                    print(self.dice.rolled)
                    print(self.playerList[playerIndex-1].score)
                    print(f"Score : {self.dice.rolled * self.playerList[playerIndex-1].score}")
                    return


def main():
    dice = Dice()
    board = Board(dice)
    board.loadPlayers()
    board.run()

if __name__ == '__main__':
    main()
