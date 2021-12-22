#!/usr/bin/env python3
MAXSCOREPARTONE = 1000
MAXSCOREPARTTWO = 27


class Player:
    def __init__(self, name, startingPos, dice):
        self.name = name
        self.position = startingPos - 1
        self.MAXPOS = 10
        self.score = 0
        self.dice = dice

    def updateScore(self):
        self.score += self.position + 1

    def updatePos(self, rolledNb):
        self.position = ((self.position + rolledNb) % self.MAXPOS)

    def checkWin(self):
        return True if self.score >= MAXSCOREPARTTWO else False

    def play(self):
        rolledNb = self.dice.roll()
        self.updatePos(rolledNb)
        self.updateScore()
        return self.checkWin()
