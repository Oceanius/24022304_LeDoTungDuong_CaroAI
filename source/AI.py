import math
import source.utils as utils

SIZE = 15  # board dimension

# ── Coordinate convention ──────────────────────────────────────────────────
# Every internal method uses (row, col).
# boardMap[row][col]
# isOnBoard(row, col)  ← always row first
# ──────────────────────────────────────────────────────────────────────────

DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]   # (drow, dcol)


class GomokuAI:
    def __init__(self, depth=5):
        self.depth = depth
        self.boardMap = [[0] * SIZE for _ in range(SIZE)]

        self.currentRow = -1
        self.currentCol = -1
        self.nextBound = {}      # set of (row,col) candidate moves
        self.boardValue = 0

        self.turn = 0            # which colour the human chose; set by UI
        self.lastPlayed = 0      # 1 or -1, last piece placed on the real board
        self.emptyCells = SIZE * SIZE

        self.patternDict = utils.createPatternDict()
        self.zobristTable = utils.createZobristTable(SIZE)
        self.rollingHash = 0
        self.transpositionTable = {}

    @property
    def currentX(self):
        return self.currentCol

    @currentX.setter
    def currentX(self, v):
        self.currentCol = v

    @property
    def currentY(self):
        return self.currentRow

    @currentY.setter
    def currentY(self, v):
        self.currentRow = v

    # ── Board helpers ──────────────────────────────────────────────────────

    def printBoard(self):
        sym = {0: '.', 1: 'X', -1: 'O'}
        for row in self.boardMap:
            print(' '.join(sym[c] for c in row))

    def isOnBoard(self, row, col):
        return 0 <= row < SIZE and 0 <= col < SIZE

    def isValidMove(self, x, y, checkEmpty=True):
        col, row = x, y
        if not self.isOnBoard(row, col):
            return False
        if checkEmpty and self.boardMap[row][col] != 0:
            return False
        return True

    def makeMove(self, row, col, player):
        assert player in (-1, 0, 1)
        self.boardMap[row][col] = player
        self.lastPlayed = player

    # ── Win detection ──────────────────────────────────────────────────────

    def _countDir(self, row, col, drow, dcol, player):
        """Count consecutive `player` pieces in one direction, not counting (row,col)."""
        n = 0
        r, c = row + drow, col + dcol
        while self.isOnBoard(r, c) and self.boardMap[r][c] == player:
            n += 1
            r += drow
            c += dcol
        return n

    def check4(self, row, col, player):
        """True if (row,col) is part of 4+ consecutive `player` pieces."""
        for drow, dcol in DIRECTIONS:
            total = (1
                     + self._countDir(row, col,  drow,  dcol, player)
                     + self._countDir(row, col, -drow, -dcol, player))
            if total >= 4:
                return True
        return False

    def updateBound(self, row, col, bound):
        """Add empty neighbours of (row,col) to the candidate set."""
        bound.pop((row, col), None)
        for drow, dcol in DIRECTIONS:
            for sign in (1, -1):
                r, c = row + sign * drow, col + sign * dcol
                if self.isOnBoard(r, c) and self.boardMap[r][c] == 0 and (r, c) not in bound:
                    bound[(r, c)] = 0

    def _scanLine(self, row, col, drow, dcol, length):
        """
        Return the sequence of board values along a line of `length` cells
        starting at (row,col) in direction (drow,dcol).
        Returns None if any cell is off-board.
        """
        cells = []
        r, c = row, col
        for _ in range(length):
            if not self.isOnBoard(r, c):
                return None
            cells.append(self.boardMap[r][c])
            r += drow
            c += dcol
        return cells

    def _scoreBoard(self):
        """
        Full board evaluation from player 1's perspective.
        Positive = good for AI (player 1), negative = good for human (player -1).
        Scans every window of the right length in all 4 directions.
        """
        score = 0
        for pattern, value in self.patternDict.items():
            L = len(pattern)
            for drow, dcol in DIRECTIONS:
                for row in range(SIZE):
                    for col in range(SIZE):
                        window = self._scanLine(row, col, drow, dcol, L)
                        if window is None:
                            continue
                        # Match for player 1
                        if all(
                            (p == 1 and w == 1) or
                            (p == -1 and w == -1) or
                            (p == 0 and w == 0)
                            for p, w in zip(pattern, window)
                        ):
                            score += value
                        # Match for player -1 (mirror: swap 1 and -1 in pattern)
                        if all(
                            (p == 1 and w == -1) or
                            (p == -1 and w == 1) or
                            (p == 0 and w == 0)
                            for p, w in zip(pattern, window)
                        ):
                            score -= value
        return score

    def _scoreDelta(self, row, col, player):
        """
        Incremental evaluation: score change from placing `player` at (row,col).
        Cell must be empty. Temporarily places, scores the affected windows, restores.
        """
        before = self._scoreAffected(row, col)
        self.boardMap[row][col] = player
        after = self._scoreAffected(row, col)
        self.boardMap[row][col] = 0
        return after - before

    def _scoreAffected(self, row, col):
        """
        Score only the windows that pass through (row,col).
        Much faster than full board rescan.
        """
        score = 0
        for pattern, value in self.patternDict.items():
            L = len(pattern)
            for drow, dcol in DIRECTIONS:
                for offset in range(L):
                    sr = row - offset * drow
                    sc = col - offset * dcol
                    window = self._scanLine(sr, sc, drow, dcol, L)
                    if window is None:
                        continue
                    # player 1
                    if all(
                        (p == 1 and w == 1) or
                        (p == -1 and w == -1) or
                        (p == 0 and w == 0)
                        for p, w in zip(pattern, window)
                    ):
                        score += value
                    # player -1
                    if all(
                        (p == 1 and w == -1) or
                        (p == -1 and w == 1) or
                        (p == 0 and w == 0)
                        for p, w in zip(pattern, window)
                    ):
                        score -= value
        return score

    # ── Move ordering ──────────────────────────────────────────────────────

    def _threatLevel(self, row, col):
        """
        Heuristic priority for move ordering.
        Returns the maximum consecutive run of either player through this cell.
        """
        best = 0
        for player in (1, -1):
            for drow, dcol in DIRECTIONS:
                run = (self._countDir(row, col,  drow,  dcol, player) +
                       self._countDir(row, col, -drow, -dcol, player))
                best = max(best, run)
        return best

    def _sortedCandidates(self, bound):
        return sorted(bound.keys(), key=lambda rc: self._threatLevel(rc[0], rc[1]), reverse=True)

    # ── Game result ────────────────────────────────────────────────────────

    def checkResult(self):
        if (self.lastPlayed != 0
                and self.isOnBoard(self.currentRow, self.currentCol)
                and self.check4(self.currentRow, self.currentCol, self.lastPlayed)):
            return self.lastPlayed
        if self.emptyCells <= 0:
            return 0
        return None

    def getWinner(self):
        r = self.checkResult()
        if r == 1:  return "AI wins!"
        if r == -1: return "Player wins!"
        if r == 0:  return "It's a draw!"
        return ""

    # ── Minimax ────────────────────────────────────────────────────────────

    def minimax(self, depth, boardValue, bound, alpha, beta, isMaximizing):
        if depth == 0 or not bound:
            return boardValue

        cached = self.transpositionTable.get(self.rollingHash)
        if cached is not None and cached[1] >= depth:
            return cached[0]

        if isMaximizing:
            maxEval = -math.inf
            for row, col in self._sortedCandidates(bound):
                delta   = self._scoreDelta(row, col, 1)
                newEval = boardValue + delta

                self.boardMap[row][col] = 1
                self.rollingHash ^= self.zobristTable[row][col][0]

                if self.check4(row, col, 1):
                    self.boardMap[row][col] = 0
                    self.rollingHash ^= self.zobristTable[row][col][0]
                    if depth == self.depth:
                        self.currentRow, self.currentCol = row, col
                        self.boardValue = newEval
                        self.nextBound = dict(bound)
                    return math.inf

                newBound = dict(bound)
                self.updateBound(row, col, newBound)
                ev = self.minimax(depth - 1, newEval, newBound, alpha, beta, False)

                self.boardMap[row][col] = 0
                self.rollingHash ^= self.zobristTable[row][col][0]

                if ev > maxEval:
                    maxEval = ev
                    if depth == self.depth:
                        self.currentRow, self.currentCol = row, col
                        self.boardValue = newEval
                        self.nextBound = newBound

                alpha = max(alpha, ev)
                if beta <= alpha:
                    break

            utils.updateTranspositionTable(self.transpositionTable, self.rollingHash, maxEval, depth)
            return maxEval

        else:
            minEval = math.inf
            for row, col in self._sortedCandidates(bound):
                delta   = self._scoreDelta(row, col, -1)
                newEval = boardValue + delta

                self.boardMap[row][col] = -1
                self.rollingHash ^= self.zobristTable[row][col][1]

                if self.check4(row, col, -1):
                    self.boardMap[row][col] = 0
                    self.rollingHash ^= self.zobristTable[row][col][1]
                    if depth == self.depth:
                        self.currentRow, self.currentCol = row, col
                        self.boardValue = newEval
                        self.nextBound = dict(bound)
                    return -math.inf

                newBound = dict(bound)
                self.updateBound(row, col, newBound)
                ev = self.minimax(depth - 1, newEval, newBound, alpha, beta, True)

                self.boardMap[row][col] = 0
                self.rollingHash ^= self.zobristTable[row][col][1]

                if ev < minEval:
                    minEval = ev
                    if depth == self.depth:
                        self.currentRow, self.currentCol = row, col
                        self.boardValue = newEval
                        self.nextBound = newBound

                beta = min(beta, ev)
                if beta <= alpha:
                    break

            utils.updateTranspositionTable(self.transpositionTable, self.rollingHash, minEval, depth)
            return minEval

    # ── Game start ─────────────────────────────────────────────────────────

    def firstMove(self):
        """AI goes first: place at center, fully initialise state."""
        row, col = SIZE // 2, SIZE // 2
        self.currentRow, self.currentCol = row, col
        self.makeMove(row, col, 1)
        self.updateBound(row, col, self.nextBound)
        self.emptyCells -= 1
        self.rollingHash ^= self.zobristTable[row][col][0]
        self.boardValue = self._scoreBoard()