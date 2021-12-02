
nbOfIncrease = 0
with open("input.txt", "r") as file:
    lines = file.readlines()
    input = int(lines[0])
    for line in lines:
        if int(line) > input:
            nbOfIncrease += 1
        input = int(line)

print(nbOfIncrease)
