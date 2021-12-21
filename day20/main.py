#!/usr/bin/env python3
import pprint


pp = pprint.PrettyPrinter(indent=2)
CYCLE = 2 # Part 1
CYCLE = 50 # Part 2

class ImageEnhancer:
    def __init__(self, inputFilePath):
        self.inputPath = inputFilePath
        self.image = []
        self.outsidePixel = '0'
        self.algoString = ""

    def parseLine(self, line):
        return ['0' if char == '.' else '1' for char in line]

    def increaseImageSize(self):
        emptyCol = [self.outsidePixel]
        newImage = []
        for line in self.image:
            line = emptyCol + line + emptyCol
            newImage.append(line)
        # Insert Empty Lines to prep the infinite case
        outsideLine = [self.outsidePixel for i in range(len(newImage[0]))]
        for i in range(1):
            newImage.insert(0, outsideLine)
            newImage.append(outsideLine)
        self.image = newImage

    def loadData(self):
        with open(self.inputPath, 'r') as inputFile:
            inputFile = inputFile.readlines()
            self.algoString = self.parseLine(inputFile[0].rstrip())
            for line in inputFile[2:]:
                parsedLine = self.parseLine(line.rstrip())
                self.image.append(parsedLine)

    def getBinNb(self, pixelPos):
        pixelBin = ""
        for x in range(pixelPos[0]-1, pixelPos[0]+2):
            for y in range(pixelPos[1]-1, pixelPos[1]+2):
                if x < 0 or x >= len(self.image) or \
                   y < 0 or y >= len(self.image[0]):
                    pixelBin += self.outsidePixel
                else:
                    pixelBin += self.image[x][y]
        return pixelBin

    def getOutputPixel(self, binNb):
        return self.algoString[int(binNb, 2)]

    def setOutsidePixel(self):
        if self.outsidePixel == '0':
            self.outsidePixel = self.algoString[0]
        else:
            self.outsidePixel = self.algoString[-1]

    def enhance(self):
        self.increaseImageSize()
        enhancedImage = []
        for lineIndex, line in enumerate(self.image):
            enhancedLine = []
            for pixelIndex, pixel in enumerate(line):
                pixelBinNb = self.getBinNb((lineIndex, pixelIndex))
                enhancedLine.append(self.getOutputPixel(pixelBinNb))
            enhancedImage.append(enhancedLine)
        self.image = enhancedImage
        #pp.pprint(self.image)
        #print("----------")
        self.setOutsidePixel()

    def countLitPixels(self):
        pixelCount = 0
        for line in self.image:
            for pixel in line:
                pixelCount += 1 if pixel == "1" else 0
        print(f"{pixelCount=}")


def main():
    imageEnhancer = ImageEnhancer("input.txt")
    imageEnhancer.loadData()
    for i in range(CYCLE):
        imageEnhancer.enhance()
    imageEnhancer.countLitPixels()

if __name__ == '__main__':
    main()
