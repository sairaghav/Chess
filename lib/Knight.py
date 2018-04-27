class Knight(object):
    def __init__(self,color,x_pos,y_pos,board):
        self.color = color.lower()
        self.name = self.color+' Knight'
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.point = 5
        if 'w' in self.color:
            self.image = 'images/white-knight.png'
        elif 'b' in self.color:
            self.image = 'images/black-knight.png'
        self.is_first_move = True
        self.board = board

    def get_moves(self,x_start='',y_start=''):
        possible_positions = []

        if x_start == '':
            x_start = self.x_pos
        if y_start == '':
            y_start = self.y_pos
        
        for step1 in [-2,-1,1,2]:
            for step2 in [-2,-1,1,2]:
                if abs(step1) != abs(step2):
                    x_pos = x_start+step1
                    y_pos = y_start+step2
                    try:
                        if self.board.get_piece(x_pos,y_pos).color == self.color:
                            pass
                        else:
                            if x_pos in range(1,9) and y_pos in range(1,9):
                                possible_positions.append((x_pos,y_pos))
                    except:
                        if x_pos in range(1,9) and y_pos in range(1,9):
                            possible_positions.append((x_pos,y_pos))

        return possible_positions
