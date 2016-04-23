import functions, random

## This is fuctionally the same as main.py, but uses controls that are harder to
## reach on a normal QWERTY keyboard.

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
                command = list(input("Command (type \"h\" for help): ").lower().strip())
                if not command:
                    print("Invalid command.")
                elif command[0] == "d":
                    instruct = True
                elif command[0] == "h":
                    print("Commands:")
                    print("Rotate: type r[direction]")
                    print("        Example:")
                    print("          To rotate to the right, type \"rr\"")
                    print()
                    print("Shift: type s[direction]")
                    print("       Example:")
                    print("         To shift to the left, type \"sl\"")
                    print()
                    print("Drop: type \"d\"")
                    print("      Drop piece without performing an action")
                    print()
                    print("Help: type \"h\"")
                    print("      Display this help text")

                elif command[0] == "r" and len(command) == 2:
                    if command[1] in ["r", "l"]:
                        instruct = True
                        direction = command[1]
                        board = functions.rotate(board, direction, pieceName)
                        functions.printBoard(board)
                    else:
                        print("Invalid rotate direction.")
                elif command[0] == "s" and len(command) == 2:
                    if command[1] in ["r", "l"]:
                        instruct = True
                        direction = command[1]
                        board = functions.shift(board, direction)
                        functions.printBoard(board)
                    else:
                        print("Invalid rotate direction.")
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
