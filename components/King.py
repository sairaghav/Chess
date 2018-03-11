class King(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_K'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 10
        self.is_first_move = True
        self.board = board             

    def get_moves(self,x_start='',y_start=''):
        possible_positions = []

        if x_start == '':
            x_start = self.x_pos
        if y_start == '':
            y_start = self.y_pos

        x_pos = x_start
        y_pos = y_start

        for x_step in range(-1,2):
            for y_step in range(-1,2):
                x_pos = x_start+x_step
                y_pos = y_start+y_step
                try:
                    if self.board.get_piece((x_pos,y_pos)).color == self.color:
                        pass
                    else:
                        possible_positions.append((x_pos,y_pos))                   
                except:
                    if not (x_pos == x_start and y_pos == y_start):
                        if x_pos in range(1,9) and y_pos in range(1,9):
                            possible_positions.append((x_pos,y_pos))

        if not self.board.is_castle:
            if self.board.get_piece((self.x_pos-3,self.y_pos)) is None and self.board.get_piece((self.x_pos-2,self.y_pos)) is None and self.board.get_piece((self.x_pos-1,self.y_pos)) is None:
                if self.is_first_move and self.board.get_piece((self.x_pos-4,self.y_pos)).is_first_move and not self.board.is_check[self.color]:
                    possible_positions.append((self.x_pos-2,self.y_pos))

            if self.board.get_piece((self.x_pos+1,self.y_pos)) is None and self.board.get_piece((self.x_pos+2,self.y_pos)) is None:
                if self.is_first_move and self.board.get_piece((self.x_pos+3,self.y_pos)).is_first_move and not self.board.is_check[self.color]:
                    possible_positions.append((self.x_pos+2,self.y_pos))
                        
        return possible_positions
