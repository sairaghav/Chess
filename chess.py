import sys
from components import Board

class TwoPlayer(object):
    def __init__(self):
        self.board = Board.Board()
        self.end_of_game = 0
        self.suggestions = True

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
        
    def start_play(self):
        try:
            white_player = raw_input('Enter the player playing white pieces: ')
            black_player = raw_input('Enter the player playing black pieces: ')

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
                        sys.exit()
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
                print black_player+' has to play'
                
            sys.exit()

        except KeyboardInterrupt:
            if self.board.opponent_player == 'w':
                print white_player+' wins!!!'
            else:
                print black_player+' has to play'
                
            sys.exit()
            
if __name__ == '__main__':
    TwoPlayer().start_play()
