from components import Board
from components import speaker,listener,cast_to_tv
import os,time
import pygame

class Player(object):
    def __init__(self,mode,suggestions,cast):
        self.board = Board.Board()
        self.end_of_game = 0
        self.suggestions = suggestions
        self.mode = int(mode)
        self.cast = cast

        if self.mode == 1:
            self.start_single_player()
        if self.mode == 2:
            self.start_two_player()          

    def get_user_input(self,color_of_player):
        try:
            suggestions = []
            cnt = 0
            get_input = True
            while get_input:
                if cnt < 3:
                    speaker.speak('Which position would you like to move?')
                    user_input = listener.listen()
                else:
                    user_input = input('Enter the from position: ')
                
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    from_x_pos,from_y_pos = self.board.convert_to_coordinates(user_input)
                    try:
                        color_of_piece = self.board.get_piece(from_x_pos,from_y_pos).color
                        suggestions = self.board.get_piece(from_x_pos,from_y_pos).get_moves()
                        if color_of_piece == color_of_player:
                            get_input = False
                        else:
                            speaker.speak('Select a piece of '+color_of_player+' color')

                    except AttributeError:
                        speaker.speak('No piece is available in that position')
                else:
                    cnt += 1
                if cnt == 3 and get_input:
                    speaker.speak('I am unable to understand you. Please type the from position')

            if self.suggestions:
                if len(suggestions) > 0:
                    speaker.speak('Suggested moves: ')
                    for pos in self.board.convert_to_position(suggestions):
                        speaker.speak(pos)
                else:
                    speaker.speak('No moves available')
                    return False
                            
            cnt = 0
            get_input = True
            while get_input:
                if cnt < 3:
                    speaker.speak('Where would you like to move to?')
                    user_input = listener.listen()
                else:
                    user_input = input('Enter the to position: ')
                    
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    to_x_pos,to_y_pos= self.board.convert_to_coordinates(user_input)
                    if (to_x_pos,to_y_pos) in suggestions:
                        get_input = False
                    else:
                        speaker.speak('Sorry! You are not allowed to do that')
                else:
                    cnt += 1
                if cnt == 3 and get_input:
                    speaker.speak('I am unable to understand you. Please type the from position')
                        
            return from_x_pos,from_y_pos,to_x_pos,to_y_pos

        except KeyboardInterrupt:
            self.end_of_game = 1
            return 0,0,0,0

    def get_info(self,player_name):
        speaker.speak(player_name+' has to play '+self.board.current_player+' pieces')
        points = self.board.points[self.board.current_player]
        if points > 0:
            speaker.speak(player_name+' has scored '+str(points)+' points')

    def display_board(self):
        path = os.path.split(os.path.realpath(__file__))[0]
        board_size = (750,725)
        piece_size = (60,50)

        screen = pygame.display.set_mode(board_size)
        screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(path,self.board.image)),board_size),(0,0))

        for piece in self.board.filled_positions.values():
            x = piece.x_pos*75
            y = abs(piece.y_pos-9)*75
            screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(path,piece.image)),piece_size),(x,y))

        if self.cast:
            image_path = os.path.join(path,'snapshots/display_'+str(time.time())+'.png')
            print(image_path)
            pygame.image.save(screen,image_path)
            cast_to_tv.cast_image(image_path)
        else:
            pygame.display.flip()
    
    def start_two_player(self):
        player_name = {}
        speaker.speak('What is the name of the player playing white pieces?')
        player_name['white'] = listener.listen()
        speaker.speak('What is the name of the player playing black pieces?')
        player_name['black'] = listener.listen()

        while self.end_of_game == 0:
            self.display_board()
            self.get_info(player_name[self.board.current_player])
            
            from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input(self.board.current_player)

            if self.end_of_game == 0:
                piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                if moved_piece:
                    if cut_piece != None:
                        speaker.speak(cut_piece.name+' is cut by '+piece_to_move.name)
                    if self.board.is_checkmate() or self.board.is_draw:
                        self.end_of_game = 1

        self.display_board()
        if self.board.is_draw:
            speaker.speak('Game drawn due to stalemate')

        else:
            speaker.speak(player_name[self.board.opponent_player]+' wins!!!')


    def start_single_player(self):
        player_name = {}
        speaker.speak('What is your name?')
        name = listener.listen()
        get_color = True
        while get_color:
            speaker.speak('Which side do you want to play? (Black or White): ')
            color_of_player = listener.listen()
            
            if 'white' in color_of_player:
                color_of_player = 'white'
                player_name['white'] = name
                get_color = False
                player_name['black'] = 'Computer'
            elif 'black' in color_of_player:
                color_of_player = 'black'
                player_name['black'] = name
                get_color = False
                player_name['white'] = 'Computer'
            else:
                speaker.speak('What did you say?')

        while self.end_of_game == 0:
            self.display_board()
            self.get_info(player_name[self.board.current_player])
            if color_of_player == self.board.current_player:
                from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input(color_of_player)

                if self.end_of_game == 0:
                    piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                    cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                    if moved_piece:
                        if cut_piece != None:
                            speaker.speak(cut_piece.name+' is cut by '+piece_to_move.name)

            else:
                if self.end_of_game == 0:
                    start_pos,cut_piece,moved_piece = self.board.choose_best_move()
                    if moved_piece:
                        speaker.speak('Moved '+moved_piece.name+' from '+self.board.convert_to_position([(start_pos[0],start_pos[1])])[0]+' to '+self.board.convert_to_position([(moved_piece.x_pos,moved_piece.y_pos)])[0])
                        if cut_piece != None:
                            speaker.speak(cut_piece.name+' is cut by '+moved_piece.name)

            if self.board.is_checkmate() or self.board.is_draw:
                self.end_of_game = 1

        self.display_board()
        if self.board.is_draw:
            speaker.speak('Game drawn due to stalemate')

        else:
            speaker.speak(player_name[self.board.opponent_player]+' wins!!!')
            
if __name__ == '__main__':
    get_choice = True
    while get_choice:
        try:
            user_choice = 0
            speaker.speak('Hi!! Would you like to play in Single player mode or Two player mode?')
            choice = listener.listen()
            if 'single' in choice:
                user_choice = 1
            elif 'two' in choice:
                user_choice = 2
                
            if user_choice in [1,2]:
                cast = False
                speaker.speak('Would you like to cast the display to TV? (yes or no): ')
                cast_choice = listener.listen()
                if 'yes' in cast_choice.lower():
                    cast = True
                
                speaker.speak('Would you like to get move suggestions? (yes or no): ')
                suggestions = listener.listen()
                if 'yes' in suggestions.lower():
                    Player(user_choice,True,cast)
                elif 'no' in suggestions.lower():
                    Player(user_choice,False,cast)
                else:
                    speaker.speak('I did not understand what you said. I will enable suggestions by default.')
                    Player(user_choice,True,cast)
                    
                speaker.speak('Would you like to play a new game? (yes or no): ')
                rematch = listener.listen()
                if 'no' in rematch.lower():
                    get_choice = False
                elif 'yes' in rematch.lower():
                    get_choice = True
                else:
                    speaker.speak('I did not understand what you said. You know what to do if you need me. Bye!')
                    get_choice = False
        except KeyboardInterrupt:
            get_choice = False
            speaker.speak('Exiting...')
