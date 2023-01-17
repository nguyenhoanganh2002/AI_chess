import pygame

from const import *


class Dragger:
    def __init__(self) :
        self.mouse = (0,0)
        self.mouse_square = (0, 0)
        self.initial = (0, 0)
        self.piece = None
        self.draggging = False
        
    

    def update_mouse(self, pos):
        self.mouse = (pos[0], pos[1])
        self.mouse_square = (pos[0] // SQSIZE, pos[1] // SQSIZE)
        
        
    def save_initial(self, pos):
        self.initial = (pos[0] // SQSIZE, pos[1] // SQSIZE)
    
    def drag_piece(self, piece):
        self.piece = piece
        self.draggging = True
    
    def undrag_piece(self):
        self.piece = None
        self.draggging = False
    
    