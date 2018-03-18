import Rook,Knight,Bishop,King,Queen,Pawn

class Board(object):
    def __init__(self):
        self.cut_pieces = []
        self.filled_positions = {}
        self.king_positions = {'w':'','b':''}
        self.points = {'w':0,'b':0}
        self.is_check = {'w':False,'b':False}
        self.current_player = 'w'
        self.opponent_player = 'b'
        self.is_castle = False
        self.is_draw = False
    
        self.set_board(Rook.Rook('w',1,1,self))
        self.set_board(Knight.Knight('w',2,1,self))
        self.set_board(Bishop.Bishop('w',3,1,self))
        self.white_queen = self.set_board(Queen.Queen('w',4,1,self))
        self.set_board(King.King('w',5,1,self))
        self.set_board(Bishop.Bishop('w',6,1,self))
        self.set_board(Knight.Knight('w',7,1,self))
        self.set_board(Rook.Rook('w',8,1,self))
        self.set_board(Pawn.Pawn('w',1,2,self))
        self.set_board(Pawn.Pawn('w',2,2,self))
        self.set_board(Pawn.Pawn('w',3,2,self))
        self.set_board(Pawn.Pawn('w',4,2,self))
        self.set_board(Pawn.Pawn('w',5,2,self))
        self.set_board(Pawn.Pawn('w',6,2,self))
        self.set_board(Pawn.Pawn('w',7,2,self))
        self.set_board(Pawn.Pawn('w',8,2,self))

        self.set_board(Rook.Rook('b',1,8,self))
        self.set_board(Knight.Knight('b',2,8,self))
        self.set_board(Bishop.Bishop('b',3,8,self))
        self.black_queen = self.set_board(Queen.Queen('b',4,8,self))
        self.set_board(King.King('b',5,8,self))
        self.set_board(Bishop.Bishop('b',6,8,self))
        self.set_board(Knight.Knight('b',7,8,self))
        self.set_board(Rook.Rook('b',8,8,self))
        self.set_board(Pawn.Pawn('b',1,7,self))
        self.set_board(Pawn.Pawn('b',2,7,self))
        self.set_board(Pawn.Pawn('b',3,7,self))
        self.set_board(Pawn.Pawn('b',4,7,self))
        self.set_board(Pawn.Pawn('b',5,7,self))
        self.set_board(Pawn.Pawn('b',6,7,self))
        self.set_board(Pawn.Pawn('b',7,7,self))
        self.set_board(Pawn.Pawn('b',8,7,self))

    def get_piece(self,(x_pos,y_pos)):
        return self.filled_positions.get((x_pos,y_pos),None)

    def get_position(self,piece):
        return (piece.x_pos,piece.y_pos)

    def convert_to_coordinates(self,position):
        if len(position) != 2:
            return False
        else:
            x = position.lower()[0]
            y = int(position.lower()[1])

            x_vals = ['','a','b','c','d','e','f','g','h']

            if x in x_vals:
                x = x_vals.index(x)

            return x,y

    def convert_to_position(self,coordinates):
        x_vals = ['','A','B','C','D','E','F','G','H']
        positions = []
        
        for (x_pos,y_pos) in coordinates:
            x_pos = x_vals[x_pos]
            y_pos = str(y_pos)
            positions.append(x_pos+y_pos)

        return positions

    def set_board(self,piece):
        x_pos = piece.x_pos
        y_pos = piece.y_pos
        self.filled_positions[(x_pos,y_pos)] = piece
        if '_K' in piece.name:
            self.king_positions[piece.color] = (x_pos,y_pos)
            
        return self.filled_positions

    def display_board(self,player_name):
        diff = 0
        x_header = ['','1','2','3','4','5','6','7','8','']
        y_header = ['','A','B','C','D','E','F','G','H','']

        if self.current_player == 'b':
            diff = 9
            x_header = ['','8','7','6','5','4','3','2','1','']
            y_header = ['','H','G','F','E','D','C','B','A','']
        for y in range(9,-1,-1):
            for x in range(10):
                if (abs(x-diff),abs(y-diff)) in self.filled_positions.keys():
                    print self.get_piece((abs(x-diff),abs(y-diff))).name+'\t',
                else:
                    if x == 0 or x == 9:
                        print x_header[y]+'\t',
                    elif y == 0 or y == 9:
                        print y_header[x]+'\t',
                    else:
                        print '\t',
            print '\n'

        print player_name+' has to play'
        print 'Pieces not available: ',
        if len(self.cut_pieces) == 0:
            print 'Nil'
        else:
            for cut_piece in self.cut_pieces:
                if self.current_player in cut_piece.name:
                    print cut_piece.name,
            print ''

        print 'Points: '+str(self.points[self.current_player])

    def get_all_moves(self):
        all_available_moves = {}
        current_player_moves = {}
        opponent_player_moves = {}
        for piece in self.filled_positions.values():
            if piece.color == self.current_player:
                current_player_moves[piece] = piece.get_moves()
                all_available_moves[self.current_player] = current_player_moves
            if piece.color == self.opponent_player:
                opponent_player_moves[piece] = piece.get_moves()
                all_available_moves[self.opponent_player] = opponent_player_moves

        return all_available_moves

    def check_for_check(self):
        for position in self.get_all_moves()[self.opponent_player].values():
            if self.king_positions[self.current_player] in position:
                self.is_check[self.current_player] = True
                break
            else:
                self.is_check[self.current_player] = False

        for position in self.get_all_moves()[self.current_player].values():
            if self.king_positions[self.opponent_player] in position:
                self.is_check[self.opponent_player] = True
                break
            else:
                self.is_check[self.opponent_player] = False

    def is_checkmate(self):
        if self.is_check[self.current_player]:
            for piece,positions in self.get_all_moves()[self.current_player].iteritems():
                for position in positions:
                    x_pos = position[0]
                    y_pos = position[1]

                    (x_start,y_start) = self.get_position(piece)
                    piece_to_reverse = self.get_piece((x_pos,y_pos))
                    if piece_to_reverse is None:
                        piece_to_reverse = piece

                    player_before_move = self.current_player

                    self.make_move(piece,x_pos,y_pos)

                    if player_before_move is not self.current_player:
                        if not self.is_check[self.opponent_player]:
                            self.reverse_move(piece,x_start,y_start,piece.x_pos,piece.y_pos,piece_to_reverse)

                            return False

            return True
        else:
            return False

    def reverse_move(self,piece,x_start,y_start,x_pos,y_pos,piece_to_reverse):
        temp = self.current_player
        self.current_player = self.opponent_player
        self.opponent_player = temp

        if self.is_castle:
            if x_pos-x_start == 2:
                self.filled_positions.pop((piece.x_pos,piece.y_pos))
                piece.x_pos = piece.x_pos-2
                self.filled_positions[(piece.x_pos,piece.y_pos)] = piece

                rook_piece = self.get_piece((x_pos+1,y_pos))
                self.filled_positions.pop((rook_piece.x_pos,rook_piece.y_pos))
                rook_piece.x_pos = rook_piece.x_pos-3
                self.filled_positions[(rook_piece.x_pos,rook_piece.y_pos)] = rook_piece
            else:
                self.filled_positions.pop((piece.x_pos,piece.y_pos))
                piece.x_pos = piece.x_pos+2
                self.filled_positions[(piece.x_pos,piece.y_pos)] = piece

                rook_piece = self.get_piece((x_pos+3,y_pos))
                self.filled_positions.pop((rook_piece.x_pos,rook_piece.y_pos))
                rook_piece.x_pos = rook_piece.x_pos+2
                self.filled_positions[(rook_piece.x_pos,rook_piece.y_pos)] = rook_piece
        else:     
            self.filled_positions[(x_start,y_start)] = piece
            self.filled_positions.pop((x_pos,y_pos))
            
            if piece_to_reverse is not piece:
                self.filled_positions[(x_pos,y_pos)] = piece_to_reverse
                self.cut_pieces.remove(piece_to_reverse)
                self.points[self.current_player] -= piece_to_reverse.point

        if '_K' in piece.name:
            self.king_positions[piece.color] = (x_start,y_start)

        piece.x_pos = x_start
        piece.y_pos = y_start

        return True

    def make_move(self,piece,x_pos,y_pos):
        cut_piece = None
        if (x_pos,y_pos) in piece.get_moves() and piece.color == self.current_player:
            (x_start,y_start) = self.get_position(piece)
            piece_to_reverse = piece
            
            if '_K' in piece.name and abs(x_pos-piece.x_pos) == 2:
                (x_start,y_start) = self.get_position(piece)
                self.is_castle = True
                
                if x_pos-piece.x_pos == 2:
                    rook_piece = self.get_piece((x_pos+1,y_pos))
                    self.filled_positions.pop((rook_piece.x_pos,rook_piece.y_pos))
                    rook_piece.x_pos = rook_piece.x_pos-2
                    self.filled_positions[(rook_piece.x_pos,rook_piece.y_pos)] = rook_piece

                    self.filled_positions.pop((piece.x_pos,piece.y_pos))
                    piece.x_pos = piece.x_pos+2
                    self.filled_positions[(piece.x_pos,piece.y_pos)] = piece

                else:
                    rook_piece = self.get_piece((x_pos-2,y_pos))
                    self.filled_positions.pop((rook_piece.x_pos,rook_piece.y_pos))
                    rook_piece.x_pos = rook_piece.x_pos+3
                    self.filled_positions[(rook_piece.x_pos,rook_piece.y_pos)] = rook_piece

                    self.filled_positions.pop((piece.x_pos,piece.y_pos))
                    piece.x_pos = piece.x_pos-2
                    self.filled_positions[(piece.x_pos,piece.y_pos)] = piece

            else:
                old_piece = self.get_piece((x_pos,y_pos))
               
                if old_piece is None:
                    self.filled_positions[(x_pos,y_pos)] = piece
                    self.filled_positions.pop((x_start,y_start))
                else:
                    if old_piece.color == piece.color:
                        return cut_piece,False
                    else:
                        cut_piece = old_piece
                        piece_to_reverse = old_piece
                        self.cut_pieces.append(old_piece)
                        self.points[self.current_player] += old_piece.point
                        self.filled_positions[(x_pos,y_pos)] = piece
                        self.filled_positions.pop((x_start,y_start))
     
                piece.x_pos = x_pos
                piece.y_pos = y_pos

            if '_K' in piece.name:
                self.king_positions[piece.color] = (x_pos,y_pos)

            temp = self.current_player
            self.current_player = self.opponent_player
            self.opponent_player = temp
     
            self.check_for_check()
     
            if self.is_check[self.opponent_player]:
                self.reverse_move(piece,x_start,y_start,x_pos,y_pos,piece_to_reverse)
            else:
                piece.is_first_move = False

                if 'w_P' in piece.name and piece.y_pos == 8:
                    if self.white_queen in self.cut_pieces:
                        cut_pieces.remove(self.white_queen)
                        self.filled_positions[(piece.x_pos,piece.y_pos)] = white_queen
                        white_queen.x_pos = piece.x_pos
                        white_queen.y_pos = piece.y_pos
                        cut_pieces.append(piece)
                    else:
                        white_queen2 = self.set_board(Queen.Queen('w',piece.x_pos,piece.y_pos,self))

                if 'b_P' in piece.name and piece.y_pos == 1:
                    if self.black_queen in self.cut_pieces:
                        cut_pieces.remove(self.black_queen)
                        self.filled_positions[(piece.x_pos,piece.y_pos)] = black_queen
                        black_queen.x_pos = piece.x_pos
                        black_queen.y_pos = piece.y_pos
                        cut_pieces.append(piece)
                    else:
                        white_queen2 = self.set_board(Queen.Queen('b',piece.x_pos,piece.y_pos,self))
                    

            self.is_castle = False

        else:
            return cut_piece,False
           
        return cut_piece,piece

    def choose_best_move(self):
        max_points = 0
        starting_points = self.points[self.current_player]
        start_pos = ''
        best_piece = ''
        best_position = ''
        cut_piece = None
        for piece,positions in self.get_all_moves()[self.current_player].iteritems():
            for position in positions:
                x_pos = position[0]
                y_pos = position[1]

                (x_start,y_start) = self.get_position(piece)
                piece_to_reverse = self.get_piece((x_pos,y_pos))
                if piece_to_reverse is None:
                    piece_to_reverse = piece

                player_before_move = self.current_player
                self.make_move(piece,x_pos,y_pos)

                if player_before_move is not self.current_player:
                    points_gained = self.points[player_before_move] - starting_points
                    self.reverse_move(piece,x_start,y_start,piece.x_pos,piece.y_pos,piece_to_reverse)

                    if points_gained >= max_points:
                        max_points = points_gained
                        best_piece = piece
                        best_position = position
                        start_pos = (x_start,y_start)

        if len(best_position) > 0:
            cut_piece,best_piece = self.make_move(best_piece,best_position[0],best_position[1])
            return start_pos,cut_piece,best_piece
        else:
            self.is_draw = True
            return start_pos,cut_piece,False
                
            
        
