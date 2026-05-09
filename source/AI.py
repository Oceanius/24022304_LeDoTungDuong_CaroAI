import math
import sys
import source.utils as utils

boardSize = 9

class GomokuAI:
    def __init__(self, depth = 5): # 4 lien tiep la thang nen depth can sau hon
        self.depth = depth
        self.boardMap = [[0 for i in range(boardSize)] for j in range(boardSize)]
        self.currentYCor = -1
        self.currentXCor = -1
        self.nextBound = {}
        self.boardValue = 0

        self.turn = 0
        self.lastPlayed = 0
        self.emptyCells = boardSize * boardSize
        self.patternDict = utils.createPatternDict()

        self.zobristTable = utils.createZobristTable(boardSize)
        self.rollingHash = 0
        self.transpositionTable = {}