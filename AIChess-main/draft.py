from ai import AI
import chess
from const import Const


board = chess.Board()
print(board.legal_moves)

board.push_san("Nh3")
board.push_san("h5")


engine = AI(5, board) 
# print(engine.eval())
# print(board.turn)




print(board.piece_at(2))
print(board.piece_at(2).piece_type)
print(board.piece_at(2).color)
print(chess.BISHOP)


# for pawn in chess.Pawns(board):
#     print(pawn)
print(engine.piece_eval(2, board.piece_at(2)))

# board.pieces(1, chess.WHITE)
# def evaluate_pawn_structure(board):
#   score = 0
  
#   # Iterate over all pawns on the board
#   for pawn in board.pieces(1, chess.WHITE):
#     # Check if the pawn is isolated
#     if not board.attacks(pawn):
#       score -= 10
#     # Check if the pawn is doubled
#     if board.is_attacked_by(chess.WHITE if board.turn else chess.BLACK, pawn):
#       score -= 5
#     # Check if the pawn is a passed pawn
#     if board.is_passed_pawn(pawn):
#       score += 10
#     # Check if the pawn is a backward pawn
#     if board.is_backward_pawn(pawn):
#       score -= 5
      
#     return score
# # print(board)
# evaluate_pawn_structure(board)


# w_squares = board.pieces(5, chess.BLACK)

# for square in w_squares:
#     print(square)
#     rank = chess.square_rank(square)
#     file = chess.square_file(square)
#     print(Const.colRowToIndex((file, rank)))



# def evaluate_pawn_structure(board):
#   score = 0
  
#   # Iterate over all pawns on the board
#   for pawn in chess.Pawns(board):
#     # Check if the pawn is isolated
#     if not board.attacks(pawn):
#       score -= 10
#     # Check if the pawn is doubled
#     if board.is_attacked_by(chess.WHITE if board.turn else chess.BLACK, pawn):
#       score -= 5
#     # Check if the pawn is a passed pawn
#     if board.is_passed_pawn(pawn):
#       score += 10
#     # Check if the pawn is a backward pawn
#     if board.is_backward_pawn(pawn):
#       score -= 5
      
#   return score

# evaluate_pawn_structure(board)





