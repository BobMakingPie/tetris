import random

memes = "dank"

## ram doesn't like me calling my module "functions.py"
## but i dont wanna change it

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

    # I just noticed "dir" is an inbuilt function but I don't want to find/replace
    # it for fear of this entire thing commiting suicide

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
    # Yes, the code in this one is very messy as I lost track between sessions
    #   After pondering for a bit I've found a much more efficient solution
    #   that's way more elegant but I've already written this and it works soooo

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

    ## Detect which spots the piece will fall into and validate
    pieceBot = piece[pieceLines[-1]]
    coordsCheck = []
    left = None
    right = None
    for i in pieceLines:
        if left != None:
            if left[0] >= piece[i][0]:
                left = [piece[i][0], i]
            if right[0] <= piece[i][1]:
                right = [piece[i][1], i]
        else:
            left = [piece[i][0], i]
            right = [piece[i][1], i]
    for i in range(pieceBot[0], pieceBot[1] + 1):
        coordsCheck.append([i, pieceLines[-1] + 1])
    if left[0] < coordsCheck[0][0]:
        coordsCheck.append([left[0], left[1] + 1])
    if right[0] > sorted(i[0] for i in coordsCheck)[-1]:
        coordsCheck.append([right[0], right[1] + 1])

    futurePiece = []
    for i in coordsCheck:
        futurePiece.append(board[i[1]][i[0]])

    # Drop the piece
    if "#" in futurePiece:
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
            lineList = list(board[line + 1])
            lineList[linePiece[0]:linePiece[1] + 1] = toDrop
            board[line + 1] = "".join(lineList)
        ## Heal line above dropped piece
        prevline = list(preProcessBoard[pieceLines[0]])
        pieceTop = piece[pieceLines[0]]

        prevline[pieceTop[0]:pieceTop[1] + 1] = "." * (pieceTop[1] + 1 - pieceTop[0])
        board[pieceLines[0]] = "".join(prevline)

    ## Return the board
    return board, last

def shift(board, direction): ### Shift the active piece by 1 in direction specified
    ### Inputs: board (list), dir (str)
    ### Outputs: board (list)
    ## Find lines of piece
    pieceLines = []
    for i in range(len(board)):
        line = board[i]
        if "x" in line or "o" in line:
            pieceLines.append(i)

    ## Find parts of line etc etc (totally not copy pasted from above) (yes i couldve made another function for this but im lazy)
    piece = {}
    for i in pieceLines:
        o = None
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
            o = line.index("o")
        else:
            firstInstance = line.index("x")
            lastInstance = 9 - line[::-1].index("x")
        piece[i] = [firstInstance, lastInstance, o]

    ## Heal parts of board where current piece is
    for i in pieceLines:
        line = list(board[i])
        cols = piece[i]
        line[cols[0]:cols[1] + 1] = "." * (cols[1] + 1 - cols[0])
        board[i] = "".join(line)

    ## Numerically shift (?) piece
    if direction == "l":
        for i in pieceLines:
            piece[i][:2] = [m - 1 for m in piece[i][:2]]
            if piece[i][2] != None:
                piece[i][2] -= 1
    else:
        for i in pieceLines:
            piece[i][:2] = [m + 1 for m in piece[i][:2]]
            if piece[i][2] != None:
                print("meme")
                piece[i][2] += 1

    ## "Render" shifted piece on to board
    for i in pieceLines:
        line = list(board[i])
        line[piece[i][0]:piece[i][1] + 1] = "x" * (piece[i][1] + 1 - piece[i][0])
        board[i] = "".join(line)

    ## Replace anchor point (known as the "o")
    for i in pieceLines:
        if piece[i][2] != None:
            line = list(board[i])
            line[piece[i][2]] = "o"
            board[i] = "".join(line)

    return board
