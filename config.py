import pygame
import os

from sound import Sound
from theme import Theme

class Config:
    def __init__(self) -> None:
        self.thems = []
        self._add_themes()
        self.idx = 1
        self.theme = self.thems[self.idx]
        
        #font 
        self.font = pygame.font.SysFont('sans', 18, bold= True) 
        
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))
    
    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.thems)
        self.theme = self.thems[self.idx]
        
    def _add_themes(self):
        green = Theme((234, 235, 200), (119, 154, 88), 
                      (244,247,116), (172, 195, 51),
                      '#f1dd85', '#f1dd85')
        brown = Theme((235, 209, 166), (165, 117, 80), 
                      (245, 234, 100), (209, 185, 59),
                      '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), 
                      (123, 187, 227), (43, 119, 191),
                      '#C86464', '#C84646')
        
        self.thems = [
            green,
            brown,
            blue,

        ]