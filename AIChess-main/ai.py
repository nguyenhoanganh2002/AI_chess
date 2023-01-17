import chess
import numpy
import time
from const import Const


class AI:
    def __init__(self, maxDepth, board = chess.Board()) -> None:
        self.board = board
        self.maxDepth = maxDepth
        self.endgame_piece_count = 7
        self.piece_values = {
            # pawn
            1:100,
            # knight
            2:330,
            # bishop
            3:320,
            # rook
            4:510,
            # queen
            5:900,
            #kind
            6:99999
        }
        
        self.piece_square_table = {
            #panwn
            1: [
                0, 0, 0, 0, 0, 0, 0, 0,
                50, 50, 50, 50, 50, 50, 50, 50,
                15, 15, 25, 35, 35, 25, 15, 15,
                5, 5, 10, 25, 25, 10, 5, 5,
                0, 0, 0, 20, 20, 0, 0, 0,
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
            7:[
                -50,-40,-30,-20,-20,-30,-40,-50,
                -30,-20,-10,  0,  0,-10,-20,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 30, 40, 40, 30,-10,-30,
                -30,-10, 20, 30, 30, 20,-10,-30,
                -30,-30,  0,  0,  0,  0,-30,-30,
                -50,-30,-30,-30,-30,-30,-30,-50
            ]
        }
        
        
        
        #evaluation of piece
        self.DOUBLED_PAWN_PENALTY      = 8
        self.ISOLATED_PAWN_PENALTY     = 15
        self.PASSED_PAWN_BONUS         = 20
        self.ROOK_SEMI_OPEN_FILE_BONUS = 15
        self.ROOK_OPEN_FILE_BONUS      = 20
        self.ROOK_ON_SEVENTH_BONUS     = 20
        self.ROOK_BLOCKED_BY_UNCASTLED_KING_PENALTY = 15
        self.QUEEEN_EEARLY_DEVELOPMENT_PENALTY = 20
        self.BAD_BISHOP_PENALTY = 10
        self.KING_HAS_CASTLING_RIGHT_BUNUS = 10
        
        
        #opening game
        self.WHITE_BISHOP_OR_KNIGHT_MOVE = False
        self.BLACK_BISHOP_OR_KNIGHT_MOVE = False
        
        
        self.leaves_reached = 0
        
        #is last move capture
        self.is_last_move_capture = True
        self.last_meterial_eval = 0
        self.last_piece_count = 0
        

    
    def material_eval(self, piece):
        color = piece.color
        i = piece.piece_type
        score = self.piece_values[i] if color == chess.WHITE else -self.piece_values[i]
        return score

    def piece_square_eval(self, square, piece, piece_count):
        color = piece.color
        i = piece.piece_type
        score = 0
        
        if color == chess.WHITE:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            if i == 6 and self.endgame_piece_count > piece_count:
                score = self.piece_square_table[7][Const.colRowToIndex((file, rank))]
            else:
                score = self.piece_square_table[i][Const.colRowToIndex((file, rank))]
        else:
            if i == 6 and self.endgame_piece_count > piece_count:
                score = -self.piece_square_table[7][square]
            else:
                score = -self.piece_square_table[i][square]
        return score
        
    def mobility_eval(self):
        score = 0
        if (self.board.turn == chess.WHITE):
            score = self.board.legal_moves.count()
        else:
            score = -self.board.legal_moves.count()
            
        #to make develop in the first moves
        if (self.board.fullmove_number < 10):
            return score
        else:
            return score*1/4

    def get_neighbors(self, a):
            neighbors = []
            if a  == 7:
                neighbors = [6]
            elif a == 0:
                neighbors = [1]
            else:
                neighbors = [a-1, a+1]
        
            return neighbors

    def piece_eval(self, square, piece):
        score = 0
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        color = piece.color
        i = piece.piece_type
        adjacent_files = self.get_neighbors(file)
        adjacent_ranks = self.get_neighbors(rank)
        
        # With pawn piece
        if i == chess.PAWN:
        # Pawn Structure
            
                
            # Check if the pawn is isolated
            is_isolated = True
            for adjacent_file in adjacent_files:
                for r in range(1, 7): 
                    if self.board.piece_at(chess.square(adjacent_file, r)) == piece:
                        is_isolated = False
                        break
            if is_isolated:
                # print("isolated")
                temp = -self.ISOLATED_PAWN_PENALTY if color == chess.WHITE else self.ISOLATED_PAWN_PENALTY
                score += temp
                
            # Check if the pawn is doubled
            is_double = False
            for adjacent_rank in adjacent_ranks:
                if self.board.piece_at(chess.square(file, adjacent_rank)) == piece:
                    is_double = True
                    break
            if is_double:
                # print("doubled")
                temp = -self.DOUBLED_PAWN_PENALTY if color == chess.WHITE else self.DOUBLED_PAWN_PENALTY
                score += temp
                
                
            #check if the pawn is a passed pawn
            files  = adjacent_files
            files.append(file)
            is_passed = True
            enemy_piece = chess.Piece(chess.PAWN, not color)
            for f in files:
                for r in range(rank + 1, 7) if color == chess.WHITE else range(1, rank):
                    p = self.board.piece_at(chess.square(f, r))
                    if p == enemy_piece:
                        is_passed = False
                        break
                
                if not is_passed:
                    break
            if is_passed:
                temp = self.PASSED_PAWN_BONUS if color == chess.WHITE else -self.PASSED_PAWN_BONUS
                score += temp     
                     
        #With knight piece
        if i == chess.KNIGHT:
            # Decreasing value as pawns disappear
            if color == chess.WHITE and not self.board.pieces(chess.PAWN, chess.WHITE):
                score -= self.piece_values[2]*0.04
                
            elif color == chess.BLACK and not self.board.pieces(chess.PAWN, chess.BLACK):
                score += self.piece_values[2]*0.04
        
        # with bishop piece
        if i == chess.BISHOP:
            #bad biship
            is_badBishop = False
            board_copy = chess.Board(self.board.fen()) 
            enemy_piece = chess.Piece(chess.BISHOP, not color)
            board_copy.set_piece_at(square, enemy_piece)
            
            p_pawn = chess.Piece(chess.PAWN, color)
             
            # Find all squares that the piece on e4 can attack
            attacked_squares = board_copy.attacks(square)
            # Convert the bitboard to a list of squares
            squares = chess.SquareSet(attacked_squares)
            for s in squares:
                if self.board.piece_at(s) == p_pawn:
                    is_badBishop = True
                    break
            if is_badBishop:
                temp = -self.BAD_BISHOP_PENALTY if color == chess.WHITE else +self.BAD_BISHOP_PENALTY
                score += temp
            
        # With rook piece
        if i == chess.ROOK:
            enemyPawn = False
            myPawn = False
            for r in range(1,7):
                piece_k = self.board.piece_at(chess.square(file, r))
                if piece_k != None and piece_k.piece_type == chess.PAWN:
                    if piece_k.color == color:
                        myPawn = True
                        break
                    else:
                        enemyPawn = True
            
            temp = 0
            if not myPawn and not enemyPawn:
                # Rook open file
                temp = self.ROOK_OPEN_FILE_BONUS
                # print("rook open file")
            elif not myPawn: # Rook semi open file
                temp = self.ROOK_SEMI_OPEN_FILE_BONUS
                # print("rook semi open file")
            
            if color == chess.WHITE:
                score += temp
            else:
                score -= temp
            
            # rook on seventh rank.
            if color == chess.WHITE and rank == 7:
                score += self.ROOK_ON_SEVENTH_BONUS
            elif color == chess.BLACK and rank == 0:
                score -= self.ROOK_ON_SEVENTH_BONUS
                
            #Increasing value as pawns disappear
            if color == chess.WHITE and not self.board.pieces(chess.PAWN, chess.BLACK):
                score += self.piece_values[4]*0.04
                
            if color == chess.BLACK and not self.board.pieces(chess.PAWN, chess.WHITE):
                score -= self.piece_values[4]*0.04
                
                
            # Penalty for a rook that is blocked by an uncastled king
            if color == chess.WHITE:
                # Find the squares attacked by the white king
                king_attacks = self.board.attacks(chess.E1)

                # Find the squares attack by the white rook
                rook_attacks_h1 = self.board.attacks(chess.H1)
                rook_attacks_a1 = self.board.attacks(chess.A1)

                # Find the squares attack by both the king and the rook
                between_attacks = king_attacks & (rook_attacks_h1 | rook_attacks_a1)

                # Check if there are any squares attack by both the king and the rook
                if not between_attacks:
                    # print('rook blocked')
                    score -= self.ROOK_BLOCKED_BY_UNCASTLED_KING_PENALTY
            if color == chess.BLACK:
                # Find the squares attacked by the white king
                king_attacks = self.board.attacks(chess.E8)

                # Find the squares attack by the white rook
                rook_attacks_h8 = self.board.attacks(chess.H8)
                rook_attacks_a8 = self.board.attacks(chess.A8)
                # Find the squares attack by both the king and the rook
                between_attacks = king_attacks & (rook_attacks_h8 | rook_attacks_a8)

                # Check if there are any squares attack by both the king and the rook
                if not between_attacks:
                    # print('rook blocked')
                    score += self.ROOK_BLOCKED_BY_UNCASTLED_KING_PENALTY
                    
        # With queen
        if i == chess.QUEEN:
        # Penalty for early development
            if color == chess.WHITE and self.board.pieces(chess.QUEEN, chess.WHITE):
                square_queen = chess.square_rank(self.board.pieces(chess.QUEEN, chess.WHITE))
                if square_queen != 0 and not self.WHITE_BISHOP_OR_KNIGHT_MOVE:
                    score -= self.QUEEEN_EEARLY_DEVELOPMENT_PENALTY
            
            if color == chess.BLACK and self.board.pieces(chess.QUEEN, chess.BLACK):
                square_queen = chess.square_rank(self.board.pieces(chess.QUEEN, chess.BLACK))
                if square_queen != 7 and not self.BLACK_BISHOP_OR_KNIGHT_MOVE:
                    score += self.QUEEEN_EEARLY_DEVELOPMENT_PENALTY

        # With king
        if i == chess.KING:
            # has castlign right.
            if self.board.has_castling_rights(chess.WHITE):
                score += self.KING_HAS_CASTLING_RIGHT_BUNUS
            if self.board.has_castling_rights(chess.BLACK):
                score -= self.KING_HAS_CASTLING_RIGHT_BUNUS

        return score
    
    def eval(self):
        score = 0
        piece_count = 0
        for p in range(1, 6):
            piece_count += len(self.board.pieces(p, chess.WHITE))
            piece_count += len(self.board.pieces(p, chess.BLACK))
        
            
        occupied_squares = self.board.occupied
        # Convert the bitboard to a list of squares
        squares = chess.SquareSet(occupied_squares)
        for square in squares:
            piece = self.board.piece_at(square)
            score += (1.02*self.material_eval(piece) 
                      + self.piece_square_eval(square,piece, piece_count)
                      + self.piece_eval(square, piece)
                      
            )
        score += self.mobility_eval()

        return score
    
                          
    def alpha_beta(self, depth, move, alpha, beta, prev_moves, maximiser):

            move_sequence = []
            if depth == 0:
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
                    move_sequence.append(move)
                    return move_sequence, 0


            # initialise best move variables. What are these used for again? I need to simplify the logic here.
            best_move = None
            best_score = -numpy.inf if maximiser else numpy.inf
 

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
                    if best_score >= beta:
                        # self.check_against_best(best_move, best_score, depth_pos, True)
                        move_sequence.append(best_move)
                        return move_sequence, best_score
                    
                    # Update alpha - upper bound
                    if best_score > alpha:
                        alpha = best_score
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
                    if best_score <= alpha:
                        # self.check_against_best(best_move, best_score, depth_pos, False)
                        move_sequence.append(best_move)
                        return move_sequence, best_score

                    # update beta - lower bound
                    if best_score < beta:
                        # print("xxxx")
                        beta = new_score

                # return the best of the results
                # self.check_against_best(best_move, best_score, depth_pos, False)
                move_sequence.append(best_move)
                return move_sequence, best_score


    def calculate_ab(self, fen):
        
        self.board.set_fen(fen)
        maximiser = self.board.turn
        
        start_time = time.time()
        move_sequence, best_score = self.alpha_beta(self.maxDepth, None, -numpy.inf, numpy.inf, None, maximiser)

        for i in range(1, len(move_sequence)):
            print(f'move {move_sequence[-i]}', end=' ')
            
        print("Time taken:", time.time() - start_time)
        print(f'score: {best_score}')
        
        move = move_sequence[-1]
        piece = self.board.piece_at(move.from_square)
        
        if self.board.is_capture(move):
            pass
        # middle game
        if piece == 'B' or piece == 'N':
            self.WHITE_BISHOP_OR_KNIGHT_MOVE = True
        elif piece == 'b' or piece == 'n':
            self.BLACK_BISHOP_OR_KNIGHT_MOVE = True
            
        # print(move)
        return move