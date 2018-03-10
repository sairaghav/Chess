import sys
from components import Board

class TwoPlayer(object):
    def __init__(self):
        self.board = Board.Board()
        self.end_of_game = 0
        self.suggestions = True

    def convert_to_coordinates(self,position):
        try:
            x = position.lower()[0]
            y = int(position.lower()[1])

            x_vals = ['','a','b','c','d','e','f','g','h']

            if x in x_vals:
                x = x_vals.index(x)

            return x,y
        except:
            return False

    def convert_to_position(self,coordinates):
        x_vals = ['','A','B','C','D','E','F','G','H']
        positions = []
        
        for (x_pos,y_pos) in coordinates:
            x_pos = x_vals[x_pos]
            y_pos = str(y_pos)
            positions.append(x_pos+y_pos)

        return positions

    def get_user_input(self):
        print self.board.current_player+' has to play'
        try:
            from_x_pos,from_y_pos = self.convert_to_coordinates(raw_input('Enter the from position: '))

            if self.suggestions:
                suggestions = self.board.get_piece((from_x_pos,from_y_pos)).get_moves()
                if len(suggestions) > 0:
                    for pos in self.convert_to_position(suggestions):
                        print pos,
                    print ''
                else:
                    return False
                
            to_x_pos,to_y_pos= self.convert_to_coordinates(raw_input('Enter the to position: '))
            return (from_x_pos,from_y_pos,to_x_pos,to_y_pos)
            
        except AttributeError,KeyboardInterrupt:
            return False
        
    def start_play(self):
        while self.end_of_game == 0:
            self.board.display_board()

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
                    print self.board.opponent_player+' wins!!'
                    sys.exit()
            else:
                print 'Invalid Move'
            
if __name__ == '__main__':
    TwoPlayer().start_play()
