#!/usr/bin/python
# adapted from: 
#   http://wordaligned.org/articles/drawing-chessboards
from PIL import Image, ImageDraw
from itertools import cycle

# def draw_chessboard(n=8, pixel_width=250):
#     """
#     Draw an n x n chessboard using PIL.
#     """
#     def sq_start(i):
#         """
#         Return the square corners, suitable for use in PIL drawings
#         """
#         return i*pixel_width / n

#     def square(i, j):
#         """
#         Return the square corners, suitable for use in PIL drawing
#         """
#         return map(sq_start, [i, j, i+1, j+1])
    
#     image = Image.new("RGB", (pixel_width, pixel_width))
#     draw_square = ImageDraw.Draw(image).rectangle
#     squares = (square(i,j)
#                 for i_start, j in zip(cycle((0, 1)), range(n))
#                 for i in range(i_start, n, 2))
#     # squaress = ((i_start, j) for i_start, j in zip(cycle((0, 1)), range(n)) for i in range(i_start, n, 2))
#     # print(squaress)
#     # print(squares)

#     for sqs in squaress:
#         print(sqs)
#     for sq in squares:
#         # print(sq)
#         draw_square(sq, fill='white')
#     image.show("chessboard.png")

def drawMaze(row, column, boxSize):
    listMaze = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1],
    [1,0,1,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,1,0,1,0,0],
    [1,1,1,1,1,1,1,1,1,1,1]
]
    """
    Draw an n x n chessboard using PIL.
    """

    def calcSqCoor(nth):
        return nth*boxSize
    
    def square(i, j):
        return map(calcSqCoor,[i, j, i+1, j+1])
    # width, height
    image = Image.new("RGB", (column*boxSize, row*boxSize))
    draw_square = ImageDraw.Draw(image).rectangle
    squares = (square(i,j) for j in range(row) for i in range(column))
    i=0
    j=0
    for sq in squares:
        # print(sq)

        if listMaze[i][j]==0:
            draw_square(sq, fill='white')
        else:
            draw_square(sq, fill='black')
        j+=1
        if j==11:
            i+=1
            j=0
    image.show()
# draw 8 x 8 chess board with 500 pixel as pixel width
# draw_chessboard(8)
# for i in range(11):
#     listRow = []
#     for j in range(11):
#         listRow.append(input())
#         print(listRow)
#     listMaze.append(listRow)
drawMaze(11,11,31)
