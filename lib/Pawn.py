class Pawn(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+' Pawn'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 1
        self.is_first_move = True
        self.board = board
        if 'w' in self.color:
            self.image = 'images/white-pawn.png'
        elif 'b' in self.color:
            self.image = 'images/black-pawn.png'
        

    def get_moves(self,x_start='',y_start=''):
        possible_positions = []

        if x_start == '':
            x_start = self.x_pos
        if y_start == '':
            y_start = self.y_pos

        x_pos = x_start
        y_pos = y_start
        if 'b' in self.color.lower():
            y_pos = y_start-1
            if self.is_first_move and self.board.get_piece(x_pos,y_start-2) is None and self.y_pos-2 in range(1,9):
                possible_positions.append((x_pos,self.y_pos-2))
        else:
            y_pos = y_start+1
            if self.is_first_move and self.board.get_piece(x_pos,y_start+2) is None and self.y_pos+2 in range(1,9):
                possible_positions.append((x_pos,self.y_pos+2))

        try:
            self.board.get_piece(x_pos,y_pos).color
        except:
            if y_pos in range(1,9):
                possible_positions.append((x_pos,y_pos))

        for x_step in [-1,1]:
            x_pos = x_start+x_step
            try:
                if self.color != self.board.get_piece(x_pos,y_pos).color and y_pos in range(1,9):
                    possible_positions.append((x_pos,y_pos))
            except:
                pass
   
        return possible_positions
