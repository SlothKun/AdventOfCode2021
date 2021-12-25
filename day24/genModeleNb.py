#!/usr/bin/env python3

# Following This explanation : https://github.com/dphilipson/advent-of-code-2021/blob/master/src/days/day24.rs#L124
# I defined that, with my input, I have these operations : (i = input | number start at 0 and end at 13)
#
# i4 = i3 - 1
# i5 = i2 - 5
# i8 = i7 + 3
# i9 = i6 + 7
# i11 = i10 + 2
# i12 = i1 - 2
# i13 = i0 + 4
#
# Then i only have to Try all combinaison while keeping the highest input possible for each for part 1
# and the lowest from part 2

def mainMax():
    inputs = [0 for i in range(14)]
    for i in range(1, 10):
        if inputs[4] <= i-1 < 10:
            inputs[4] = i-1
            inputs[3] = i
        if inputs[5] <= i-5 < 10:
            inputs[5] = i-5
            inputs[2] = i
        if inputs[8] <= i+3 < 10:
            inputs[8] = i+3
            inputs[7] = i
        if inputs[9] <= i+7 < 10:
            inputs[9] = i+7
            inputs[6] = i
        if inputs[11] <= i+2 < 10:
            inputs[11] = i+2
            inputs[10] = i
        if inputs[12] <= i-2 < 10:
            inputs[12] = i-2
            inputs[1] = i
        if inputs[13] <= i+4 < 10:
            inputs[13] = i+4
            inputs[0] = i

    result = "".join(map(str, inputs))
    print("Max model : ", result)

def mainMin():
    inputs = [9 for i in range(14)]
    for i in range(1, 10):
        if 0 < i-1 < inputs[4]:
            inputs[4] = i-1
            inputs[3] = i
        if 0 < i-5 < inputs[5]:
            inputs[5] = i-5
            inputs[2] = i
        if 0 < i+3 < inputs[8]:
            inputs[8] = i+3
            inputs[7] = i
        if 0 < i+7 < inputs[9]:
            inputs[9] = i+7
            inputs[6] = i
        if 0 < i+2 < inputs[11]:
            inputs[11] = i+2
            inputs[10] = i
        if 0 < i-2 < inputs[12]:
            inputs[12] = i-2
            inputs[1] = i
        if 0 < i+4 < inputs[13]:
            inputs[13] = i+4
            inputs[0] = i

    result = "".join(map(str, inputs))
    print("Min model : ", result)

if __name__ == '__main__':
    mainMax()
    mainMin()
