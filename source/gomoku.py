import math
import time
import pygame
from source.AI import GomokuAI
from gui.interface import GameUI
import source.utils as utils

pygame.init()


def aiMove(ai):
    startTime = time.time()
    ai.minimax(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    elapsed = time.time() - startTime
    print(f"AI move took {elapsed:.2f}s")

    row, col = ai.currentRow, ai.currentCol

    if not ai.isOnBoard(row, col) or ai.boardMap[row][col] != 0:
        print("AI chose an invalid cell — falling back to best candidate.")
        ai.nextBound.pop((row, col), None)
        if ai.nextBound:
            row, col = max(ai.nextBound, key=lambda rc: ai._threatLevel(rc[0], rc[1]))
            ai.currentRow, ai.currentCol = row, col
        else:
            print("No candidates left!")

    print(f"AI places at row={row}, col={col}")
    ai.updateBound(row, col, ai.nextBound)
    return row, col