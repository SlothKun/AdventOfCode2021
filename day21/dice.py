#!/usr/bin/env python3

class Dice:
    def __init__(self, face=100):
        self.face = face - 1 # Starting so we can roll
        self.MAXFACE = 100 # 0 to 99 -> 100
        self.rolled = 0

    def roll(self):
        number = 0
        self.rolled += 3
        for i in range(3):
            self.face = (self.face + 1) % self.MAXFACE # Increment by 1
            number += self.face+1
        return number
