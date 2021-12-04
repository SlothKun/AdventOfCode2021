MAXLEN = 5

# Create an array full of zero
def createZeroArray(length=MAXLEN):
    return ['0' for i in range(length)]


# Check the last line and col of the board where a number has been marked
def checkWin(checkBoard, lineNb, colNb):
    # Check the column
    win = True
    for line in checkBoard:
        if line[colNb] == '0':
            win = False

    # Check the line
    filteredLine = list(filter(lambda bit: '1' in bit, checkBoard[lineNb]))
    win = True if len(filteredLine) == MAXLEN else win

    return win


with open("input.txt", 'r') as file:
    ### Get all datas
    numbers = file.readline().rstrip().split(',') # Get the list of numbers
    boards = [] # Init array containing boards
    file.readline() # Skip the 1st blank line

    boardData = { "board": [], "check": [] }

    # Add board and their checking matrice together in boards list
    for line in file:
        if len(line) != 1:
            boardData["board"].append(line.rstrip().split())
            boardData["check"].append(createZeroArray())
        else:
            boards.append(boardData)
            boardData = { "board": [], "check": [] }
    boards.append(boardData) # Save last registered board

    ### Check boards against numbers
    win = False
    winningBoard = []
    winningNb = 0
    alreadyWon = []

    for chosenNb in numbers:
        for board in boards:
            for lineNb in range(len(board["board"])):
                for colNb in range(len(board["board"][lineNb])):
                    # Check for winning board only if number is found and board not already won
                    if board["board"][lineNb][colNb] == chosenNb and board not in alreadyWon:
                        board["check"][lineNb][colNb] = '1'
                        if checkWin(board["check"], lineNb, colNb):
                            winningBoard = board
                            winningNb = int(chosenNb)
                            alreadyWon.append(board)

    ### Calculate the final score
    # Get sum of all unmarked numbers
    unmarkedSum = 0
    for lineNb in range(len(winningBoard["board"])):
        for colNb in range(len(winningBoard["board"][lineNb])):
            if winningBoard["check"][lineNb][colNb] == '0':
                unmarkedSum += int(winningBoard["board"][lineNb][colNb])

    # print final score
    print("Final score : ", unmarkedSum * winningNb)

