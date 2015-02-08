
class Engine:

    def __init__(self, state, active_turn):
        self.state = state
        self.active_turn = active_turn
        self.signs = {
            True : 'pawn_white',
            False : 'pawn_black'
        }

    def get_available_moves_for_pawn(self, pawn_cords):

        available_moves = []
        available_moves_empty = []
        available_moves_beating = []
        # below we have vectors - or something like vectors
        # [row, column] - important ! may be a little bit confusing
        expect_that_empty = [
            [-1, -1],
            [-1, 1],
        ]

        expect_that_beating_backward = [
            [1, -1],
            [1, 1],
        ]

        for vector in expect_that_empty + expect_that_beating_backward:
            # black always at the bottom - assumption
            if self.active_turn == False:
                row = pawn_cords[0] + vector[0]
            else:
                row = pawn_cords[0] - vector[0]

            col = pawn_cords[1] + vector[1]

            try:
                value = self.state[row][col]
                if row > -1 and col > -1:
                    # test if field is empty
                    if value is None and vector in expect_that_empty:
                        available_moves.append([row, col])
                    # test if field next to pawn which we will take is empty
                    # both backward and forward beating
                    elif value == self.signs[not self.active_turn]:
                        if self.active_turn == False:
                            b_row = row + vector[0]
                        else:
                            b_row = row - vector[0]

                        b_col = col + vector[1]
                        field_after_jump = self.state[b_row][b_col]
                        if field_after_jump is None:
                            available_moves.append([b_row, b_col])

            except (KeyError, IndexError):
                # TODO:add something
                pass

        return available_moves


    def update_board(self, start_coord, end_coord):
        feature_state = list(self.state)
        #check if player has made a beating
        row_diff = end_coord[0] - start_coord[0] 
        col_diff = end_coord[1] - start_coord[1]

        if abs(row_diff) == 2 and abs(col_diff) == 2:
            removed_pawn = []
            # was beating
            if row_diff < 0 and col_diff < 0:
                removed_pawn = [
                    start_coord[0] - 1,
                    start_coord[1] - 1 
                ]
            if row_diff > 0 and col_diff > 0:
                removed_pawn = [
                    start_coord[0] + 1,
                    start_coord[1] + 1
                ]
            if row_diff > 0 and col_diff < 0:
                removed_pawn = [
                    start_coord[0] + 1,
                    start_coord[1] - 1
                ]
            if row_diff < 0 and col_diff > 0:
                removed_pawn = [
                    start_coord[0] - 1 ,
                    start_coord[1] + 1 
                ]

            feature_state[removed_pawn[0]][removed_pawn[1]] = 'beaten' 
        else:
            sign = self.signs[self.active_turn]
            feature_state[end_coord[0]][end_coord[1]] = sign

        return feature_state


    def won(self, state, player):
        pass


    def check_game_result(self, state):
        print state
        if self.won(state, self.player) :
            print 'won ai'
            return 1
        if self.won(state, not self.player) :
            print 'won player'
            return -1
        print 'draw'
        return 0


    def get_possible_moves(self, state='', turn=''):
        '''
        Funcion returns these pawns which can make a move
        '''
        pawns=[]
        state = self.state if state == '' else state
        turn = self.active_turn if turn == '' else turn
        for row_key, row in enumerate(state):
            for col_key, field in enumerate(row):
                if field == self.signs[turn]:
                    coords = [row_key, col_key]
                    if self.get_available_moves_for_pawn(coords) != []:
                        data.append(coords)

        return pawns

    def get_ai_move(self, board, active_turn=''):
        '''
        minmax algorithm in very simple version
        '''

        game_result = self.check_game_result(board)
        if game_result != 0:
            return game_result
        possible_moves = self.get_possible_moves(board)
        if not possible_moves:
            return game_result

        if active_turn == '':
            active_turn = self.player
        scores = {}
        for move in possible_moves:
            new_board = list(board)
            new_board[move] = self.signs[active_turn]
            scores[move] = self.get_ai_move(new_board, not active_turn)

        if self.player == active_turn:
            move = max(scores, key=scores.get)
            self.next_move = move
        else:
            move = min(scores, key=scores.get)

        print scores
        return scores[move]


