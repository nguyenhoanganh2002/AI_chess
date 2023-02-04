import pygame
import sys
from game import *
from const import *
from time import time
from ai import AI
from computer import Computer
import time
from button import Button
# from comp2 import Computer_2




# load menu images
resume_img = pygame.image.load("images/resume.png")
menu_img = pygame.image.load("images/menu.png")
pvp_img = pygame.image.load("images/pvp.png")
pvc_img = pygame.image.load("images/pvc.png")
cvc_img = pygame.image.load("images/cvc.png")
quit_img = pygame.image.load("images/quit.png")
white_img = pygame.image.load("images/WHITE.png")
black_img = pygame.image.load("images/BLACK.png")
depth_img = pygame.image.load("images/choose_depth.png")
d1_img = pygame.image.load("images/d1.png")
d2_img = pygame.image.load("images/d2.png")
d3_img = pygame.image.load("images/d3.png")
d4_img = pygame.image.load("images/d4.png")


# create buttom instance
resume_button = Button(WIDTH/2 - resume_img.get_width()/2, HEIGH/4 - resume_img.get_height()/2, resume_img, 1)
menu_button = Button(WIDTH/2 - menu_img.get_width()/2, HEIGH/2 - menu_img.get_height()/2, menu_img, 1)
quit_button_pause = Button(WIDTH/2 - quit_img.get_width()/2, 3*HEIGH/4 - quit_img.get_height()/2, quit_img, 1)

pvp_button = Button(WIDTH/2 - pvp_img.get_width()/2, HEIGH/5 - pvp_img.get_height()/2, pvp_img, 1)
pvc_button = Button(WIDTH/2 - pvc_img.get_width()/2, 2*HEIGH/5 - pvc_img.get_height()/2, pvc_img, 1)
cvc_button = Button(WIDTH/2 - cvc_img.get_width()/2, 3*HEIGH/5 - cvc_img.get_height()/2, cvc_img, 1)
quit_button_main = Button(WIDTH/2 - quit_img.get_width()/2, 4*HEIGH/5 - quit_img.get_height()/2, quit_img, 1)

white_button = Button(WIDTH/2 - white_img.get_width()/2, HEIGH/3 - white_img.get_height()/2, white_img, 1)
black_button = Button(WIDTH/2 - black_img.get_width()/2, 2*HEIGH/3 - black_img.get_height()/2, black_img, 1)

depth_button = Button(WIDTH/2 - depth_img.get_width()/2, HEIGH/6 - depth_img.get_height()/2, depth_img, 1)
d1_button = Button(WIDTH/2 - d1_img.get_width()/2, HEIGH/3 - d1_img.get_height()/2, d1_img, 1)
d2_button = Button(WIDTH/2 - d2_img.get_width()/2, HEIGH/2 - d2_img.get_height()/2, d2_img, 1)
d3_button = Button(WIDTH/2 - d3_img.get_width()/2, 2*HEIGH/3 - d3_img.get_height()/2, d3_img, 1)
d4_button = Button(WIDTH/2 - d4_img.get_width()/2, 5*HEIGH/6 - d4_img.get_height()/2, d4_img, 1)





class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGH))
        pygame.display.set_caption('Chess') 
        self.game = Game()
        self.clock = pygame.time.Clock()
        self.engine_1 = Computer(MAX_DEPTH=3, k1=1, usemodel=True)
        self.engine_3 = AI(3)
        # self.engine_3 = Computer_2(MAX_DEPTH=3, k1=1, usemodel=True)
        self.game_state = 0
        self.type_play = 0
        self.depth = 1
        
    MENU_STATE = 0
    PAUSE_STATE = 1
    PLAY_STATE = 2
    OVER_STATE = 3
    CHOOSE_COLOR = 4
    CHOOSE_DEPTH = 5
    PVP = 0
    PVC = 1
    CVC = 2

    def mainloop(self):
        
        self.clock.tick(100)
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = game.board
        game_state = self.game_state
        type_play = self.type_play

        running = True
        player = True
        # player = False
        count = 0
    
        while running:

            # menu state
            if game_state == self.MENU_STATE:
                screen.fill((0, 0, 0))
                if pvp_button.draw(screen):
                    game_state = self.PLAY_STATE
                    type_play = self.PVP
                if pvc_button.draw(screen):
                    type_play = self.PVC
                    game_state = self.CHOOSE_COLOR
                if cvc_button.draw(screen):
                    player = False
                    game_state = self.PLAY_STATE
                    type_play = self.CVC
                if quit_button_main.draw(screen):
                    running = False

            # choose color (black or white)
            if game_state == self.CHOOSE_COLOR:
                screen.fill((0,0,0))
                if white_button.draw(screen):
                    player = True
                    game_state = self.CHOOSE_DEPTH
                if black_button.draw(screen):
                    player = False
                    game_state = self.CHOOSE_DEPTH

            # choose depth
            if game_state == self.CHOOSE_DEPTH:
                screen.fill((0,0,0))
                if depth_button.draw(screen):
                    pass

                if d1_button.draw(screen):
                    count += 1
                    if count == 2:
                        self.depth = 1
                        game_state = self.PLAY_STATE
                        count = 0
                if d2_button.draw(screen):
                    count += 1
                    if count == 2:
                        self.depth = 2
                        game_state = self.PLAY_STATE
                        count = 0
                if d3_button.draw(screen):
                    count += 1
                    if count == 2:
                        self.depth = 3
                        game_state = self.PLAY_STATE
                        count = 0
                if d4_button.draw(screen):
                    count += 1
                    if count == 2:
                        self.depth = 4
                        game_state = self.PLAY_STATE
                        count = 0


            # pause state
            if game_state == self.PAUSE_STATE:
                screen.fill((0, 0, 0))
                if resume_button.draw(screen):
                    game_state = self.PLAY_STATE
                if menu_button.draw(screen):
                    game.reset()
                    game = self.game
                    board = self.game.board
                    screen = self.screen
                    dragger = self.game.dragger
                    game_state = self.MENU_STATE
                if quit_button_pause.draw(screen):
                    running = False

            # play state
            if game_state == self.PLAY_STATE:
                self.clock.tick(100)
                game.show_bg(screen)

                if (dragger.draggging):
                    game.show_move(screen)

                game.show_last_move(screen)

                if (dragger.draggging):
                    game.show_move(screen)

                game.show_hover(screen)

                game.show_pieces(screen)

                # player vs computer
                if type_play == self.PVC:
                    if not player:
                        pygame.display.flip()
                        try:

                            self.engine_1.MAX_DEPTH = self.depth
                            board.push(self.engine_1.getCompMove(board.fen()))

                        except:
                            print("exception line 78")
                        player = True

                # computer vs computer
                if type_play == self.CVC:
                    # WHITE move
                    if player:
                        pygame.display.flip()
                        try:

                            print("ANN thinking ...")
                            # board.push(self.engine_3.calculate_ab(board.fen()))
                            # board.push(self.engine_2.getCompMove(board.fen()))
                            board.push(self.engine_1.getCompMove(board.fen()))

                        except:
                            print("exception line 211")
                        player = False

                    game.show_bg(screen)

                    if (dragger.draggging):
                        game.show_move(screen)

                    game.show_last_move(screen)
                    game.show_pieces(screen)

                    #BLACK move
                    if not player:
                        pygame.display.flip()
                        try:

                            print("Normal heuristics thinking ...")
                            # board.push(self.engine_1.getCompMove(board))
                            board.push(self.engine_3.calculate_ab(board.fen()))

                        except:
                            print("exception line 232")
                        player = True

                if (dragger.draggging):
                    game.update_blit(screen)

                if board.is_game_over():
                    game_state = self.OVER_STATE
                    font1 = pygame.font.SysFont("arialblack", 80)
                    font2 = pygame.font.SysFont("arialblack", 20)

                    if board.result() == '0-1':
                        text = "BLACK WIN"
                        img = font1.render(text, True, (6,57,112))
                        screen.blit(img, (WIDTH / 2 - font1.size(text)[0] / 2, HEIGH / 2 - font1.size(text)[1] / 2))
                    elif board.result() == '1-0':
                        text = "WHITE WIN"
                        img = font1.render(text, True, (6,57,112))
                        screen.blit(img, (WIDTH / 2 - font1.size(text)[0] / 2, HEIGH / 2 - font1.size(text)[1] / 2))
                    else:
                        text = "DRAW"
                        img = font1.render(text, True, (6,57,112))
                        screen.blit(img, (WIDTH / 2 - font1.size(text)[0] / 2, HEIGH / 2 - font1.size(text)[1] / 2))

                    text = "Press SPACE to return to MENU GAME!"
                    img = font2.render(text, True, (6,57,112))
                    screen.blit(img, (WIDTH / 2 - font2.size(text)[0] / 2, 2*HEIGH / 3 - font2.size(text)[1] / 2))

                    print(board.result())

            # game over state
            if game_state == self.OVER_STATE:
                game.reset()
                game = self.game
                board = self.game.board
                screen = self.screen
                dragger = self.game.dragger

            for event in pygame.event.get():

                if (game_state == self.PLAY_STATE) and (type_play != self.CVC):
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
                    if game_state == self.PLAY_STATE:
                        # 'esc' to pause game
                        if event.key == pygame.K_ESCAPE:
                            game_state = self.PAUSE_STATE

                        # 't' to change theme
                        if event.key == pygame.K_t:
                            game.change_theme()

                        # 'r' to reset game
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            board = self.game.board
                            screen = self.screen
                            dragger = self.game.dragger

                        # 'z;' to undo move
                        if event.key == pygame.K_z:
                            # update later
                            game.undo_move()

                    elif game_state == self.PAUSE_STATE:
                        if event.key == pygame.K_ESCAPE:
                            game_state = self.PLAY_STATE

                    elif game_state == self.OVER_STATE:
                        if event.key == pygame.K_SPACE:
                            game_state = self.MENU_STATE
                
                                   
                #quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        
            pygame.display.flip()
                    
main = Main()
main.mainloop()  