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
"..x.......",
"..x.......",
"..o.......",
"..x.......",
"#######...",
"####.##.##",
"#######.##",
"##########"
]
functions.printBoard(board)
board = functions.shift(board, "l")
functions.printBoard(board)
board = functions.shift(board, "l")
functions.printBoard(board)
