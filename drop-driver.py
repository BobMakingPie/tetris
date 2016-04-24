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
"......xox.",
"#####..x..",
"#######..#",
"#######..#",
"##########"
]
functions.printBoard(board)
board, last = functions.drop(board)
functions.printBoard(board)
print(last)
