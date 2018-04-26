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
            get_input = True
            while get_input:
                user_input = input('Enter the from position: ')
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    from_x_pos,from_y_pos = self.board.convert_to_coordinates(user_input)

                    if self.suggestions:
                        suggestions = self.board.get_piece(from_x_pos,from_y_pos).get_moves()
                        if len(suggestions) > 0:
                            print('Suggested moves: ',end=' ')
                            for pos in self.board.convert_to_position(suggestions):
                                print(pos,end=' ')
                            print('')
                        else:
                            print('No moves available')
                            return False

                    get_input = False

            get_input = True
            while get_input:
                user_input = input('Enter the to position: ')
                if len(user_input) == 2 and user_input.lower()[0] in ['a','b','c','d','e','f','g','h'] and user_input.lower()[1] in ['1','2','3','4','5','6','7','8']:
                    to_x_pos,to_y_pos= self.board.convert_to_coordinates(user_input)
                    get_input = False
            return from_x_pos,from_y_pos,to_x_pos,to_y_pos

        except KeyboardInterrupt:
            self.end_of_game = 1
            return 0,0,0,0
        except AttributeError:
            self.is_draw = True
            return 0,0,0,0
        
    def start_two_player(self):
        white_player = input('Enter the name of player playing white pieces: ')
        black_player = input('Enter the name of player playing black pieces: ')

        while self.end_of_game == 0:
            if self.board.current_player == 'w':
                self.board.display_board(white_player)
            else:
                self.board.display_board(black_player)
                
            from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input()

            if self.end_of_game == 0:
                piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                if piece_to_move is not None and moved_piece:
                    if cut_piece != None:
                        print(cut_piece.name+' is cut by '+piece_to_move.name)
                    if self.board.is_checkmate() or self.board.is_draw:
                        self.end_of_game = 1
                else:
                    print('Invalid Move')

        if self.board.is_draw:
            print('Game drawn due to stalemate')

        else:
            if self.board.opponent_player == 'w':
                self.board.display_board(black_player)
                print(white_player+' wins!!!')
            else:
                self.board.display_board(white_player)
                print(black_player+' wins!!!')


    def start_single_player(self):
        get_color = True
        while get_color:
            color_of_player = input('Which side do you want to play? (Black/White): ')
            if color_of_player.lower() in ['w','white']:
                white_player = input('Enter the player name: ')
                get_color = False
            elif color_of_player.lower() in ['b','black']:
                black_player = input('Enter the player name: ')
                get_color = False
            else:
                print('Did not understand input... Enter \'black\' or \'white\'')

        while self.end_of_game == 0:
            try:
                if self.board.current_player == 'w':
                    self.board.display_board(white_player)
                else:
                    self.board.display_board(black_player)

                from_x_pos,from_y_pos,to_x_pos,to_y_pos = self.get_user_input()

                if self.end_of_game == 0:
                    piece_to_move = self.board.get_piece(from_x_pos,from_y_pos)
                    cut_piece,moved_piece = self.board.make_move(piece_to_move,to_x_pos,to_y_pos)
                    if piece_to_move is not None and moved_piece is not False:
                        if cut_piece != None:
                            print(cut_piece.name+' is cut by '+piece_to_move.name)
                    else:
                        print('Invalid Move')

            except UnboundLocalError:
                if self.end_of_game == 0:
                    start_pos,cut_piece,moved_piece = self.board.choose_best_move()
                    if moved_piece is not False:
                        print('Moved '+moved_piece.name+' from '+self.board.convert_to_position([(start_pos[0],start_pos[1])])[0]+' to '+self.board.convert_to_position([(moved_piece.x_pos,moved_piece.y_pos)])[0])
                        if cut_piece != None:
                            print(cut_piece.name+' is cut by '+moved_piece.name)

            if self.board.is_checkmate() or self.board.is_draw:
                self.end_of_game = 1

        try:
            if self.board.opponent_player == 'w':
                self.board.display_board(white_player)
                print(white_player+' wins!!!')
            else:
                self.board.display_board(black_player)
                print(black_player+' wins!!!')
        except UnboundLocalError:
            pass
            
if __name__ == '__main__':
    get_choice = True
    while get_choice:
        try:
            choice = int(input('Hi!! Would you like to play in \n1. Single player mode\n2. Two player mode\nEnter your choice: '))    
            if choice in [1,2]:
                suggestions = input('Would you like to get move suggestions? (yes/no): ')
                if suggestions.lower() in ['yes','y']:
                    Player(choice,True)
                elif suggestions.lower() in ['no','n']:
                    Player(choice,False)
                else:
                    print('Did not understand input. Suggestions will be enabled by default.')
                    Player(choice,True)
                    
                rematch = input('Would you like to play a new game? (yes/no): ')
                if rematch.lower() in ['no','n']:
                    get_choice = False
                elif rematch.lower() in ['yes','y']:
                    get_choice = True
                else:
                    print('Did not understand input. Exiting...')
            else:
                print('Enter 1 or 2')
        except KeyboardInterrupt:
            get_choice = False
            print('Exiting...')
        except ValueError:
            print('Enter 1 or 2')
