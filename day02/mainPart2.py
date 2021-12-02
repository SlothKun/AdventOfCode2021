
depth = 0
hPos = 0
aim = 0

with open("input.txt", "r") as file:
    for line in file:
        data = line.split()
        instruction = data[0]
        value = int(data[1])
        if instruction == "forward":
            hPos += value
            depth += (aim * value)
        elif instruction == "up":
            aim -= value
        elif instruction == "down":
            aim += value

print("final result : ", depth * hPos)
