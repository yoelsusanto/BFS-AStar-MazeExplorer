from PIL import Image, ImageDraw, ImageFont
from itertools import cycle
from queue import PriorityQueue, Queue
from math import *


def drawMaze(maxWindowSize, fileName, listOfPath, visited):
    fileObj = open(fileName, 'r')
    listMaze = [list(line.strip('\n')) for line in fileObj]
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
            draw_square(list(sq), fill=(51,255,0))
        elif (j, i) in visited:
            draw_square(list(sq), fill=(255,102,0))
        elif listMaze[i][j] == '0':
            draw_square(list(sq), fill='white')
        else:
            draw_square(list(sq), fill='black')
        j += 1
        if j == column:
            i += 1
            j = 0
    image.show(title='Maze')


def aStar(fileName, start, dest):
    nextTilesDict = {}
    fileObj = open(fileName, 'r')
    matrix = [list(line.strip()) for line in fileObj]
    column = len(matrix[0])-1
    row = len(matrix)-1
    
    visited = {}
    nextTiles = PriorityQueue()
    cTile = None
    
    if not ((0 <= start[0] <= column) and (0 <= start[1] <= row) and (0 <= dest[0] <= column) and (0 <= dest[1] <= row) and matrix[start[1]][start[0]]=='0' and matrix[dest[1]][dest[0]]=='0'):
        print("Input tidak valid!")
    else:
        def manhattanDist(point, dest):
            x1 = point[0]
            x2 = dest[0]
            y1 = point[1]
            y2 = dest[1]
            return abs(x2-x1)+abs(y2-y1)

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
        nextTiles.put([priority, tile])

        # assign cTile with head of pQueue
        found = False
        while (not nextTiles.empty() and not found):
            data = nextTiles.get()[1]  # (point, distance)
            parent = data[2]
            distance = data[1]
            nextTilePoint = data[0]

            visited[nextTilePoint] = parent  # parent
            cTile = nextTilePoint
            if cTile == dest:
                found = True
                print("Found path!")
                print("Distance: "+str(distance))
            else:
                expandables = getExpandable(cTile)
                if expandables:  # ada yang bisa di expand
                    for expandable in expandables:
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
        if found:
            path = []
            while cTile:
                # print(cTile)
                path.append(cTile)
                cTile = visited[cTile]
            drawMaze(1200, 'input.txt', path, visited)


def BFS(fileName, start, dest):
    nextTilesDict = {}
    fileObj = open(fileName, 'r')
    matrix = [list(line.strip()) for line in fileObj]
    column = len(matrix[0])-1
    row = len(matrix)-1
    if not ((0 <= start[0] <= column) and (0 <= start[1] <= row) and (0 <= dest[0] <= column) and (0 <= dest[1] <= row) and matrix[start[1]][start[0]]=='0' and matrix[dest[1]][dest[0]]=='0'):
        print("Input tidak valid!")
    else:
        visited = {}
        nextTiles = PriorityQueue()
        cTile = None

        def manhattanDist(point, dest):
            x1 = point[0]
            x2 = dest[0]
            y1 = point[1]
            y2 = dest[1]
            return abs(x2-x1)+abs(y2-y1)

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
        nextTiles.put((0,tile))

        # assign cTile with head of pQueue
        found = False
        while (not nextTiles.empty() and not found):
            data = nextTiles.get()[1]  # (point, distance)
            parent = data[2]
            distance = data[1]
            nextTilePoint = data[0]

            visited[nextTilePoint] = parent  # parent
            cTile = nextTilePoint
            if cTile == dest:
                found = True
                print("Found path!")
                print("Distance: "+str(distance))
            else:
                expandables = getExpandable(cTile)
                if expandables:  # ada yang bisa di expand
                    for expandable in expandables:
                        tile = [expandable, distance+1, cTile]
                        if expandable in nextTilesDict:  # kalau sudah ada di nextTiles
                            if distance <= nextTilesDict[expandable]:
                                nextTilesDict[expandable]=distance
                                # hapus yang awal masukin yang baru
                                for item in enumerate(nextTiles.queue):
                                    if item[1][1][0] == expandable:
                                        nextTiles.queue.pop(item[0])
                                        break
                                nextTiles.put((0,tile))
                        else:
                            nextTilesDict[expandable]=distance
                            nextTiles.put((0,tile))
                else:  # tidak ada yan# g bisa di expand lagi
                    if nextTiles.empty():
                        print("Path doesn't exist!")
        if found:
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
    x1,y1,x2,y2 = [int(x) for x in input("Masukkan koordinat pintu masuk dan keluar(x1 y1 x2 y2):").split()]
    aStar('input.txt', (x1, y1), (x2, y2))
elif choice == 2:
    x1,y1,x2,y2 = [int(x) for x in input("Masukkan koordinat pintu masuk dan keluar(x1 y1 x2 y2):").split()]
    BFS('input.txt', (x1, y1), (x2, y2))
else:
    print("Tidak ada pilihan tersebut")