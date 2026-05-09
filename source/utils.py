import random
import uuid

##### For managing the interface #####
SIZE = 540 #size of the board image
PIECE = 32 #size of the single pieces
N = 15
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N-1)

def pixel_conversion(list_points, target):
    # point of the list from where start the search
    index = int((len(list_points)-1)//2) 

    while True:
        if target < list_points[0]:
            index = 0
            break
        elif target >= list_points[-1]:
            index = len(list_points)-2
            break

        elif list_points[index] > target:
            if list_points[index-1] <= target:
                index -= 1
                break
            else:
                index -= 1

        elif list_points[index] <= target:
            if list_points[index+1] > target:
                break
            else:
                index += 1
    
    return index


# Transform pygame pixel to boardMap coordinates
def pos_pixel2map(x, y):
    start = int(MARGIN - GRID//2)
    end = int(SIZE - MARGIN + GRID//2)
    list_points = [p for p in range(start, end+1, int(GRID))]

    i = pixel_conversion(list_points, y)
    j = pixel_conversion(list_points, x)
    return (i,j)

# Transform boardMap to pygame pixel coordinates
def pos_map2pixel(i, j):
    return (MARGIN + j * GRID - PIECE/2, MARGIN + i * GRID - PIECE/2)


def create_mapping():
    pos_mapping = {}
    for i in range(N):
        for j in range(N):
            spacing = [r for r in range(MARGIN, SIZE-MARGIN+1, int(GRID))]
            pos_mapping[(i,j)] = (spacing[j],spacing[i])
    
    return pos_mapping



#### Pattern scores ####
def createPatternDict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # chuoi 4
        patternDict[(x, x, x, x)] = 1000000 * x
        # chuoi 3 khong chan 2 dau
        patternDict[(0, x, x, x, 0)] = 100000 * x
        patternDict[(x, x, 0, x)] = 50000 * x
        patternDict[(x, 0, x, x)] = 50000 * x
        # chuoi 3 chan 1 dau
        patternDict[(0, x, x, x, y)] = 10000 * x
        patternDict[(y, x, x, x, 0)] = 10000 * x
        # chuoi 3 chan 2 dau
        #patternDict[(y, x, x, x, y)] = 0
        # chuoi 2 khong chan 2 dau
        patternDict[(0, x, x, 0)] = 1000 * x
        patternDict[(0, x, 0, x, 0)] = 1000 * x
        # chuoi 2 chan 1 dau
        patternDict[(0, x, x, y)] = 100 * x
        patternDict[(y, x, x, 0)] = 100 * x
        #chuoi thieu 2 o giua
        patternDict[(x, 0, 0, x)] = 500 * x
        # chuoi 2 chan 2 dau
        #patternDict[(y, x, x, y)] = 0
        x += 2
    return patternDict



##### Zobrist Hashing #####
def createZobristTable(boardSize):
    zTable = [[[uuid.uuid4().int  for _ in range(2)] \
                        for j in range(boardSize)] for i in range(boardSize)]
    return zTable

def updateTranspositionTable(table, hash, score, depth):
    table[hash] = [score, depth]