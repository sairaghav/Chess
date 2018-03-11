from components import Board

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
            from_x_pos,from_y_pos = self.board.convert_to_coordinates(raw_input('Enter the from position: '))

            if self.suggestions:
                suggestions = self.board.get_piece((from_x_pos,from_y_pos)).get_moves()
                if len(suggestions) > 0:
                    for pos in self.board.convert_to_position(suggestions):
                        print pos,
                    print ''
                else:
                    return False
                
            to_x_pos,to_y_pos= self.board.convert_to_coordinates(raw_input('Enter the to position: '))
            return (from_x_pos,from_y_pos,to_x_pos,to_y_pos)
            
        except AttributeError:
            return False
        
    def start_two_player(self):
        try:
            white_player = raw_input('Enter the name of player playing white pieces: ')
            black_player = raw_input('Enter the name of player playing black pieces: ')

            while self.end_of_game == 0:
                
                if self.board.current_player == 'w':
                    self.board.display_board(white_player)
                else:
                    self.board.display_board(black_player)

                get = True
                while get:
                    try:
                        (from_x_pos,from_y_pos,to_x_pos,to_y_pos) = self.get_user_input()
                        get = False
                    except KeyboardInterrupt:
                        self.end_of_game = 1
                    except:
                        get = True

                piece_to_move = self.board.get_piece((from_x_pos,from_y_pos))
                if piece_to_move is not None and self.board.make_move(piece_to_move,to_x_pos,to_y_pos):
                    if self.board.is_checkmate():
                        self.end_of_game = 1
                else:
                    print 'Invalid Move'

            if self.board.opponent_player == 'w':
                print white_player+' wins!!!'
            else:
                print black_player+' wins!!!'

        except KeyboardInterrupt:
            if self.board.current_player == 'w':
                print white_player+' wins!!!'
            else:
                print black_player+' wins!!!'

    def start_single_player(self):
        try:
            get_color = True
            while get_color:
                color_of_player = raw_input('Which side do you want to play? (Black/White): ')
                if color_of_player.lower() == 'white':
                    white_player = raw_input('Enter the player name: ')
                    get_color = False
                elif color_of_player.lower() == 'black':
                    black_player = raw_input('Enter the player name: ')
                    get_color = False

            while self.end_of_game == 0:
                try:
                    if self.board.current_player == 'w':
                        self.board.display_board(white_player)
                    else:
                        self.board.display_board(black_player)
                    get = True
                    while get:
                        try:
                            (from_x_pos,from_y_pos,to_x_pos,to_y_pos) = self.get_user_input()
                            get = False
                        except KeyboardInterrupt:
                            self.end_of_game = 1
                        except:
                            get = True

                    piece_to_move = self.board.get_piece((from_x_pos,from_y_pos))
                    if piece_to_move is not None and self.board.make_move(piece_to_move,to_x_pos,to_y_pos):
                        pass
                    else:
                        print 'Invalid Move'
                except:
                    self.board.choose_best_move()

                if self.board.is_checkmate():
                    self.end_of_game = 1

            if self.board.opponent_player == 'w':
                print white_player+' wins!!!'
            else:
                print black_player+' wins!!!'

        except KeyboardInterrupt:
            if self.board.current_player == 'w':
                print white_player+' wins!!!'
            else:
                print black_player+' wins!!!'
            
if __name__ == '__main__':
    get_choice = True
    while get_choice:
        choice = int(raw_input('Hi!! Would you like to play in \n1. Single player mode\n2. Two player mode\nEnter your choice: '))
        suggestions = raw_input('Would you like to get move suggestions? (yes/no): ')

        if choice in [1,2]:
            if suggestions.lower() in ['yes','y']:
                Player(choice,True)
            else:
                Player(choice,False)
            rematch = raw_input('Would you like to play a new game? (yes/no): ')
            if not rematch.lower() in ['yes']:
                get_choice = False
        else:
            print 'Invalid choice'
