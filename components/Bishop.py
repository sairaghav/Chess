class Bishop(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+'_B'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
        self.board = board

    def get_moves(self,x_start='',y_start=''):
        possible_positions = []

        if x_start == '':
            x_start = self.x_pos
        if y_start == '':
            y_start = self.y_pos

        x_pos = x_start
        y_pos = y_start
        for step in range(1,8):
            x_pos = x_start+step
            y_pos = y_start+step

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
        for step in range(-1,-8,-1):
            x_pos = x_start+step
            y_pos = y_start+step

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
        for step in range(1,8):
            x_pos = x_start-step
            y_pos = y_start+step

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
        for step in range(-1,-8,-1):
            x_pos = x_start-step
            y_pos = y_start+step

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
