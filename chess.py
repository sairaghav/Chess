from components import Board
from components import speaker,listener

class Player(object):
    def __init__(self,mode,suggestions):
        self.board = Board.Board()
        self.end_of_game = 0
        self.suggestions = suggestions
        self.mode = int(mode)

        if self.mode == 1:
            self.start_single_player()
        if self.mode == 2:
            self.start_two_player()          

    def get_user_input(self):
        try:
            get_input = True
            while get_input:
                speaker.speak('Enter the from position: ')
                user_input = listener.listen()
                
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    from_x_pos,from_y_pos = self.board.convert_to_coordinates(user_input)

                    if self.suggestions:
                        suggestions = self.board.get_piece(from_x_pos,from_y_pos).get_moves()
                        if len(suggestions) > 0:
                            speaker.speak('Suggested moves: ')
                            for pos in self.board.convert_to_position(suggestions):
                                speaker.speak(pos)
                        else:
                            speaker.speak('No moves available')
                            return False

                    get_input = False

            get_input = True
            while get_input:
                speaker.speak('Enter the to position: ')
                user_input = listener.listen()
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    to_x_pos,to_y_pos= self.board.convert_to_coordinates(user_input)
                    get_input = False
            return from_x_pos,from_y_pos,to_x_pos,to_y_pos

        except KeyboardInterrupt:
            self.end_of_game = 1
            return 0,0,0,0
        except AttributeError:
            self.is_draw = True
            return 0,0,0,0
        
    def start_two_player(self):
        speaker.speak('Enter the name of player playing white pieces: ')
        white_player = listener.listen()
        speaker.speak('Enter the name of player playing black pieces: ')
        black_player = listener.listen()

        while self.end_of_game == 0:
            if self.board.current_player == 'w':
                self.board.display_board(white_player)
            else:
                self.board.display_board(black_player)
                
            from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input()

            if self.end_of_game == 0:
                piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                if piece_to_move is not None and moved_piece:
                    if cut_piece != None:
                        speaker.speak(cut_piece.name+' is cut by '+piece_to_move.name)
                    if self.board.is_checkmate() or self.board.is_draw:
                        self.end_of_game = 1
                else:
                    speaker.speak('Invalid Move')

        if self.board.is_draw:
            speaker.speak('Game drawn due to stalemate')

        else:
            if self.board.opponent_player == 'w':
                self.board.display_board(black_player)
                speaker.speak(white_player+' wins!!!')
            else:
                self.board.display_board(white_player)
                speaker.speak(black_player+' wins!!!')


    def start_single_player(self):
        get_color = True
        while get_color:
            speaker.speak('Which side do you want to play? (Black/White): ')
            color_of_player = listener.listen()
            if color_of_player.lower() in ['w','white']:
                speaker.speak('Enter the player name: ')
                white_player = listener.listen()
                get_color = False
            elif color_of_player.lower() in ['b','black']:
                speaker.speak('Enter the player name: ')
                black_player = listener.listen()
                get_color = False
            else:
                speaker.speak('Did not understand input... Enter \'black\' or \'white\'')

        while self.end_of_game == 0:
            try:
                if self.board.current_player == 'w':
                    self.board.display_board(white_player)
                else:
                    self.board.display_board(black_player)

                from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input()

                if self.end_of_game == 0:
                    piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                    cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                    if piece_to_move is not None and moved_piece is not False:
                        if cut_piece != None:
                            speaker.speak(cut_piece.name+' is cut by '+piece_to_move.name)
                    else:
                        speaker.speak('Invalid Move')

            except UnboundLocalError:
                if self.end_of_game == 0:
                    start_pos,cut_piece,moved_piece = self.board.choose_best_move()
                    if moved_piece is not False:
                        speaker.speak('Moved '+moved_piece.name+' from '+self.board.convert_to_position([(start_pos[0],start_pos[1])])[0]+' to '+self.board.convert_to_position([(moved_piece.x_pos,moved_piece.y_pos)])[0])
                        if cut_piece != None:
                            speaker.speak(cut_piece.name+' is cut by '+moved_piece.name)

            if self.board.is_checkmate() or self.board.is_draw:
                self.end_of_game = 1

        try:
            if self.board.opponent_player == 'w':
                self.board.display_board(white_player)
                speaker.speak(white_player+' wins!!!')
            else:
                self.board.display_board(black_player)
                speaker.speak(black_player+' wins!!!')
        except UnboundLocalError:
            pass
            
if __name__ == '__main__':
    get_choice = True
    while get_choice:
        try:
            speaker.speak('Hi!! Would you like to play in \n1. Single player mode\n2. Two player mode\nEnter your choice: ')
            choice = listener.listen()
            if choice == 'single':
                user_choice = 1
            else:
                user_choice = 2
                
            if user_choice in [1,2]:
                speaker.speak('Would you like to get move suggestions? (yes/no): ')
                suggestions = listener.listen()
                if suggestions.lower() in ['yes','y']:
                    Player(user_choice,True)
                elif suggestions.lower() in ['no','n']:
                    Player(user_choice,False)
                else:
                    speaker.speak('Did not understand input. Suggestions will be enabled by default.')
                    Player(user_choice,True)
                    
                speaker.speak('Would you like to play a new game? (yes/no): ')
                rematch = listener.listen()
                if rematch.lower() in ['no','n']:
                    get_choice = False
                elif rematch.lower() in ['yes','y']:
                    get_choice = True
                else:
                    speaker.speak('Did not understand input. Exiting...')
            else:
                speaker.speak('Enter 1 or 2')
        except KeyboardInterrupt:
            get_choice = False
            speaker.speak('Exiting...')
        except ValueError:
            speaker.speak('Enter 1 or 2')
