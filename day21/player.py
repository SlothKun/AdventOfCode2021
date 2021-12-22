#!/usr/bin/env python3

class Player:
    def __init__(self, name, startingPos, dice):
        self.name = name
        self.position = startingPos - 1
        self.MAXPOS = 10
        self.score = 0
        self.winner = False
        self.dice = dice
        self.first = True

    def updateScore(self):
        self.score += self.position + 1

    def updatePos(self, rolledNb):
        print("pos before : ", self.position)
        #self.position += 1
        self.position = ((self.position + rolledNb) % self.MAXPOS)
        print("pos after : ", self.position)

        
    def checkWin(self):
        return True if self.score >= 1000 else False

    def play(self):
        rolledNb = self.dice.roll()
        print("RolledNb ", rolledNb)
        self.updatePos(rolledNb)
        self.updateScore()
        print(f"{self.name=} - {self.score=} - {self.position}")
        return self.checkWin()
