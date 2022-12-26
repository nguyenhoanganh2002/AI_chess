import chess
import random
import numpy
import time


class AI:
    def __init__(self, board, maxDepth) -> None:
        self.board = board
        self.maxDepth = maxDepth
        self.piece_values = {
            # pawn
            1: 100,
            # bishop
            2: 330,
            # knight
            3: 320,
            # rook
            4: 510,
            # queen
            5: 880,
        }

        self.square_table = {
            1: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                10, 10, 20, 30, 30, 20, 10, 10,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
                5, -5, -10, 0, 0, -10, -5, 5,
                5, 10, 10, -20, -20, 10, 10, 5,
                0, 0, 0, 0, 0, 0, 0, 0
            ],
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
            6: [
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -30, -40, -40, -50, -50, -40, -40, -30,
                -20, -30, -30, -40, -40, -30, -30, -20,
                -10, -20, -20, -20, -20, -20, -20, -10,
                20, 20, 0, 0, 0, 0, 20, 20,
                20, 30, 10, 0, 0, 10, 30, 20
            ]
        }
        self.leaves_reached = 0

    def material_eval(self):
        score = 0
        # iterate through the pieces
        for i in range(1, 6):
            score += len(self.board.pieces(i, chess.WHITE)) * self.piece_values[i]
            score -= len(self.board.pieces(i, chess.BLACK)) * self.piece_values[i]
        return score

    def mateOpportunity(self):
        if (self.board.legal_moves.count() == 0):
            if (self.board.turn == chess.WHITE):
                return -99999
            else:
                return 99999
        else:
            return 0

    def openning(self):
        if (self.board.fullmove_number < 10):
            if (self.board.turn == chess.WHITE):
                return 30 * self.board.legal_moves.count()
            else:
                return -30 * self.board.legal_moves.count()
        else:
            return 0

    def position_eval(self):
        score = 0
        # iterate through the pieces
        for i in range(1, 7):
            # eval white pieces
            w_squares = self.board.pieces(i, chess.WHITE)

            for square in w_squares:
                score += self.square_table[i][-square]

            b_squares = self.board.pieces(i, chess.BLACK)

            for square in b_squares:
                score -= self.square_table[i][square]

        return score

    def eval(self):
        return self.openning() + self.material_eval() + self.mateOpportunity() + self.position_eval()

    def alpha_beta(self, depth, move, alpha, beta, prev_moves, maximiser):

        move_sequence = []

        if depth == 0:
            # return move, self.material_eval()
            move_sequence.append(move)
            return move_sequence, self.eval()

        moves = list(self.board.legal_moves)

        # if there are no legal moves, check for checkmate / stalemate
        if not moves:
            if self.board.is_checkmate():
                if self.board.result() == "1-0":
                    move_sequence.append(move)
                    return move_sequence, 1000000
                elif self.board.result() == "0-1":
                    move_sequence.append(move)
                    return move_sequence, -1000000
            else:
                print("khong phai chieu")
                move_sequence.append(move)
                return move_sequence, 0

        # initialise best move variables. What are these used for again? I need to simplify the logic here.
        best_move = None
        best_score = -numpy.inf if maximiser else numpy.inf

        # chuwa hieu

        # put the last calculated best move in first place of the list. Hopefully this improves pruning.
        if prev_moves and len(prev_moves) >= depth:
            if depth == 4 and not self.board.turn:
                print(prev_moves[depth - 1])
            if prev_moves[depth - 1] in moves:
                # if prev_moves[depth - 1] in self.board.legal_moves:
                # if not self.board.turn:
                #     print(prev_moves[depth - 1])
                moves.insert(0, prev_moves[depth - 1])

        if maximiser:
            for move in moves:
                self.leaves_reached += 1

                # get score of the new move, record what it is
                self.board.push(move)
                new_sequence, new_score = self.alpha_beta(depth - 1, move, alpha, beta, prev_moves, False)
                self.board.pop()

                # Check whether the new score is better than the best score. If so, replace the best score.
                if new_score > best_score:
                    move_sequence = new_sequence
                    best_score, best_move = new_score, move

                # Check whether the new score is better than the beta. If it is, return and break the loop.
                # Need to rethink the check against best here.
                if new_score >= beta:
                    # self.check_against_best(best_move, best_score, depth_pos, True)
                    move_sequence.append(best_move)
                    return move_sequence, best_score

                # Update alpha - upper bound
                if new_score > alpha:
                    alpha = new_score
            # return the best of the results
            # self.check_against_best(best_move, best_score, depth_pos, True)
            move_sequence.append(best_move)
            return move_sequence, best_score

        else:
            for move in moves:
                self.leaves_reached += 1

                # get score of the new move, record what it is
                self.board.push(move)
                new_sequence, new_score = self.alpha_beta(depth - 1, move, alpha, beta, prev_moves, True)
                self.board.pop()

                # Check whether the new score is better than the best score. If so, replace the best score.
                if new_score < best_score:
                    move_sequence = new_sequence
                    best_score, best_move = new_score, move

                # Check whether the new score is better than the alpha. If it is, return and break the loop
                if new_score <= alpha:
                    # self.check_against_best(best_move, best_score, depth_pos, False)
                    move_sequence.append(best_move)
                    return move_sequence, best_score

                # update beta - lower bound
                if new_score < beta:
                    # print("xxxx")
                    beta = new_score

            # return the best of the results
            # self.check_against_best(best_move, best_score, depth_pos, False)
            move_sequence.append(best_move)
            return move_sequence, best_score

    def total_leaves(self):
        leaves = self.leaves_reached
        self.leaves_reached = 0
        return leaves

    def calculate_ab(self, depth):
        maximiser = self.board.turn

        start_time = time.time()
        move_sequence, best_score = self.alpha_beta(depth, None, -numpy.inf, numpy.inf, None, maximiser)
        print(self.total_leaves())
        for i in range(1, len(move_sequence)):
            print(f'move {move_sequence[-i]}', end=' ')
        print("Time taken:", time.time() - start_time)

        if self.board.is_game_over():
            print(f'Game over {self.board.outcome().result()}')
            return

        return move_sequence[-1]