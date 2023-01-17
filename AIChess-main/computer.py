import chess
import numpy as np
from model import LiteModel
from tensorflow import keras
import time
from const import Const


class Computer:
    values = {chess.PAWN: 100,
              chess.KNIGHT: 330,
              chess.BISHOP: 320,
              chess.ROOK: 510,
              chess.QUEEN: 900,
              chess.KING: 10000}
    piece_square_table = {
            #panwn
            1: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                20, 20, 25, 35, 35, 25, 20, 20,
                15, 15, 20, 25, 25, 20, 15, 15,
                0, 10, 10, 20, 20, 10, 10, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],

            # Knight
            2: [
                -50, -40, -30, -30, -30, -30, -40, -50,
                -40, -20, 0, 0, 0, 0, -20, -40,
                -30, 0, 10, 15, 15, 10, 0, -30,
                -30, 5, 15, 20, 20, 15, 5, -30,
                -30, 0, 15, 20, 20, 15, 0, -30,
                -30, 5, 10, 15, 15, 10, 5, -30,
                -40, -20, 0, 5, 5, 0, -20, -40,
                -50, -40, -30, -30, -30, -30, -40, -50,
            ],

            # bishop
            3: [
                -20, -10, -10, -10, -10, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 10, 10, 5, 0, -10,
                -10, 5, 5, 10, 10, 5, 5, -10,
                -10, 0, 10, 10, 10, 10, 0, -10,
                -10, 10, 10, 10, 10, 10, 10, -10,
                -10, 5, 0, 0, 0, 0, 5, -10,
                -20, -10, -10, -10, -10, -10, -10, -20,
            ],

            #rook
            4: [
                0, 0, 0, 0, 0, 0, 0, 0,
                5, 10, 10, 10, 10, 10, 10, 5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                -5, 0, 0, 0, 0, 0, 0, -5,
                0, 0, 0, 5, 5, 0, 0, 0
            ],

            # queen
            5: [
                -20, -10, -10, -5, -5, -10, -10, -20,
                -10, 0, 0, 0, 0, 0, 0, -10,
                -10, 0, 5, 5, 5, 5, 0, -10,
                -5, 0, 5, 5, 5, 5, 0, -5,
                0, 0, 5, 5, 5, 5, 0, -5,
                -10, 5, 5, 5, 5, 5, 0, -10,
                -10, 0, 5, 0, 0, 0, 0, -10,
                -20, -10, -10, -5, -5, -10, -10, -20
            ],

            # king opening and middle game
            6: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 40, 10, 0, 0, 10, 40, 20
            ],

            # king end game
            7: [
                -50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50
            ],

            # queen opening
            8: [
                -20, -10, -10, 0, 0, -10, -10, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -20, -20, -20, -20, -20, -20, -20,
                -20, -10, -10, 0, 0, -10, -10, -20
            ]
        }
    MAXVAL = 100000
    k2 = 100
    memories = []
    def __init__(self, MAX_DEPTH=3, k1=0.01, usemodel=False):
        self.k1 = k1
        self.MAX_DEPTH = MAX_DEPTH
        self.usemodel = usemodel
        # load model
        if usemodel:
            self.opening_model = keras.models.load_model('model/opening_2layer_384neural.h5')
            self.opening_model = LiteModel.from_keras_model( self.opening_model)
            self.middle_model = keras.models.load_model('model/middle_model_3layer_384neural.h5')
            self.middle_model = LiteModel.from_keras_model(self.middle_model)
    # for encoding
    def serialize(self, brd):

        mark_white = 0
        mark_black = 0

        pawnBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'P':
                pawnBoard[i] = 1
            if pp.symbol() == 'p':
                pawnBoard[i] = -1

        knightBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'N':
                knightBoard[i] = 1
                mark_white += 1
            if pp.symbol() == 'n':
                knightBoard[i] = -1
                mark_black += 1

        bishopBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'B':
                bishopBoard[i] = 1
                mark_white += 1
            if pp.symbol() == 'b':
                bishopBoard[i] = -1
                mark_black += 1

        rookBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'R':
                rookBoard[i] = 1
                mark_white += 1
            if pp.symbol() == 'r':
                rookBoard[i] = -1
                mark_black += 1

        queenBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'Q':
                queenBoard[i] = 1
                mark_white += 1
            if pp.symbol() == 'q':
                queenBoard[i] = -1
                mark_black += 1

        kingBoard = np.zeros(64, float)
        for i in range(64):
            pp = brd.piece_at(i)
            if pp is None:
                continue
            if pp.symbol() == 'K':
                kingBoard[i] = 1
            if pp.symbol() == 'k':
                kingBoard[i] = -1
        if mark_white <= 3 and mark_black <= 3:
            state = 3
        else:
            state = 2
        return np.concatenate((pawnBoard, knightBoard, bishopBoard, rookBoard, queenBoard, kingBoard)), state


    def valuator_state1(self, brd, ser):
        # heuristic 1: value per type
        h1 = 0.0

        pm = brd.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                h1 += tval
            else:
                h1 -= tval

        # heuristic 2:
        h2 = 0.0

        squares = chess.SquareSet(brd.occupied)
        for square in squares:
            piece = brd.piece_at(square)
            color = piece.color
            i = piece.piece_type
            score = 0
            if color == chess.WHITE:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                if i == 5:
                    score = self.piece_square_table[8][Const.colRowToIndex((file, rank))]
                else:
                    score = self.piece_square_table[i][Const.colRowToIndex((file, rank))]
            else:
                if i == 5:
                    score = -self.piece_square_table[8][square]
                else:
                    score = -self.piece_square_table[i][square]
            h2 += score

        # heuristic 3:
        if self.usemodel:
            h3 = self.opening_model.predict_single(ser)
        else:
            h3 = 0

        return h1 + self.k1*h2 + self.k2*h3


    def valuator_state2(self, brd, ser):
        # heuristic 1: value per type
        h1 = 0.0

        pm = brd.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                h1 += tval
            else:
                h1 -= tval

        # heuristic 2:
        h2 = 0.0

        squares = chess.SquareSet(brd.occupied)
        for square in squares:
            piece = brd.piece_at(square)
            color = piece.color
            i = piece.piece_type
            score = 0
            if color == chess.WHITE:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                score = self.piece_square_table[i][Const.colRowToIndex((file, rank))]
            else:
                score = -self.piece_square_table[i][square]
            h2 += score

        # heuristic 3:
        if self.usemodel:
            h3 = self.middle_model.predict_single(ser)
        else:
            h3 = 0

        return h1 + self.k1 * h2 + self.k2 * h3

    def valuator_state3(self, brd):
        # heuristic 1: value per type
        h1 = 0.0

        pm = brd.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                h1 += tval
            else:
                h1 -= tval

        # heuristic 2:
        h2 = 0.0

        squares = chess.SquareSet(brd.occupied)
        for square in squares:
            piece = brd.piece_at(square)
            color = piece.color
            i = piece.piece_type
            score = 0
            if color == chess.WHITE:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                if i == 6:
                    score = self.piece_square_table[7][Const.colRowToIndex((file, rank))]
                else:
                    score = self.piece_square_table[i][Const.colRowToIndex((file, rank))]
            else:
                if i == 6:
                    score = -self.piece_square_table[7][square]
                else:
                    score = -self.piece_square_table[i][square]
            h2 += score

        return h1 + self.k1*h2

    def valuator(self, brd): # brd : chess board

        # game over state
        if brd.is_game_over():
            if brd.result() == '1-0':
                return self.MAXVAL
            if brd.result() == '0-1':
                return -self.MAXVAL
            else:
                return 0

        ser, state = self.serialize(brd)

        # state 1
        if len(self.memories) <= 20:
            return self.valuator_state1(brd, ser)

        # state 2
        if state == 2:
            return self.valuator_state2(brd, ser)

        # state 3
        if state == 3:
            return self.valuator_state3(brd)



    def anpha_beta_prunning(self, brd, depth, a, b, flaq=False):
        if depth >= self.MAX_DEPTH or brd.is_game_over():
            return self.valuator(brd)
        # white is maximizing player
        turn = brd.turn
        if turn == chess.WHITE:
            ret = -self.MAXVAL
        else:
            ret = self.MAXVAL
        if flaq:
            bret = []

        for move in brd.legal_moves:
            brd.push(move)
            tval = self.anpha_beta_prunning(brd, depth + 1, a, b)
            brd.pop()
            if flaq:
                bret.append((tval, move))
            if turn == chess.WHITE:
                ret = max(ret, tval)
                a = max(a, ret)
                if a >= b:
                    break  # b cut-off
            else:
                ret = min(ret, tval)
                b = min(b, ret)
                if a >= b:
                    break  # a cut-off
        if flaq:
            return ret, bret
        else:
            return ret

    def explore_leaves(self, brd):
        ret = []
        start = time.time()
        bval = self.valuator(brd)
        if (brd.legal_moves.count() < 15):
            cval, ret = self.anpha_beta_prunning(brd, -1, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        else:
            cval, ret = self.anpha_beta_prunning(brd, 0, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        eta = time.time() - start
        print("%.2f -> %.2f: explored in %.3f seconds" % (bval, cval, eta))
        return ret

    def getCompMove(self, brd):
        print(f'legal move: {brd.legal_moves.count()}')
        if brd.is_game_over():
            print(f'Game over {brd.outcome().result()}')
            return

        move = sorted(self.explore_leaves(brd), key=lambda x: x[0], reverse=brd.turn)
        if len(move) == 0:
            return
        mark = []
        for i, m in enumerate(move):
            for j in range(len(self.memories)):
                brd.push(move[i][1])
                fen = brd.fen()
                index = 0
                for idx in range(1, len(fen)):
                    if (fen[idx] == 'b' or fen[idx] == 'w') and fen[idx - 1] == ' ':
                        index = idx - 1
                        break
                if fen[:index] == self.memories[j][0]:
                    self.memories[j][1] += 1
                    if self.memories[j][1] > 2:
                        mark.append(i)
                    brd.pop()
                else:
                    brd.pop()
        print(f'mark {mark}')
        for i, m in enumerate(move):
            if i not in mark:
                brd.push(move[i][1])
                fen = brd.fen()
                index = 0
                for idx in range(1, len(fen)):
                    if (fen[idx] == 'b' or fen[idx] == 'w') and fen[idx - 1] == ' ':
                        index = idx - 1
                        break
                self.memories.append([fen[:index], 1])
                print(fen)
                return move[i][1]












