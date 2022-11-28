import chess
from state import State
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
    k2 = 10
    MAX_DEPTH = 4

    def __init__(self):
        self.model = keras.models.load_model('model/model.h5')

    def valuator(self, s):
        b = s.board

        # game over state
        if b.is_game_over():
            if b.result() == '1-0':
                return self.MAXVAL
            if b.result() == '0-1':
                return -self.MAXVAL
            else:
                return 0

        # heuristic 1: value per type
        h1 = 0.0

        pm = b.piece_map()
        for x in pm:
            tval = self.values[pm[x].piece_type]
            if pm[x].color == chess.WHITE:
                h1 += tval
            else:
                h1 -= tval

        # heuristic 2: total legal moves
        h2 = 0.0
        temp_turn = b.turn
        b.turn = chess.WHITE
        h2 += b.legal_moves.count()
        b.turn = chess.BLACK
        h2 -= b.legal_moves.count()
        b.turn = temp_turn

        # heuristic 3: model deep learning
        # h3 = 0.0
        # brd = s.serialize()[None] #encoding and predict
        # v_dl = float(self.model(brd))
        # if b.turn == chess.WHITE:
        #     h3 += v_dl*v_dl*v_dl
        # else:
        #     h3 -= v_dl*v_dl*v_dl

        # valuator here
        val = h1 + self.k1*h2# + self.k2*h3

        return val


    def anpha_beta_prunning(self, s, depth, a, b, flaq=False):
        if depth >= self.MAX_DEPTH or s.board.is_game_over():
            return self.valuator(s)
        # white is maximizing player
        turn = s.board.turn
        if turn == chess.WHITE:
            ret = -self.MAXVAL
        else:
            ret = self.MAXVAL
        if flaq:
            bret = []

        for move in s.board.legal_moves:
            s.board.push(move)
            tval = self.anpha_beta_prunning(s, depth + 1, a, b)
            s.board.pop()
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

    def explore_leaves(self, s):
        ret = []
        start = time.time()
        bval = self.valuator(s)
        cval, ret = self.anpha_beta_prunning(s, 0, a=-self.MAXVAL, b=self.MAXVAL, flaq=True)
        eta = time.time() - start
        print("%.2f -> %.2f: explored in %.3f seconds" % (bval, cval, eta))
        return ret

    def getCompMove(self, s):
        move = sorted(self.explore_leaves(s), key=lambda x: x[0], reverse=s.board.turn)
        if len(move) == 0:
            return
        print("top 3:")
        for i, m in enumerate(move[0:3]):
            print("  ", m)
        print(s.board.turn, "moving", move[0][1])
        return move[0][1]












