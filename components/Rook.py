class Rook(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_R'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
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
        for x_step in range(1,8):
            x_pos = x_start+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                if x_pos in range(1,9) and y_pos in range(1,9):
                    possible_positions.append((x_pos,y_pos))

        x_pos = x_start
        y_pos = y_start
        for x_step in range(-1,-8,-1):
            x_pos = x_start+x_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                if x_pos in range(1,9) and y_pos in range(1,9):
                    possible_positions.append((x_pos,y_pos))  

        x_pos = x_start
        y_pos = y_start
        for y_step in range(1,8):
            y_pos = y_start+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                if x_pos in range(1,9) and y_pos in range(1,9):
                    possible_positions.append((x_pos,y_pos))

        x_pos = x_start
        y_pos = y_start
        for y_step in range(-1,-8,-1):
            y_pos = y_start+y_step

            try:
                if self.board.get_piece((x_pos,y_pos)).color == self.color:
                    break
                else:
                    possible_positions.append((x_pos,y_pos))
                    break
            except:
                if x_pos in range(1,9) and y_pos in range(1,9):
                    possible_positions.append((x_pos,y_pos))
       
        return possible_positions
