import random

def printBoard(board): ### Print the board, line for line.
    ### Input: board (list)
    for line in board:
        print(line)

def placeRandom(board, pieces, pieceNames): ### Choose a piece at random, then place it on the board.
    ### Inputs: board (list), pieces (dict), pieceNames(list)
    ### Returns: board (list)
    piece = pieces[pieceNames[random.randint(1, len(pieces)) - 1]]
    for i in range(len(piece)):
        line = piece[i]
        if line[0] == ".":
            line = line[1:]
            boardLine = list(board[i + 1])
            boardLine[4:4 + len(line)] = line
            board[i + 1] = "".join(boardLine)
        else:
            boardLine = list(board[i + 1])
            boardLine[3:3 + len(line)] = line
            board[i + 1] = "".join(boardLine)
    return board

def hashify(board): ### Turn the active (movable) piece to hashes.
    ### Input: board (list)
    ### Returns: board (list)
    for i in range(len(board)):
        line = list(board[i])
        while "x" in line:
            line[line.index("x")] = "#"
        while "o" in line:
            line[line.index("o")] = "#"
        board[i] = "".join(line)
    return board

def rotate(board, dir): ### Rotate the active piece in the direction specified (or passes through if no direction specified) (in a really roundabout fashion)
    ### Inputs: board (list), dir (str)
    ### Returns: board (list)
    ## Set turn direction as a boolean (I am lazy)
    if dir.lower().strip() == "r":
        turnRight = True
    elif dir.lower().strip() == "l":
        turnRight = False
    else:
        return board

    ## Find the coords for the active piece, relative to (0, 0) and remove all instances of x
    coords = []
    occord = []
    for i in range(len(board)):
        filler = "."
        if i == 0:
            filler = "/"
        line = list(board[i])
        while "x" in line:
            coords.append([line.index("x"), i])
            line[line.index("x")] = filler
        if "o" in line:
            ocoord = [line.index("o"), i]
        board[i] = "".join(line)

    ## Find the coords for the active piece, with o as the origin
    originCoords = []
    for coord in coords:
        originCoords.append([(coord[0] - ocoord[0]), - (coord[1] - ocoord[1])])

    ## Edit the coords to rotate in the direction
    if turnRight:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [coord[1], - coord[0]]
    else:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [- coord[1], coord[0]]
    print(originCoords)

    ## Translate the coords back to (0, 0) as origin
    # TODO figure out correct reversal of neg/pos
    coords = []
    for coord in originCoords:
        coords.append([(coord[0] + ocoord[0]), (coord[1] + ocoord[1])])
    print(coords)

    ## Place each x back, rotated
    for coord in coords:
        line = list(board[coord[1]])
        line[coord[0]] = "x"
        board[coord[1]] = "".join(line)

    return board
