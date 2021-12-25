#!/usr/bin/env python3

class Alu:
    def __init__(self):
        self.initVar = {'w':0, 'x':0, 'y':0, 'z':0}
        self.var = self.initVar.copy()
        self.instructions = []
        self.digits = 0

    def __str__(self):
        return f"For digit {self.digits} : w={self.var['w']} - x={self.var['x']} - y={self.var['y']} - z={self.var['z']}"

    def resetVars(self):
        self.var = self.initVar.copy()

    def resetInstructions(self):
        self.instructions.clear()

    def loadInstructions(self, instructionPath):
        with open(instructionPath, 'r') as fileInput:
            for line in fileInput:
                self.instructions.append(line.split())
        print(f"File : {instructionPath} - {len(self.instructions)} instructions loaded.")

    def loadDigits(self, digits):
        self.digits = digits

    def applyOperation(self, operation, firstVar, value):
        if operation == "inp":
            self.var[firstVar] = self.digits[0]
            self.digits.pop(0)
        elif operation == "add":
            self.var[firstVar] += value
        elif operation == "mul":
            self.var[firstVar] *= value
        elif operation == "div":
            self.var[firstVar] = int(self.var[firstVar] / value)
        elif operation == "mod":
            self.var[firstVar] = self.var[firstVar] % value
        elif operation == "eql":
            self.var[firstVar] = int(self.var[firstVar] == value)

    def executeInstructions(self):
        for instruction in self.instructions:
            value = 0
            if len(instruction) == 3:
                if instruction[2].isalpha(): # if it's a letter
                    value = self.var[instruction[2]]
                else: # if it's a number
                    value = int(instruction[2])
            self.applyOperation(instruction[0], instruction[1], value)

#"""
def main():
    alu = Alu()
    validZValue = [0]
    targetZValueInstruction = {}
    for x in range(14, 0, -1):
        zValueTarget = validZValue.copy()
        validZValue = []
        alu.resetInstructions()
        alu.loadInstructions(f'divInput{x}.txt')
        for d in range(1, 10):
            for z in range(200000):
                alu.resetVars()
                alu.var['z'] = z
                alu.loadDigits([d])
                alu.executeInstructions()
                if alu.var['z'] in zValueTarget:
                    validZValue.append(z)
        targetZValueInstruction[x] = list(set(validZValue))
        print(len(targetZValueInstruction[x]))
    print("Final : ", targetZValueInstruction)

"""

def main():
    alu = Alu()
    alu.loadInstructions('divInput2.txt')
    for i in range(1,10):
        for z in range(9,18):
            alu.resetVars()
            alu.var['z'] = z
            alu.loadDigits([i for x in range(14)])
            alu.executeInstructions()
            #if alu.var['z'] in [5,6,7,8,9,10,11,12,13]:
            print(f"for digit {i} and starting z value {z} | Got z={alu.var['z']}")
"""

if __name__ == '__main__':
    main()
