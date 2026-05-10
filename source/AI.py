from itertools import count
import math
import sys
import source.utils as utils

boardSize = 9

class GomokuAI:
    def __init__(self, depth = 5): # 4 lien tiep la thang nen depth can sau hon
        self.depth = depth
        self.boardMap = [[0 for i in range(boardSize)] for j in range(boardSize)]
        self.currentY = -1
        self.currentX = -1
        self.nextBound = {}
        self.boardValue = 0

        self.turn = 0
        self.lastPlayed = 0
        self.emptyCells = boardSize * boardSize
        self.patternDict = utils.createPatternDict()

        self.zobristTable = utils.createZobristTable(boardSize)
        self.rollingHash = 0
        self.transpositionTable = {}

    #Ve ban co , 0: o trong, 1: X, -1: O
    def printBoard(self):
        for i in range(boardSize):
            for j in range(boardSize):
                if self.boardMap[i][j] == 0:
                    print('.', end=' ')
                elif self.boardMap[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()

    #Kiem tra nuoc co hop le
    #neu state = False thi chi kiem tra xem co vuot qua bien hay khong
    #neu state = True: Kiemm tra xem o da co quan co hay chua
    def isValidMove(self, x, y, state = True):
        if x < 0 or x >= boardSize or y < 0 or y >= boardSize:
            return False
        if state and self.boardMap[y][x] != 0:
            return False
        return True
    
    #chuyen trang thai 1 o
    def makeMove(self, x, y, state):
        assert state in [-1, 0, 1], "Phai la -1, 0, or 1"
        if self.boardMap[y][x] == 0 and state != 0:
            self.emptyCells -= 1
        elif self.boardMap[y][x] != 0 and state == 0:
            self.emptyCells += 1
        self.boardMap[y][x] = state
        self.lastPlayed = state

    #Dem so quan co lien tiep theo huong dx, dy
    def countDirection(self, x, y, dx, dy, state):
        count = 0
        for i in range(1, 4):
            nx, ny = x + i * dx, y + i * dy
            if self.isValidMove(nx, ny) and self.boardMap[ny][nx] == state:
                count += 1
            else:
                break
        return count

    #Kiem tra xem co 4 quan co lien tiep hay khong
    def check4(self, x, y, state):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            count += self.countDirection(x, y, dx, dy, state)
            count += self.countDirection(x, y, -dx, -dy, state)
            if count >= 4:
                return True
        return False
    
    #Tra ve moi nuoc di hop le trong bang khi biet bao cac quan co
    #Sap xep theo gia tri tang dan
    def childNodes(self, bound):
        for pos in sorted(bound.items(), key=lambda item: item[1], reverse=True):
            yield pos[0]

    #Update bound sau moi nuoc di
    def updateBound(self, x, y, bound):
        if (x, y) in bound:
            bound.pop((x, y))
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if self.isValidMove(new_x, new_y) and (new_x, new_y) not in bound:
                bound[(new_x, new_y)] = 0
            new_x, new_y = x - dx, y - dy
            if self.isValidMove(new_x, new_y) and (new_x, new_y) not in bound:
                bound[(new_x, new_y)] = 0

    #Dem so pattern lien tiep theo huong dx, dy xung quanh o (x, y)
    def countPattern(self, x, y, pattern, score, bound, flag):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        lenPattern = len(pattern)
        count = 0
        for dx, dy in directions:
            if dx * dy == 0:
                maxStep = dx * min(4, y) + dy * min(4, x)
            elif dx == 1:
                maxStep = min(4, x, y)
            else:
                maxStep = min(4, x, boardSize - 1 - y)
            xStart = x - dx * maxStep
            yStart = y - dy * maxStep
            var = 0
            while var <= maxStep:
                curPattern = []
                index = 0
                nx = xStart + var * dx
                ny = yStart + var * dy
                while index < lenPattern and self.isValidMove(nx, ny, False) and self.boardMap[ny][nx] == pattern[index]:
                    if self.isValidMove(nx, ny):
                        curPattern.append((nx, ny))
                    nx += dx
                    ny += dy
                    index += 1
                if index == lenPattern:
                    count += 1
                    for pos in curPattern:
                        if pos not in bound:
                            bound[pos] = 0
                        bound[pos] += score * flag
                    var += index
                else:
                    var += 1
        return count
    
    #Tinh gia tri cua ban co sau moi nuoc di
    def evaluateBoard(self, x, y, boardValue, turn, bound):
        valueBefore = 0
        valueAfter = 0

        for pattern, score in self.patternDict.items():
            valueBefore += self.countPattern(x, y, pattern, abs(score), bound, -1) * score
            self.boardMap[y][x] = turn
            valueAfter += self.countPattern(x, y, pattern, abs(score), bound, 1) * score
            self.boardMap[y][x] = 0

        return boardValue - valueBefore + valueAfter
    
    def checkResult(self):
        if self.check4(self.currentX, self.currentY, self.lastPlayed) and self.lastPlayed != 0:
            return self.lastPlayed
        elif self.emptyCells <= 0:
            return 0
        else:
            return None
    
    #Minimax voi alpha-beta pruning
    def minimax(self, depth,boardValue, bound, alpha, beta, isMaximizing):
        if depth == 0 or self.checkResult() is not None:
            return boardValue

        if self.rollingHash in self.transpositionTable and self.transpositionTable[self.rollingHash][1] >= depth:
            return self.transpositionTable[self.rollingHash][0]
        
        if isMaximizing:
            maxEval = -math.inf

            for x, y in self.childNodes(bound):

                newBound = dict(bound)
                newEval =  self.evaluateBoard(x, y, boardValue, 1, newBound)

                self.boardMap[y][x] = 1
                self.rollingHash ^= self.zobristTable[y][x][0]
                self.updateBound(x, y, newBound)

                eval = self.minimax(depth - 1, newEval, newBound, alpha, beta, False)
                if eval > maxEval:
                    maxEval = eval
                    if depth == self.depth:
                        self.currentX, self.currentY = x, y
                        self.boardValue = newEval
                        self.nextBound = newBound
                alpha = max(alpha, eval)

                self.boardMap[y][x] = 0
                self.rollingHash ^= self.zobristTable[y][x][0]
                del newBound

                if beta <= alpha:
                    break

            utils.updateTranspositionTable(self.transpositionTable, self.rollingHash, maxEval, depth)

            return maxEval
        
        else:
            minEval = math.inf
            
            for x, y in self.childNodes(bound):

                newBound = dict(bound)
                newEval = self.evaluateBoard(x, y, boardValue, -1, newBound)

                self.boardMap[y][x] = -1
                self.rollingHash ^= self.zobristTable[y][x][1]
                self.updateBound(x, y, newBound)

                eval = self.minimax(depth - 1, newEval, newBound, alpha, beta, True)
                if eval < minEval:
                    minEval = eval
                    if depth == self.depth:
                        self.currentX, self.currentY = x, y
                        self.boardValue = newEval
                        self.nextBound = newBound
                beta = min(beta, eval)

                self.boardMap[y][x] = 0
                self.rollingHash ^= self.zobristTable[y][x][1]
                del newBound

                if beta <= alpha:
                    break

            utils.updateTranspositionTable(self.transpositionTable, self.rollingHash, minEval, depth)

            return minEval
        
    def firstMove(self):
        self.currentX, self.currentY = boardSize // 2, boardSize // 2
        self.makeMove(self.currentX, self.currentY, 1)

    def getWinner(self):
        if self.checkResult() == 1:
            return "AI wins!"
        elif self.checkResult() == -1:
            return "Player wins!"
        elif self.checkResult() == 0:
            return "It's a draw!"