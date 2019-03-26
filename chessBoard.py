from PIL import Image, ImageDraw
from itertools import cycle

def drawMaze(maxWindowSize, fileName):
    fileObj = open(fileName,'r')
    listMaze = [list(line[0:-1]) for line in fileObj]
    row = len(listMaze)
    column = len(listMaze[0])

    boxSize = maxWindowSize // max(row,column)
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
        if listMaze[i][j]=='0':
            draw_square(list(sq), fill='white')
        else:
            draw_square(list(sq), fill='black')
        j+=1
        if j==column:
            i+=1
            j=0
    image.show()

drawMaze(600,'input.txt')