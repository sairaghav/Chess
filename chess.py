import sys
class Board(object):
    cut_pieces = []
    filled_positions = {}
    end_of_game = 0
    current_player = 'w'

    def __init__(self):
        self.set_board(Rook('w',0,0,self))
        self.set_board(Knight('w',1,0,self))
        self.set_board(Bishop('w',2,0,self))
        self.set_board(Queen('w',3,0,self))
        self.set_board(King('w',4,0,self))
        self.set_board(Bishop('w',5,0,self))
        self.set_board(Knight('w',6,0,self))
        self.set_board(Rook('w',7,0,self))
        self.set_board(Pawn('w',0,1,self))
        self.set_board(Pawn('w',1,1,self))
        self.set_board(Pawn('w',2,1,self))
        self.set_board(Pawn('w',3,1,self))
        self.set_board(Pawn('w',4,1,self))
        self.set_board(Pawn('w',5,1,self))
        self.set_board(Pawn('w',6,1,self))
        self.set_board(Pawn('w',7,1,self))

        self.set_board(Pawn('b',0,6,self))
        self.set_board(Pawn('b',1,6,self))
        self.set_board(Pawn('b',2,6,self))
        self.set_board(Pawn('b',3,6,self))
        self.set_board(Pawn('b',4,6,self))
        self.set_board(Pawn('b',5,6,self))
        self.set_board(Pawn('b',6,6,self))
        self.set_board(Pawn('b',7,6,self))
        self.set_board(Rook('b',7,7,self))
        self.set_board(Knight('b',6,7,self))
        self.set_board(Bishop('b',5,7,self))
        self.set_board(Queen('b',3,7,self))
        self.set_board(King('b',4,7,self))
        self.set_board(Bishop('b',2,7,self))
        self.set_board(Knight('b',1,7,self))
        self.set_board(Rook('b',0,7,self))

    def get_user_input(self):
        print Board.current_player+' has to play'
        from_pos = raw_input('Enter the from position: ')
        from_x_pos = int(from_pos.split(',')[0].strip())
        from_y_pos = int(from_pos.split(',')[1].strip())
        if not from_x_pos in range(8) and from_y_pos in range(8):
            return False

        try:
            print self.get_piece((from_x_pos,from_y_pos)).get_moves()
        except AttributeError:
            return False

        to_pos= raw_input('Enter the to position: ')
        to_x_pos = int(to_pos.split(',')[0].strip())
        to_y_pos = int(to_pos.split(',')[1].strip())
        if not to_x_pos in range(8) and to_y_pos in range(8):
            return False

        return (from_x_pos,from_y_pos,to_x_pos,to_y_pos)

    def get_piece(self,(x_pos,y_pos)):
        return Board.filled_positions.get((x_pos,y_pos),None)

    def get_position(self,piece):
        return (piece.x_pos,piece.y_pos)

    def set_board(self,piece):
        x_pos = piece.x_pos
        y_pos = piece.y_pos
        Board.filled_positions[(x_pos,y_pos)] = piece
        return Board.filled_positions

    def display_board(self):
        for y in range(7,-1,-1):
            for x in range(8):
                print str((x,y)),
                if (x,y) in Board.filled_positions.keys():
                    print self.get_piece((x,y)).name+'\t',
                else:
                    print '\t\t',
            print '\n'

    def get_white_moves(self):
        white_available_moves = {}
        for piece in Board.filled_positions.values():
            if piece.color == 'w':
                white_available_moves[piece.name+'('+str(piece.x_pos)+','+str(piece.y_pos)+')'] = piece.get_moves()

        return white_available_moves

    def get_black_moves(self):
        black_available_moves = {}
        for piece in Board.filled_positions.values():
            if piece.color == 'b':
                black_available_moves[piece.name+'('+str(piece.x_pos)+','+str(piece.y_pos)+')'] = piece.get_moves()

        return black_available_moves

    def get_all_moves(self):
        white_available_moves = []
        black_available_moves = []
        for piece in Board.filled_positions.values():
            if piece.color == 'b':
                for val in piece.get_moves():
                    black_available_moves.append(val)
            if piece.color == 'w':
                for val in piece.get_moves():
                    white_available_moves.append(val)                    

        return {'w':white_available_moves,'b':black_available_moves}
            

    def make_move(self,piece,x_pos,y_pos):
        (x_start,y_start) = self.get_position(piece)

        if (x_pos,y_pos) in piece.get_moves():
            old_piece = self.get_piece((x_pos,y_pos))
            
            if old_piece is None:
                Board.filled_positions[(x_pos,y_pos)] = piece
                Board.filled_positions.pop((x_start,y_start))
            else:
                if old_piece.color == piece.color:
                    return False
                else:
                    Board.cut_pieces.append(old_piece)
                    Board.filled_positions[(x_pos,y_pos)] = piece
                    Board.filled_positions.pop((x_start,y_start))
        else:
            return False

        piece.x_pos = x_pos
        piece.y_pos = y_pos
        try:
            piece.is_first_move = False
        except:
            pass
                
        return Board.filled_positions

class Rook(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_R'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
        self.is_first_move = True
        self.board = board

    def get_moves(self):
        possible_positions = []

        x_pos = self.x_pos
        y_pos = self.y_pos
        for x_step in range(1,8):
            x_pos = self.x_pos+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for x_step in range(-1,-8,-1):
            x_pos = self.x_pos+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for y_step in range(1,8):
            y_pos = self.y_pos+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for y_step in range(-1,-8,-1):
            y_pos = self.y_pos+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))
       
        return possible_positions

class Knight(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_H'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
        self.board = board

    def get_moves(self):
        possible_positions = []
        
        for step1 in range(-2,3):
            for step2 in range(-2,3):
                if abs(step1) != abs(step2) and step1 != 0 and step2 != 0:
                    x_pos = self.x_pos+step1
                    y_pos = self.y_pos+step2
                    try:
                        if self.board.get_piece((x_pos,y_pos)).color == self.color:
                            break
                        else:
                            possible_positions.append((x_pos,y_pos))
                            break
                    except:
                        pass
                    if x_pos in range(8) and y_pos in range(8):
                        possible_positions.append((x_pos,y_pos))

        return possible_positions

class Bishop(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_B'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
        self.board = board

    def get_moves(self):
        possible_positions = []

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(1,8):
            x_pos = self.x_pos+step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(-1,-8,-1):
            x_pos = self.x_pos+step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(1,8):
            x_pos = self.x_pos-step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(-1,-8,-1):
            x_pos = self.x_pos-step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))
                
        return possible_positions

class Queen(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_Q'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 10
        self.board = board
    
    def get_moves(self):
        possible_positions = []

        x_pos = self.x_pos
        y_pos = self.y_pos
        for x_step in range(1,8):
            x_pos = self.x_pos+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for x_step in range(-1,-8,-1):
            x_pos = self.x_pos+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for y_step in range(1,8):
            y_pos = self.y_pos+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for y_step in range(-1,-8,-1):
            y_pos = self.y_pos+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))
                    
        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(1,8):
            x_pos = self.x_pos+step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(-1,-8,-1):
            x_pos = self.x_pos+step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(1,8):
            x_pos = self.x_pos-step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))

        x_pos = self.x_pos
        y_pos = self.y_pos
        for step in range(-1,-8,-1):
            x_pos = self.x_pos-step
            y_pos = self.y_pos+step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                pass

            if x_pos in range(8) and y_pos in range(8):
                possible_positions.append((x_pos,y_pos))
            
        return possible_positions

class King(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_K'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 10
        self.is_first_move = True
        self.is_check = False
        self.board = board

    def check_for_check(self,possible_positions):
        final_positions = possible_positions
        for position in possible_positions:
            if self.color == 'w':
                for val in self.board.get_all_moves['b'].values:
                    if position in val:
                        final_positions.remove(position)
            if self.color == 'b':
                for val in self.board.get_all_moves['w'].values:
                    if position in val:
                        final_positions.remove(position)

        print possible_positions
        return final_positions              

    def get_moves(self):
        possible_positions = []

        x_pos = self.x_pos
        y_pos = self.y_pos

        for x_step in range(-1,2):
            for y_step in range(-1,2):
                x_pos = self.x_pos+x_step
                y_pos = self.y_pos+y_step
                try:
                    if self.board.get_piece((x_pos,y_pos)).color == self.color:
                        break
                    else:
                        possible_positions.append((x_pos,y_pos))
                        break
                except:
                    pass
                if not (x_pos == self.x_pos and y_pos == self.y_pos):
                    if x_pos in range(8) and y_pos in range(8):
                        possible_positions.append((x_pos,y_pos))

        possible_positions = self.check_for_check(possible_positions)
                        
        return possible_positions

class Pawn(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_P'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 1
        self.is_first_move = True
        self.board = board
        

    def get_moves(self):
        possible_positions = []

        x_pos = self.x_pos
        y_pos = self.y_pos
        if self.color.lower() == 'b':
            y_pos = self.y_pos-1
            if self.is_first_move and self.board.get_piece((x_pos,self.y_pos-2)) is None:
                possible_positions.append((x_pos,self.y_pos-2))
        else:
            y_pos = self.y_pos+1
            if self.is_first_move and self.board.get_piece((x_pos,self.y_pos+2)) is None:
                possible_positions.append((x_pos,self.y_pos+2))

        try:
            self.board.get_piece((x_pos,y_pos)).color
        except:
            possible_positions.append((x_pos,y_pos))

        for x_step in [-1,1]:
            x_pos = self.x_pos+x_step
            try:
                if self.color != self.board.get_piece((x_pos,y_pos)).color:
                    possible_positions.append((x_pos,y_pos))
            except:
                pass
   
        return possible_positions

class TwoPlayer(object):
    def __init__(self):
        self.board = Board()
        

    def start_play(self):
        while Board.end_of_game == 0:
            self.board.display_board()

            get = False
            while not get:
                try:
                    (from_x_pos,from_y_pos,to_x_pos,to_y_pos) = self.board.get_user_input()
                    get = True
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    get = False

            piece_to_move = self.board.get_piece((from_x_pos,from_y_pos))
            if piece_to_move is not None:
                if piece_to_move.color.lower() == Board.current_player.lower():
                    if self.board.make_move(piece_to_move,to_x_pos,to_y_pos):
                        if Board.current_player.lower() == 'w':
                           Board.current_player = 'b'
                        else:
                            Board.current_player = 'w'
                    else:
                        print 'Invalid Move'
                else:
                    print 'Wrong piece moved'
            else:
                print 'Invalid Move'
            
            

if __name__ == '__main__':
    TwoPlayer().start_play()
