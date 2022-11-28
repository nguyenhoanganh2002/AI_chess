"""
Storing all the information about the current state of a chess game.
Determining the valid moves at the current state.
"""

from tracemalloc import start

def isInside(r, c):
    return 0 <= r and r <= 7 and 0 <= c and c <= 7

class GameState():
    def __init__(self):
        self.board = [
            # "--" = blank space
            # b, w = color (black or white)
            # R, N, B, Q, K, p: represent type of piece
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []

        self.enpassantPossible = ()

        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(True, True, True, True)]
        self.halfmove = 0




    def makeMove(self, move):
        if move.pieceMoved[1] != 'p' and move.pieceCaptured == "--":
            self.halfmove += 1
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove # swap players turn
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        # en passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # kingside castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else: # queenside castle
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        # update castling rights - whenever it is a rook or a king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved[1] != 'p' and move.pieceCaptured == "--":
                self.halfmove -= 1

        # undo enpassant move
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol] = "--"
            self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantPossible = (move.endRow, move.endCol)
        # undo 2 square pawn advance
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ()
        # undo castling rights
        self.castleRightsLog.pop()
        castleRights = self.castleRightsLog[-1]
        #self.currentCastlingRight = castleRights
        self.currentCastlingRight = CastleRights(castleRights.wks, castleRights.bks, castleRights.wqs, castleRights.bqs)
        # undo castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # kingside
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                self.board[move.endRow][move.endCol-1] = "--"
            else: # queenside
                self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = []
        possibleMoves = self.getAllPossibleMoves()
        for r in range(8):
            for c in range(8):
                if self.board[r][c][1] == 'K':
                    if (self.whiteToMove and self.board[r][c][0] == 'w') or (not self.whiteToMove and self.board[r][c][0] == 'b'):
                        # pass
                        self.getCastleMoves(r, c, moves) 

        for move in possibleMoves:
            flag = True
            self.makeMove(move)
            currentPossibleMoves = self.getAllPossibleMoves()
            for curMove in currentPossibleMoves:
                startRow = curMove.startRow
                startCol = curMove.startCol
                endRow = curMove.endRow
                endCol = curMove.endCol
                if ((self.board[startRow][startCol][0] == 'w' and self.board[endRow][endCol] == "bK") or (self.board[startRow][startCol][0] == 'b' and self.board[endRow][endCol] == "wK")):
                    flag = False
            if flag == True:
                moves.append(move)        
            self.undoMove()

        self.enpassantPossible = tempEnpassantPossible 
        self.currentCastlingRight = tempCastleRights
        return moves

    '''
    Determine if the enemy can attack the square (r, c)
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove 
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                if self.board[move.startRow][move.startCol][1] == 'p' and move.endCol == move.startCol:
                    continue
                return True
        return False
    '''
    All moves without considering checks
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
                    elif piece == 'B':
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'N':
                        self.getKnightMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == 'K':
                        self.getKingMoves(r, c, moves)
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if isInside(r-1, c) and self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and isInside(r-2, c) and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if isInside(r-1, c-1):
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if isInside(r-1, c+1):
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        else:   
            if isInside(r+1, c) and self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and isInside(r+2, c) and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if isInside(r+1, c-1):
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if isInside(r+1, c+1):
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        # left 
        for i in range(1,8):
            if isInside(r, c-i):
                if self.board[r][c-i] == "--":
                    # print(r, c, r, c-i)
                    moves.append(Move((r, c), (r, c-i), self.board))
                    # print(r,c-i)
                else:
                    if (self.board[r][c-i][0] == 'w' and not self.whiteToMove) or (self.board[r][c-i][0] == 'b' and self.whiteToMove):
                        # print(r, c, r, c-i)
                        moves.append(Move((r, c), (r, c-i), self.board))
                    break
            else: 
                break

        # right
        for i in range(1,8):
            if isInside(r, c+i):
                if self.board[r][c+i] == "--":
                    moves.append(Move((r, c), (r, c+i), self.board))
                else:
                    if (self.board[r][c+i][0] == 'w' and not self.whiteToMove) or (self.board[r][c+i][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r, c+i), self.board))
                    break
            else: 
                break

        # up
        for i in range(1,8):
            if isInside(r-i, c):
                if self.board[r-i][c] == "--":
                    moves.append(Move((r, c), (r-i, c), self.board))
                else:
                    if (self.board[r-i][c][0] == 'w' and not self.whiteToMove) or (self.board[r-i][c][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r-i, c), self.board))
                    break
            else: 
                break
        # down
        for i in range(1,8):
            if isInside(r+i, c):
                if self.board[r+i][c] == "--":
                    moves.append(Move((r, c), (r+i, c), self.board))
                else:
                    if (self.board[r+i][c][0] == 'w' and not self.whiteToMove) or (self.board[r+i][c][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r+i, c), self.board))
                    break
            else: 
                break

    def getBishopMoves(self, r, c, moves):
        # South West
        for i in range(1,8):
            if isInside(r-i,c-i):
                if self.board[r-i][c-i] == "--":
                    moves.append(Move((r, c), (r-i, c-i), self.board))
                else:
                    if (self.board[r-i][c-i][0] == 'w' and not self.whiteToMove) or (self.board[r-i][c-i][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r-i, c-i), self.board))
                    break
            else:
                break

        # South East
        for i in range(1,8):
            if isInside(r-i,c+i):
                if self.board[r-i][c+i] == "--":
                    moves.append(Move((r, c), (r-i, c+i), self.board))
                else:
                    if (self.board[r-i][c+i][0] == 'w' and not self.whiteToMove) or (self.board[r-i][c+i][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r-i, c+i), self.board))
                    break
            else:
                break

        # North West
        for i in range(1,8):
            if isInside(r+i,c-i):
                if self.board[r+i][c-i] == "--":
                    moves.append(Move((r, c), (r+i, c-i), self.board))
                else:
                    if (self.board[r+i][c-i][0] == 'w' and not self.whiteToMove) or (self.board[r+i][c-i][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r+i, c-i), self.board))
                    break
            else:
                break

        # North East
        for i in range(1,8):
            if isInside(r+i,c+i):
                if self.board[r+i][c+i] == "--":
                    moves.append(Move((r, c), (r+i, c+i), self.board))
                else:
                    if (self.board[r+i][c+i][0] == 'w' and not self.whiteToMove) or (self.board[r+i][c+i][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (r+i, c+i), self.board))
                    break
            else:
                break

    def getKnightMoves(self, r, c, moves):
        dx = [-1,-1,-2,-2,+1,+1,+2,+2]
        dy = [-2,+2,-1,+1,-2,+2,-1,+1]
        for i in range(8):
            u = r + dx[i]
            v = c + dy[i]
            if isInside(u, v):
                if self.board[u][v] == "--":
                    moves.append(Move((r, c), (u, v), self.board))
                else:
                    if (self.board[u][v][0] == 'w' and not self.whiteToMove) or (self.board[u][v][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (u, v), self.board))
        
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        dx = [-1,-1,-1,+0,+0,+1,+1,+1]
        dy = [-1,+0,+1,-1,+1,-1,+0,+1]
        for i in range(8):
            u = r + dx[i]
            v = c + dy[i]
            if isInside(u, v):
                if self.board[u][v] == "--":
                    moves.append(Move((r, c), (u, v), self.board))
                else:
                    if (self.board[u][v][0] == 'w' and not self.whiteToMove) or (self.board[u][v][0] == 'b' and self.whiteToMove):
                        moves.append(Move((r, c), (u, v), self.board))

    '''
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if (not self.squareUnderAttack(r, c+1)) and (not self.squareUnderAttack(r, c+2)):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if (not self.squareUnderAttack(r, c-1)) and (not self.squareUnderAttack(r, c-2)) and (not self.squareUnderAttack(r, c-3)):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))            

    def getNoMoves(self, r, c, moves):
        pass

    def getFen(self):
        """
        piece placement
        active color
        castling avail
        en passant target square
        halfmove:
        fullmove
        :return:
        """
        s = ""
        cnt = 0
        for row in range(0, 8):
            cnt = 0
            for col in range(0, 8):
                if self.board[row][col][0] == 'b':
                    if cnt != 0:
                        s += str(cnt)
                    s += self.board[row][col][1].lower()
                    cnt = 0
                elif self.board[row][col][0] == 'w':
                    if cnt != 0:
                        s += str(cnt)
                    s += self.board[row][col][1].upper()
                    cnt = 0
                else:
                    cnt += 1
            if cnt != 0:
                s += str(cnt)

            if row != 7:
                s += '/'

        s += ' '
        if self.whiteToMove:
            s += 'w '
        else:
            s += 'b '

        if (not self.currentCastlingRight.wks and not self.currentCastlingRight.wqs and not self.currentCastlingRight.bks and not self.currentCastlingRight.bqs):
            s += '- '
        else:
            if self.currentCastlingRight.wks:
                s += 'K'
            if self.currentCastlingRight.wqs:
                s += 'Q'
            if self.currentCastlingRight.bks:
                s += 'k'
            if self.currentCastlingRight.bqs:
                s += 'q'

        s += ' '
        if len(self.moveLog) == 0:
            s += '-'
        else:
            mv = self.moveLog[-1]
            if mv.pieceMoved[1] != 'p':
                s += '-'
            else:
                if mv.startRow == 1 and mv.endRow == 3:
                    s += mv.colsToFiles[mv.endCol]
                    s += str(6)
                elif mv.startRow == 6 and mv.endRow == 4:
                    s += mv.colsToFiles[mv.endCol]
                    s += str(3)
                else:
                    s += '-'
        s += ' '
        s += str(self.halfmove)

        s += ' '
        s += str(((len(self.moveLog)) // 2) + 1)

        return s

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # maps keys to value
    # key : value
    # row in chess: ranks, col in chess: files
    # we have to map our 8x8 board to a chessboard

    ranksToRows = {
        "1": 7, "2": 6, "3": 5, "4": 4,
        "5": 3, "6": 2, "7": 1, "8": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {
        "a": 0, "b": 1, "c": 2, "d": 3,
        "e": 4, "f": 5, "g": 6, "h": 7 
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True 
        # en passant
        self.isEnpassantMove = False
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]    
        