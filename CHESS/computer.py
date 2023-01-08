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
    MAXVAL = 10000
    k2 = 1
    memories = []
    def __init__(self, MAX_DEPTH=3, k1=0.01, usemodel=False):
        self.auto_dataset = list(np.load('auto_dataset.npy'))
        self.k1 = k1
        self.MAX_DEPTH = MAX_DEPTH
        self.usemodel = usemodel
        # load model
        if usemodel:
            self.opening_model = keras.models.load_model('model/opening_model_2layer_384neural.h5')
            self.opening_model = LiteModel.from_keras_model( self.opening_model)
            self.middle_model = keras.models.load_model('model/middle_model_3layer_384neural.h5')
            self.middle_model = LiteModel.from_keras_model(self.middle_model)
            self.ending_model = keras.models.load_model('model/ending_model_3layer_384neural.h5')
            self.ending_model = LiteModel.from_keras_model(self.ending_model)
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
        if mark_white <= 3 or mark_black <= 3:
            state = 3
        else:
            state = 2
        return np.concatenate((pawnBoard, knightBoard, bishopBoard, rookBoard, queenBoard, kingBoard)), state

    def valuator(self, brd): # brd : chess board

        # game over state
        if brd.is_game_over():
            if brd.result() == '1-0':
                return self.MAXVAL
            if brd.result() == '0-1':
                return -self.MAXVAL
            else:
                return 0



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
            ser, state = self.serialize(brd)  # encoding and predict
            if np.shape(self.memories)[0] <= 20:
                h3 = self.opening_model.predict_single(ser)
            else:
                if state == 2:
                    h3 = self.middle_model.predict_single(ser)
                else:
                    h3 = 0

            # valuator here
            val = self.k1 * h2 + self.k2 * h3
        else:
            val = self.k1 * h2

        # heuristic 1: value per type
        h1 = 0.0

        pm = brd.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                rank = int(x / 8)
                if rank > 3 and pm[x].piece_type == chess.PAWN and state == 3:
                    tval += (rank - 3)*0.5
                h1 += tval
            else:
                rank = int(x / 8)
                if rank < 4 and pm[x].piece_type == chess.PAWN and state == 3:
                    tval += (rank - 3) * 0.5
                h1 -= tval

        val += h1
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
        if (brd.legal_moves.count() <= 20):
            cval, ret = self.anpha_beta_prunning(brd, -1, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        else:
            cval, ret = self.anpha_beta_prunning(brd, 0, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        eta = time.time() - start
        print("%.2f -> %.2f: explored in %.3f seconds" % (bval, cval, eta))
        return ret

    def getCompMove(self, brd):
        print(f'legal move: {brd.legal_moves.count()}')
        if brd.is_game_over():
            np.save('auto_dataset.npy', np.array(self.auto_dataset))
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
                self.auto_dataset.append(fen)
                print(fen)
                return move[i][1]












