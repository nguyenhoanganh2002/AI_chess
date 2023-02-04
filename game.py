from const import *
import os
import pygame
import chess
from dragger import Dragger
from theme  import Theme
from config import Config


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = (-1, -1)
        self.board = chess.Board()
        self.dragger = Dragger()
        self.config = Config()
    
    
    def __set_texture(self, piece, size = 80):
        color = 'white' if piece.color else 'black'
        name = chess.piece_name(piece.piece_type)
        texture = self.texture = os.path.join(f'assets/images/imgs-{size}px/{color}_{name}.png')
        return texture
    
    #blit method
    def update_blit(self, surface):
        #texture
        texture =  self.__set_texture(self.dragger.piece,size = 128)
        
        #img
        img = pygame.image.load(texture)
        #rect
        img_center = (self.dragger.mouse[0], self.dragger.mouse[1])
        texture_rect = img.get_rect(center = img_center) 
        #blit
        surface.blit(img, texture_rect)
        
        
    def update(self, surface):
        #texture
        texture = os.path.join('assets/images/imgs-128px/black_queen.png')
        
        #img
        img = pygame.image.load(texture)
        #rect
        img_center = (200, 200)
        texture_rect = img.get_rect(center = img_center) 
        #blit
        surface.blit(img, texture_rect)
        
    # Show method
    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
    
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
                #row coordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.config.font.render(str(ROWS - row), True, color)
                    label_pos = (5, 5 + row*SQSIZE)
                    surface.blit(label, label_pos)
                    
                #col coordinates
                if row == 7:
                    color = theme.bg.dark if col % 2 == 1 else theme.bg.light
                    # label = self.config.font.render(Square.get_alphacol(col), True, color)
                    label = self.config.font.render(Const.colsToFiles[col], True, color)
                
                    label_pos = (col*SQSIZE + SQSIZE - 25, HEIGH - 25)
                    surface.blit(label, label_pos)
                    
    
    def show_pieces(self, surface):
       
        for row in range(ROWS):
            for col in range(COLS):
                pos = Const.colRowToIndex((col,row))
                # pos = Const.posToindex((col, row))
                if self.board.piece_at(pos):
                    piece = self.board.piece_at(pos)
                    
                    # all piece except dragger piece
                    if not self.dragger.draggging or row != self.dragger.initial[1] or col != self.dragger.initial[0]:
                        texture = self.__set_texture(piece)
                        img = pygame.image.load(texture)
                        img_center = col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
    
    def legal_move_from_square(self):
        moves = []
        for move in self.board.legal_moves:
            if move.from_square == Const.colRowToIndex(self.dragger.initial):
                moves.append(move)
                # print('yyyy')
        return moves
    
    def show_move(self, surface):
        theme = self.config.theme 
        
        if self.dragger.draggging:
            
            
            #loop all valid moves
            for move in self.legal_move_from_square():
                # print("kkkk")
                #color
                color = theme.move.light if (move.to_square // 8 + move.to_square % 8) % 2 == 0 else theme.move.dark
                #rect
                col, row = Const.indexToColRow(move.to_square)
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
                # print(f'{col} {row}')
    
    
    def show_last_move(self, surface):
        theme = self.config.theme
        
        if len(self.board.move_stack) > 0:
            last_move = self.board.peek()
            
            initial = last_move.from_square
            final = last_move.to_square
            
            for pos in (initial, final):
                col , row = Const.indexToColRow(pos)
                color = theme.trace.light if (row + col) % 2 == 0 else theme.trace.dark
                rect = pygame.Rect(col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            
            rect = pygame.Rect(self.hovered_sqr[0]*SQSIZE, self.hovered_sqr[1]*SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width= 5)  
            
    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.board.pop()
                     
                
    def change_theme(self):
        self.config.change_theme()
                                     
    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()  
    
    
    def reset(self):
        self.__init__()               
                       
    
    def set_hover(self, motion):
        self.hovered_sqr = (motion[0] // SQSIZE, motion[1] // SQSIZE)
        
                    
