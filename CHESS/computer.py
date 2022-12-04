import chess
import numpy as np
from model import LiteModel
from tensorflow import keras
import time

class Computer:
    values = {chess.PAWN: 1,
              chess.KNIGHT: 3,
              chess.BISHOP: 3,
              chess.ROOK: 5,
              chess.QUEEN: 9,
              chess.KING: 0}
    MAXVAL = 1000
    k1 = 0.1
    k2 = 1
    MAX_DEPTH = 3

    def __init__(self, usemodel=False):
        self.usemodel = usemodel
        # load model
        if usemodel:
            self.model = keras.models.load_model('model/cp6.h5')
            self.model = LiteModel.from_keras_model(self.model)

    # for encoding
    def splitter(self, inputStr, black):
        inputStr = format(inputStr, "064b")
        tmp = [inputStr[i:i + 8] for i in range(0, len(inputStr), 8)]

        for i in range(0, len(tmp)):
            tmp2 = list(tmp[i])
            tmp2 = [int(x) * black for x in tmp2]
            tmp[i] = tmp2

        return np.asarray(tmp).reshape((64))

    # encoding here
    def fen2bit(self, b):
        return np.concatenate((self.splitter(int(b.pieces(chess.PAWN, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.ROOK, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.KNIGHT, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.BISHOP, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.QUEEN, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.KING, chess.WHITE)), 1),
                               self.splitter(int(b.pieces(chess.PAWN, chess.BLACK)), -1),
                               self.splitter(int(b.pieces(chess.ROOK, chess.BLACK)), -1),
                               self.splitter(int(b.pieces(chess.KNIGHT, chess.BLACK)), -1),
                               self.splitter(int(b.pieces(chess.BISHOP, chess.BLACK)), -1),
                               self.splitter(int(b.pieces(chess.QUEEN, chess.BLACK)), -1),
                               self.splitter(int(b.pieces(chess.KING, chess.BLACK)), -1)), axis=0)

    def valuator(self, brd): # brd : chess board

        # game over state
        if brd.is_game_over():
            if brd.result() == '1-0':
                return self.MAXVAL
            if brd.result() == '0-1':
                return -self.MAXVAL
            else:
                return 0

        # heuristic 1: value per type
        h1 = 0.0

        pm = brd.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                h1 += tval
            else:
                h1 -= tval

        # heuristic 2: total legal moves
        h2 = 0.0
        temp_turn = brd.turn
        brd.turn = chess.WHITE
        h2 += brd.legal_moves.count()
        brd.turn = chess.BLACK
        h2 -= brd.legal_moves.count()
        brd.turn = temp_turn

        # heuristic 3: model deep learning
        if self.usemodel:
            bitmap = self.fen2bit(brd)  # encoding and predict
            h3 = self.model.predict_single(bitmap)
            # valuator here
            val = h1 + self.k1 * h2 + self.k2 * h3
        else:
            val = h1 + self.k1 * h2

        return val


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
        cval, ret = self.anpha_beta_prunning(brd, 0, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        eta = time.time() - start
        print("%.2f -> %.2f: explored in %.3f seconds" % (bval, cval, eta))
        return ret

    def getCompMove(self, brd):
        move = sorted(self.explore_leaves(brd), key=lambda x: x[0], reverse=brd.turn)
        if len(move) == 0:
            return
        print("top 3:")
        for i, m in enumerate(move[0:3]):
            print("  ", m)
        print(brd.turn, "moving", move[0][1])
        return move[0][1]












