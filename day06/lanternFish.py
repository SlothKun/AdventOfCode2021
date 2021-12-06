#!/usr/bin/env python3

DEFAULT_DAYS = 6

class LanternFish:
    def __init__(self, daysLeft):
        self.daysLeft = daysLeft

    def resetTimer(self):
        self.daysLeft = DEFAULT_DAYS

    def decreaseTimer(self):
        self.daysLeft -= 1

    def getDaysLeft(self):
        return self.daysLeft
