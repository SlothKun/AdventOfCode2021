#!/usr/bin/env python3

class ImageEnhancer:
    def __init__(self, inputFilePath):
        self.inputPath = inputFilePath
        self.image = []
        self.algoString = ""

    def loadData(self):
        with open(self.inputPath, 'r') as inputFile:
            inputFile = inputFile.readlines()
            self.algoString = inputFile[0].rstrip()
            for line in inputFile[2:]:
                imgLine = [0, 0]
                parsedLine = [0 if char == '.' else 1 for char in line.rstrip()]
                print(f"{len(parsedLine)=}")
                imgLine += parsedLine
                imgLine += [0, 0]
                self.image.append(imgLine)
                print(f"{len(imgLine)=}")
            # Insert Empty Lines to prep the infinite case
            emptyLine = [0 for i in range(len(self.image[0]))]
            for i in range(2):
                self.image.insert(0, emptyLine)
                self.image.append(emptyLine)





def main():
    imageEnhancer = ImageEnhancer("testInput.txt")
    imageEnhancer.loadData()

if __name__ == '__main__':
    main()
