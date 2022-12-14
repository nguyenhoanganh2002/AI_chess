"""
This is our main driver file.
"""
import pygame
import pygame as p
import ChessEngine
import  chess
from computer import Computer
from AI import AI

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30
IMAGES = {}

'''
Initialize a global dictionary of images. This is called exactly
once in the main
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))   

# comp1 = Computer(MAX_DEPTH=4, k1=0.01)
comp2 = Computer(MAX_DEPTH=3, k1=0.01, usemodel=True)
def getMove(fen, comp):
    brd = chess.Board(fen)
    move = comp.getCompMove(brd)
    return str(move)

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    print(gs.getFen())
    #print(len(gs.castleRightsLog))
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages() # Only do this once, because it's heavy

    # --------------------------------------------------------------------------
    while True:
        ranksToRows1 = {
            "1": 7, "2": 6, "3": 5, "4": 4,
            "5": 3, "6": 2, "7": 1, "8": 0
        }

        filesToCols1 = {
            "a": 0, "b": 1, "c": 2, "d": 3,
            "e": 4, "f": 5, "g": 6, "h": 7
        }
        print('\nComp1 thinking ... \n')
        ai = AI(chess.Board(gs.getFen()), 3)
        comp1Move = str(ai.calculate_ab(3))
        if comp1Move[0] == 'O':
            if len(comp1Move) == 3:
                # kingside
                startSq = (0, 4)
                endSq = (0, 6)
            else:
                # queenside
                startSq = (0, 4)
                endSq = (0, 2)
            tempMove = ChessEngine.Move(startSq, endSq, gs.board, isCastleMove=True)
            gs.makeMove(tempMove)
        else:
            startSq1 = (ranksToRows1[comp1Move[1]], filesToCols1[comp1Move[0]])
            endSq1 = (int(ranksToRows1[comp1Move[3]]), int(filesToCols1[comp1Move[2]]))
            gs.makeMove(ChessEngine.Move(startSq1, endSq1, gs.board))

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

        #----------------------
        print('\nComp2 thinking ... \n')
        comp2Move = getMove(gs.getFen(), comp2)
        print(comp2Move)
        if comp1Move[0] == 'O':
            if len(comp1Move) == 3:
                # kingside
                startSq = (0, 4)
                endSq = (0, 6)
            else:
                # queenside
                startSq = (0, 4)
                endSq = (0, 2)
            tempMove = ChessEngine.Move(startSq, endSq, gs.board, isCastleMove=True)
            gs.makeMove(tempMove)
        else:
            startSq2 = (ranksToRows1[comp2Move[1]], filesToCols1[comp2Move[0]])
            endSq2 = (int(ranksToRows1[comp2Move[3]]), int(filesToCols1[comp2Move[2]]))
            gs.makeMove(ChessEngine.Move(startSq2, endSq2, gs.board))

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    # --------------------------------------------------------------------------

    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of player clicks (two tuples: from, to)
    while running:
        clock.tick(100)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) pos of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): # user clicked the same square twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: # after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if validMoves[i] == move:

                            gs.makeMove(validMoves[i])
                            drawGameState(screen, gs)
                            clock.tick(MAX_FPS)
                            p.display.flip()

                            # get commputer move
                            compMove = getMove(gs.getFen(), comp2)
                            print(compMove)
                            if compMove[0] == 'O':
                                if len(compMove) == 3:
                                    # kingside
                                    startSq = (0, 4)
                                    endSq = (0, 6)
                                else:
                                    #queenside
                                    startSq = (0, 4)
                                    endSq = (0, 2)
                                tempMove = ChessEngine.Move(startSq, endSq, gs.board, isCastleMove=True)
                                gs.makeMove(tempMove)
                            else:
                                ranksToRows1 = {
                                    "1": 7, "2": 6, "3": 5, "4": 4,
                                    "5": 3, "6": 2, "7": 1, "8": 0
                                }

                                filesToCols1 = {
                                    "a": 0, "b": 1, "c": 2, "d": 3,
                                    "e": 4, "f": 5, "g": 6, "h": 7
                                }
                                startSq = (ranksToRows1[compMove[1]], filesToCols1[compMove[0]])
                                endSq = (int(ranksToRows1[compMove[3]]), int(filesToCols1[compMove[2]]))

                                tempMove = ChessEngine.Move(startSq, endSq, gs.board)
                                gs.makeMove(tempMove)

                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is 
                    #print(gs.castleRightsLog[-2].wks)
                    print(gs.castleRightsLog[-1].wks, gs.castleRightsLog[-1].bks, gs.castleRightsLog[-1].wqs, gs.castleRightsLog[-1].bqs)
                    gs.undoMove()
                    print(gs.castleRightsLog[-1].wks, gs.castleRightsLog[-1].bks, gs.castleRightsLog[-1].wqs, gs.castleRightsLog[-1].bqs)
                    #print(len(gs.castleRightsLog))
                    validMoves = gs.getValidMoves()
                    #print(gs.currentCastlingRight.wks)
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        # drawBoard(screen)

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    pygame.quit()
'''
Responsible for all the graphics within a current game state.
'''

def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting or move suggestion (later)
    drawPieces(screen, gs.board) # draw pieces on top of those squares

def drawBoard(screen):
    # the top left always light
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()