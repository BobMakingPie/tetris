import functions, random

if functions.memes == "dank":
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
    board = ["//////////"] + [".........."] * 15 + ["##########"]

    ##### Start game logic
    touchingTop = False # Change when a "#" is found in the top line, at the end
    while not touchingTop:
        ## Place piece on the board (on the 4th dot from left)
        board, pieceName = functions.placeRandom(board, pieces, pieceNames)
        functions.printBoard(board)

        last = False
        while not last:
            instruct = False
            while not instruct:
                ## Rotate/move piece
                command = input("Command (type \"h\" for help): ").lower().strip()
                if not command:
                    print("Invalid command.")
                elif command == "'":
                    instruct = True
                elif command == "h":
                    print("Commands:")
                    print("Rotate right: type \"]\"")
                    print()
                    print("Rotate left: type \"[\"")
                    print()
                    print("Shift right: type \".\"")
                    print()
                    print("Shift left: type \",\"")
                    print()
                    print("Drop: \"'\"")
                    print("      Drop piece without performing an action")
                    print()
                    print("Help: type \"h\"")
                    print("      Display this help text")
                elif command == "]":
                    instruct = True
                    direction = "r"
                    board = functions.rotate(board, direction, pieceName)
                    functions.printBoard(board)
                elif command == "[":
                    instruct = True
                    direction = "l"
                    board = functions.rotate(board, direction, pieceName)
                    functions.printBoard(board)
                elif command == ".":
                    instruct = True
                    direction = "r"
                    board = functions.shift(board, direction)
                    functions.printBoard(board)
                elif command == ",":
                    instruct = True
                    direction = "l"
                    board = functions.shift(board, direction)
                    functions.printBoard(board)
                else:
                    print("Invalid command.")

            ## Drop piece one unit
            board, last = functions.drop(board)
            functions.printBoard(board)
        ## When piece cannot be dropped, render it as hashes and continue
        board = functions.hashify(board)

        ## Check for line clears
        while "##########" in board[:-1]:
            ## Clear lines and insert new
            no = board[:-1].index("##########")
            del board[no]
            board.insert(1, "..........")

        ## Trigger game over
        if "#" in board[1]:
            touchingTop = True
    functions.printBoard(board)
    print("##################")
    print("### Game over! ###")
    print("##################")
else:
    print("nah bro")
