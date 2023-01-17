import pygame
import sys
from game import *
from const import *
from time import time
from ai import AI
from computer import Computer
import time
from button import Button




# load menu images
resume_img = pygame.image.load("images/button_resume.png")

# create buttom instance
resume_button = Button(WIDTH/2 - resume_img.get_width()/2, HEIGH/4 - resume_img.get_height()/2, resume_img, 1)

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGH))
        pygame.display.set_caption('Chess') 
        self.game = Game()
        self.clock = pygame.time.Clock()
        self.engine_1 = Computer(MAX_DEPTH=3, k1=1, usemodel=True)
        self.engine_2 = AI(3)
        self.pause_state = True
        
    
    def mainloop(self):
        
        self.clock.tick(100)
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = game.board
        pause_state = self.pause_state

        running = True
        player = True
        # player = False
        
    
        while running:

            if pause_state == True:
                screen.fill((0,0,0))
                if resume_button.draw(screen):
                    pause_state = False
            else:
                self.clock.tick(100)
                game.show_bg(screen)

                if(dragger.draggging):
                    game.show_move(screen)

                game.show_last_move(screen)

                if(dragger.draggging):
                    game.show_move(screen)

                game.show_hover(screen)


                game.show_pieces(screen)

                # WHITE move
                # if player:
                #     pygame.display.flip()
                #     try:
                #
                #         # board.push(self.engine_1.getCompMove(board))
                #         board.push(self.engine_2.calculate_ab(board.fen()))
                #
                #     except:
                #         print("exception")
                #     player = False
                #
                # game.show_bg(screen)
                #
                # if (dragger.draggging):
                #     game.show_move(screen)
                #
                # game.show_last_move(screen)
                # game.show_pieces(screen)

                #BLACK move
                # if not player:
                #     pygame.display.flip()
                #     try:
                #
                #         board.push(self.engine_1.getCompMove(board))
                #         # board.push(self.engine_2.calculate_ab(board.fen()))
                #
                #     except:
                #         print("exception")
                #     player = True


                if(dragger.draggging):
                    game.update_blit(screen)


                if board.is_game_over():
                    time.sleep(3)
                    running = False
                    print(board.result())
                 
            for event in pygame.event.get():

                if not pause_state:
                    #click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse(event.pos)
                        # print('click {}'.format(event.pos))
                        print(dragger.mouse_square)

                        if board.piece_at(Const.colRowToIndex(dragger.mouse_square)):

                            dragger.save_initial(event.pos)
                            # print(dragger.initial)
                            pos = Const.colRowToIndex(dragger.initial)
                            # print(pos)
                            piece = board.piece_at(pos)

                            # print(chess.piece_name(piece.piece_type))
                            dragger.drag_piece(piece)


                    #mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion = event.pos
                        game.set_hover(motion)

                        if dragger.draggging:
                            dragger.update_mouse(event.pos)
                            game.update_blit(screen)


                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP :

                        initial = Const.colRowToIndex(dragger.initial)
                        released = Const.colRowToIndex(dragger.mouse_square)

                        from_square = chess.SQUARE_NAMES[initial]
                        to_square = chess.SQUARE_NAMES[released]

                        try:
                            move = chess.Move.from_uci(from_square + to_square)


                            if move in game.legal_move_from_square():
                                game.play_sound(board.is_capture(move))
                                board.push(move)
                                player = False

                            #pawn promotion
                            try:
                                move = chess.Move.from_uci(from_square + to_square + 'q')
                            except:
                                pass

                            if move in game.legal_move_from_square():

                                # #en passant capture
                                game.play_sound(True)
                                board.push(move)
                                player = False


                        except:
                            move = None
                            print('exception')

                        dragger.undrag_piece()
                        game.show_pieces(screen)
                    
                # key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_state = not pause_state
                    if not pause_state:
                        if event.key == pygame.K_t:
                            game.change_theme()

                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            screen = self.screen
                            dragger = self.game.dragger
                        if event.key == pygame.K_z:
                            # update later
                            game.undo_move()
                
                                   
                #quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            pygame.display.flip()
                    
main = Main()
main.mainloop()  