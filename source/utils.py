import uuid

##### For managing the interface #####
SIZE = 540   # size of the board image
PIECE = 32   # size of a single piece
N = 15
MARGIN = 23
GRID = (SIZE - 2 * MARGIN) / (N - 1)


def pixel_conversion(list_points, target):
    index = int((len(list_points) - 1) // 2)
    while True:
        if target < list_points[0]:
            index = 0
            break
        elif target >= list_points[-1]:
            index = len(list_points) - 2
            break
        elif list_points[index] > target:
            if list_points[index - 1] <= target:
                index -= 1
                break
            else:
                index -= 1
        elif list_points[index] <= target:
            if list_points[index + 1] > target:
                break
            else:
                index += 1
    return index


def pos_pixel2map(x, y):
    """Transform pygame pixel coords to boardMap (row, col)."""
    start = int(MARGIN - GRID // 2)
    end = int(SIZE - MARGIN + GRID // 2)
    list_points = [p for p in range(start, end + 1, int(GRID))]
    row = pixel_conversion(list_points, y)
    col = pixel_conversion(list_points, x)
    return (row, col)


def pos_map2pixel(row, col):
    """Transform boardMap (row, col) to pygame pixel coords."""
    return (MARGIN + col * GRID - PIECE / 2, MARGIN + row * GRID - PIECE / 2)


def create_mapping():
    pos_mapping = {}
    spacing = [r for r in range(MARGIN, SIZE - MARGIN + 1, int(GRID))]
    for i in range(N):
        for j in range(N):
            pos_mapping[(i, j)] = (spacing[j], spacing[i])
    return pos_mapping


#### Pattern scores ####
# Patterns are tuples of cell values:
#   p  = the player whose patterns we're scoring  (1 or -1)
#   0  = empty cell
#  -p  = opponent piece (used as a blocker in some patterns)
#
# All score values are positive. The evaluator applies +score for player 1
# and -score for player -1.

def createPatternDict():
    p = 1   # placeholder; evaluator substitutes actual player value

    patterns = {
        # 4 in a row = instant win
        (p, p, p, p): 1_000_000,

        # Open 3 — one away from a forced win
        (0, p, p, p, 0): 100_000,

        # Broken 3 — skip in the middle, still very dangerous
        (p, p, 0, p): 50_000,
        (p, 0, p, p): 50_000,

        # Half-open 3 — one end blocked
        (0, p, p, p, -1): 10_000,
        (-1, p, p, p, 0): 10_000,

        # Open 2
        (0, p, p, 0): 1_000,
        (0, p, 0, p, 0): 1_000,

        # Half-open 2
        (0, p, p, -1): 100,
        (-1, p, p, 0): 100,

        # Separated pair
        (p, 0, 0, p): 500,
    }
    return patterns


##### Zobrist Hashing #####
def createZobristTable(boardSize):
    # [row][col][player_index]  player_index: 0=player1, 1=player-1
    return [[[uuid.uuid4().int for _ in range(2)]
             for _ in range(boardSize)]
            for _ in range(boardSize)]


def updateTranspositionTable(table, hash_key, score, depth):
    table[hash_key] = (score, depth)