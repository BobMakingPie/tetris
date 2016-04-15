import random

memes = "dank"

## i went through much pain and suffering to make this please enjoy it

def printBoard(board): ### Print the board, line for line.
    ### Input: board (list)
    for line in board:
        print(line)

def placeRandom(board, pieces, pieceNames): ### Choose a piece at random, then place it on the board.
    ### Inputs: board (list), pieces (dict), pieceNames(list)
    ### Returns: board (list), name (str)
    pieceName = pieceNames[random.randint(1, len(pieces)) - 1]
    piece = pieces[pieceName]
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
    return board, pieceName

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

def rotate(board, dir, pieceName): ### Rotate the active piece in the direction specified (or passes through if no direction specified) (in a really roundabout fashion)
    ### Inputs: board (list), dir (str), pieceName (str)
    ### Returns: board (list)
    ## Set turn direction as a boolean (I am lazy)
    if pieceName == "o":
        return board
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
        originCoords.append([(coord[0] - ocoord[0]), (coord[1] - ocoord[1])])

    ## Edit the coords to rotate in the direction
    if not turnRight:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [coord[1], - coord[0]]
    else:
        for i in range(len(originCoords)):
            coord = originCoords[i]
            originCoords[i] = [- coord[1], coord[0]]

    ## Translate the coords back to (0, 0) as origin
    coords = []
    for coord in originCoords:
        coords.append([(coord[0] + ocoord[0]), (coord[1] + ocoord[1])])

    ## Place each x back, rotated
    for coord in coords:
        line = list(board[coord[1]])
        line[coord[0]] = "x"
        board[coord[1]] = "".join(line)
    return board

def drop(board): ### Drops the active piece by 1.
    ### Inputs: board (list)
    ### Outputs: board (list)
    ## Store current board in preProcessBoard (for some reason simple assig.
    ## does not work)
    preProcessBoard = []
    for i in board:
        preProcessBoard.append(i)

    ## Find lines where piece is located
    pieceLines = []
    for i in range(len(board)):
        line = board[i]
        if "x" in line or "o" in line:
            pieceLines.append(i)

    ## Find which part of each line the piece is on
    piece = {}
    for i in pieceLines:
        line = board[i]
        if "o" in line:
            if not "x" in line:
                firstInstance = line.index("o")
                lastInstance = line.index("o")
            else:
                firstInstance = None
                if line.index("x") < line.index("o"):
                    firstInstance = line.index("x")
                else:
                    firstInstance = line.index("o")

                lastInstance = None
                if line[::-1].index("x") < line[::-1].index("o"):
                    lastInstance = 9 - line[::-1].index("x")
                else:
                    lastInstance = line.index("o")
        else:
            firstInstance = line.index("x")
            lastInstance = 9 - line[::-1].index("x")
        piece[i] = [firstInstance, lastInstance]

    ## Drop the piece
    pieceBot = piece[pieceLines[-1]]
    if "#" in board[pieceLines[-1] + 1][pieceBot[0]:pieceBot[1] + 1]:
        ## Refuse to drop if it is the last possible drop
        last = True
    else:
        ## If a drop is possible, do so
        last = False
        for line in pieceLines[::-1]:
            linePiece = piece[line]
            if linePiece[0] != linePiece[1]:
                ## If piece line length > 1
                toDrop = preProcessBoard[line][linePiece[0]:linePiece[1] + 1]
                heal = list(board[line])
                heal[linePiece[0]:linePiece[1] + 1] = "." * (linePiece[1] + 1 - linePiece[0])
                board[line] = "".join(heal)
            else:
                toDrop = preProcessBoard[line][linePiece[0]]
                heal = list(board[line])
                heal[linePiece[0]] = "."
                board[line] = "".join(heal)
            print(toDrop)
            lineList = list(board[line + 1])
            print(lineList[linePiece[0]:linePiece[1] + 1])
            lineList[linePiece[0]:linePiece[1] + 1] = toDrop
            board[line + 1] = "".join(lineList)
        ## Heal line above dropped piece
        prevline = list(preProcessBoard[pieceLines[0]])
        pieceTop = piece[pieceLines[0]]

        prevline[pieceTop[0]:pieceTop[1] + 1] = "." * (pieceTop[1] + 1 - pieceTop[0])
        board[pieceLines[0]] = "".join(prevline)

    ## Return the board
    return board, last
