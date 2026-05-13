import pygame
import math

from gui.interface import GameUI
from source.AI import GomokuAI
from gui.button import Button
import source.utils as utils
import source.gomoku as gomoku

pygame.init()


def startGame():
    """Top-level loop. Restarts by looping, not recursing."""
    while True:
        pygame.init()
        ai   = GomokuAI()
        game = GameUI(ai)

        btn_black = Button(game.buttonSurf, 200, 290, "BLACK", 22)
        btn_white = Button(game.buttonSurf, 340, 290, "WHITE", 22)
        game.drawMenu()
        game.drawButtons(btn_black, btn_white, game.screen)

        # ── Wait for color choice ──────────────────────────────────────────
        while game.ai.turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    game.checkColorChoice(btn_black, btn_white, event.pos)
            pygame.display.update()

        # Draw the empty board
        game.screen.blit(game.board, (0, 0))
        pygame.display.update()

        # If AI goes first, make the opening move now
        if game.ai.turn == 1:
            game.ai.firstMove()
            color = game.colorState[1]
            game.drawPiece(color, game.ai.currentRow, game.ai.currentCol)
            pygame.display.update()
            game.ai.turn *= -1

        result = _mainLoop(game)

        if _endMenu(game):
            continue   # restart
        else:
            pygame.quit()
            return


def _mainLoop(game):
    """Play until someone wins or the board fills. Returns the result."""
    while True:
        turn = game.ai.turn

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            # ── AI move ───────────────────────────────────────────────────
            if turn == 1:
                row, col = gomoku.aiMove(game.ai)

                # Commit move to real board state
                game.ai.boardValue += game.ai._scoreDelta(row, col, 1)
                game.ai.makeMove(row, col, 1)
                game.ai.rollingHash ^= game.ai.zobristTable[row][col][0]
                game.ai.emptyCells  -= 1
                game.ai.currentRow, game.ai.currentCol = row, col

                game.drawPiece(game.colorState[1], row, col)
                pygame.display.update()
                game.ai.turn *= -1

                result = game.ai.checkResult()
                if result is not None:
                    return result

            # ── Human move ────────────────────────────────────────────────
            if turn == -1 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                move = utils.pos_pixel2map(event.pos[0], event.pos[1])
                row, col = move   

                if game.ai.isValidMove(col, row):
                    game.ai.boardValue += game.ai._scoreDelta(row, col, -1)
                    game.ai.updateBound(row, col, game.ai.nextBound)
                    game.ai.makeMove(row, col, -1)
                    game.ai.rollingHash ^= game.ai.zobristTable[row][col][1]
                    game.ai.emptyCells  -= 1
                    game.ai.currentRow, game.ai.currentCol = row, col

                    game.drawPiece(game.colorState[-1], row, col)
                    pygame.display.update()
                    game.ai.turn *= -1

                    result = game.ai.checkResult()
                    if result is not None:
                        return result

        pygame.display.update()


def _endMenu(game):
    """Show result overlay and YES/NO buttons. Returns True to restart."""
    game.drawResult()
    yes_btn = Button(game.buttonSurf, 200, 155, "YES", 18)
    no_btn  = Button(game.buttonSurf, 350, 155, "NO",  18)
    game.drawButtons(yes_btn, no_btn, game.screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_btn.rect.collidepoint(event.pos):
                    return True
                if no_btn.rect.collidepoint(event.pos):
                    return False
        pygame.display.update()


if __name__ == '__main__':
    startGame()