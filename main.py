import functions, random

##### Place pieces in a dictionary
## Define lists/dictionary
pieceNames = ["i", "j", "l", "o", "s", "t", "z"]
pieces = {}

## Initialise the dictionary with blank lists (ceebs typing it)
for name in pieceNames:
    pieces[name] = []

## Define names as lists of the piece in a dictionary
for name in pieceNames:
    with open("./pieces/" + name + ".txt") as pieceFile:
        for line in pieceFile:
            pieces[name].append(line.strip("\n"))

##### Prepare the board
## Create blank board
board = [".........."] * 15 + ["##########"]

## Print blank board
functions.printBoard(board)

##### Start game logic
touchingTop = False # Change when a "#" is found in the top line, at the end
while not touchingTop:
    ## Place piece on the board (on the 4th dot from left)
    
