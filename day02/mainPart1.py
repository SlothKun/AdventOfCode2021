
depth = 0
hPos = 0

with open("input.txt", "r") as file:
    for line in file:
        data = line.split()
        if data[0] == "forward":
            hPos += int(data[1])
        elif data[0] == "up":
            depth -= int(data[1])
        elif data[0] == "down":
            depth += int(data[1])

print("final result : ", depth * hPos)
