import functions
board = [
"//////////",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"..........",
"......x...",
"#####.ox..",
"#######x.#",
"#######..#",
"##########"
]
functions.printBoard(board)
board, last = functions.drop(board)
functions.printBoard(board)
print(last)
