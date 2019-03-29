from PIL import Image, ImageDraw
from itertools import cycle
from queue import PriorityQueue, Queue
from math import *


def drawMaze(maxWindowSize, fileName, listOfPath, visited):
    fileObj = open(fileName, 'r')
    listMaze = [list(line[0:-1]) for line in fileObj]
    row = len(listMaze)
    column = len(listMaze[0])

    boxSize = maxWindowSize // max(row, column)

    def calcSqCoor(nth):
        return nth*boxSize

    def square(i, j):
        return map(calcSqCoor, [i, j, i+1, j+1])

    # width, height
    image = Image.new("RGB", (column*boxSize, row*boxSize))
    draw_square = ImageDraw.Draw(image).rectangle
    squares = (square(i, j) for j in range(row) for i in range(column))
    i = 0
    j = 0
    for sq in squares:
        if (j, i) in listOfPath:
            draw_square(list(sq), fill=(105, 195, 198))
        elif (j, i) in visited:
            draw_square(list(sq), fill='red')
        elif listMaze[i][j] == '0':
            draw_square(list(sq), fill='white')
        else:
            draw_square(list(sq), fill='black')
        j += 1
        if j == column:
            i += 1
            j = 0
    image.show()


def aStar(fileName, start, dest):
    nextTilesDict = {}
    fileObj = open(fileName, 'r')
    matrix = [list(line[0:-1]) for line in fileObj]

    visited = {}
    nextTiles = PriorityQueue()
    cTile = None

    def manhattanDist(point, dest):
        x1 = point[0]
        x2 = dest[0]
        y1 = point[1]
        y2 = dest[1]
        return abs(x2-x1)+abs(y2-y1)
        # return sqrt(pow(x2-x1,2)+pow(y2-y1,2))

    def getExpandable(tile):
        column = len(matrix[0])-1
        row = len(matrix)-1

        def valid(x, y):
            return (0 <= x <= column) and (0 <= y <= row)
        appendable = []
        # atas
        x = tile[0]
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(1)
        # kanan
        x = tile[0]+1
        y = tile[1]
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(2)
        # bawah
        x = tile[0]
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(3)
        # kiri
        x = tile[0]-1
        y = tile[1]
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(4)
        diagonal = False
        # kiri atas
        x = tile[0]-1
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(5)
        # kiri bawah
        x = tile[0]-1
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(6)
        # kanan atas
        x = tile[0]+1
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(7)
        # kanan bawah
        x = tile[0]+1
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(8)
        return appendable

    # putting starting tile into pQueue
    priority = 0 + manhattanDist(start, dest)
    tile = [start, 0, None]  # tile(point, distance)
    nextTiles.put([priority, tile, None])

    # assign cTile with head of pQueue
    found = False
    i = 0
    while (not nextTiles.empty() and not found):
        i += 1
        # if i==100:
        # break
        data = nextTiles.get()[1]  # (point, distance)
        parent = data[2]
        distance = data[1]
        nextTilePoint = data[0]

        visited[nextTilePoint] = parent  # parent
        cTile = nextTilePoint
        # print(cTile)
        if cTile == dest:
            found = True
            print(len(visited))
            print("Found path!")
            print("Distance: "+str(distance))
        else:
            expandables = getExpandable(cTile)
            if expandables:  # ada yang bisa di expand
                for expandable in expandables:

                    # print(' - ' + str(expandable))
                    tile = [expandable, distance+1, cTile]
                    prio = 0
                    if (abs(expandable[0]-cTile[0]) + abs(expandable[1]-cTile[1])) > 1:
                        prio = manhattanDist(
                            expandable, dest) + (distance+sqrt(2))
                    else:
                        prio = manhattanDist(expandable, dest) + (distance+1)
                    if expandable in nextTilesDict:  # kalau sudah ada di nextTiles
                        # hapus yang awal masukin yang baru
                        if prio <= nextTilesDict[expandable]:
                            nextTilesDict[expandable] = prio
                            for item in enumerate(nextTiles.queue):
                                if item[1][1][0] == expandable:
                                    nextTiles.queue.pop(item[0])
                                    break
                            nextTiles.put([prio, tile])
                    else:
                        nextTilesDict[expandable] = prio
                        nextTiles.put([prio, tile])
            else:  # tidak ada yang bisa di expand lagi
                if nextTiles.empty():
                    print("Path doesn't exist!")
    path = []
    while cTile:
        # print(cTile)
        path.append(cTile)
        cTile = visited[cTile]
    drawMaze(1200, 'input.txt', path, visited)


def BFS(fileName, start, dest):
    nextTilesDict = {}
    fileObj = open(fileName, 'r')
    matrix = [list(line[0:-1]) for line in fileObj]

    visited = {}
    nextTiles = Queue()
    cTile = None

    def manhattanDist(point, dest):
        x1 = point[0]
        x2 = dest[0]
        y1 = point[1]
        y2 = dest[1]
        return abs(x2-x1)+abs(y2-y1)
        # return sqrt(pow(x2-x1,2)+pow(y2-y1,2))

    def getExpandable(tile):
        column = len(matrix[0])-1
        row = len(matrix)-1

        def valid(x, y):
            return (0 <= x <= column) and (0 <= y <= row)
        appendable = []
        # atas
        x = tile[0]
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(1)
        # kanan
        x = tile[0]+1
        y = tile[1]
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(2)
        # bawah
        x = tile[0]
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(3)
        # kiri
        x = tile[0]-1
        y = tile[1]
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited:
            appendable.append((x, y))
            # print(4)
        diagonal = False
        # kiri atas
        x = tile[0]-1
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(5)
        # kiri bawah
        x = tile[0]-1
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(6)
        # kanan atas
        x = tile[0]+1
        y = tile[1]-1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(7)
        # kanan bawah
        x = tile[0]+1
        y = tile[1]+1
        if valid(x, y) and matrix[y][x] == '0' and (x, y) not in visited and diagonal:
            appendable.append((x, y))
            # print(8)
        return appendable

    # putting starting tile into Queue
    tile = [start, 0, None]  # tile(point, distance)
    nextTiles.put([tile, None])

    # assign cTile with head of pQueue
    found = False
    i = 0
    while (not nextTiles.empty() and not found):
        i += 1
        # if i==100:
        # break
        data = nextTiles.get()[0]  # (point, distance)
        parent = data[2]
        distance = data[1]
        nextTilePoint = data[0]

        visited[nextTilePoint] = parent  # parent
        cTile = nextTilePoint
        # print(cTile)
        if cTile == dest:
            found = True
            print(len(visited))
            print("Found path!")
            print("Distance: "+str(distance))
        else:
            expandables = getExpandable(cTile)
            if expandables:  # ada yang bisa di expand
                for expandable in expandables:

                    # print(' - ' + str(expandable))
                    tile = [expandable, distance+1, cTile]
                    if expandable in nextTilesDict:  # kalau sudah ada di nextTiles
                        # hapus yang awal masukin yang baru
                        for item in enumerate(nextTiles.queue):
                            if item[1][1][0] == expandable:
                                nextTiles.queue.pop(item[0])
                                break
                        nextTiles.put([tile])
                    else:
                        nextTiles.put([tile])
            else:  # tidak ada yan# g bisa di expand lagi
                if nextTiles.empty():
                    print("Path doesn't exist!")
    path = []
    while cTile:
        # print(cTile)
        path.append(cTile)
        cTile = visited[cTile]
    drawMaze(1200, 'input.txt', path, visited)


print("Ingin menjalankan algoritma apa?")
print()
print("1. AStar")
print("2. BFS")
print()
choice = int(input(">> "))
if choice == 1:
    aStar('input.txt', (0, 11), (40, 27))
elif choice == 2:
    BFS('input.txt', (0, 11), (40, 27))
else:
    print("Tidak ada pilihan tersebut")