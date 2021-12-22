#!/usr/bin/env python3

class Dice:
    def __init__(self):
        self.face = 99 # Starting so we can roll
        self.MAXFACE = 100 # 0 to 99 -> 100
        self.rolled = 0

    def roll(self):
        numbers = 0
        self.rolled += 3
        for i in range(3):
            self.face = (self.face + 1) % self.MAXFACE # Increment by 1
            numbers += self.face+1
            #numbers.append(self.face+1) # because we start at 0
        return numbers
