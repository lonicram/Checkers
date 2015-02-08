
class Engine:

    def __init__(self, state, active_turn):
        self.state = state
        self.active_turn = active_turn
        self.signs = {
            True : 'pawn_white',
            False : 'pawn_black'
        }

    def get_available_moves_for_pawn(self, pawn_cords, turn = ''):
        turn = self.active_turn if turn == '' else turn
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
            if turn == False:
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


    def update_board(self, start_coord, end_coord, turn =''):
        turn = self.active_turn if turn == '' else turn
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
        
        sign = self.signs[turn]
        feature_state[start_coord[0]][start_coord[1]] = None
        feature_state[end_coord[0]][end_coord[1]] = sign

        return feature_state


    def won(self, state, player):
        pass


    def check_game_result(self, state):
        white = 0
        black = 0
        for row in state:
            for field in row:
                if field == self.signs[self.active_turn]:
                    white += 1
                elif field == self.signs[not self.active_turn]:
                    black += 1

        if white == 0:
            return -1
        if black == 0:
            return 1

        return 0


    def get_possible_moves(self, state='', turn=''):
        '''
        Funcion returns moves:
        [pawn cords, target coords]
        '''
        moves=[]
        state = self.state if state == '' else state
        turn = self.active_turn if turn == '' else turn
        for row_key, row in enumerate(state):
            for col_key, field in enumerate(row):
                if field == self.signs[turn]:
                    pawn = [row_key, col_key]
                    moves_for_pawn = self.get_available_moves_for_pawn(pawn)
                    if moves_for_pawn != []:
                        for move in moves_for_pawn:
                            moves.append([pawn, move]);

        return moves

    def get_ai_move(self, board=[], active_turn='', depth = 0):
        '''
        minmax algorithm in very simple version
        '''
        board = self.state if board == [] else board
        active_turn = self.active_turn if active_turn == [] else active_turn
        depth += 1
        game_result = self.check_game_result(board)

        if game_result != 0:
            return game_result
        #
        possible_moves = self.get_possible_moves(board)
        if not possible_moves:
            return game_result
        #
        scores = {}
        print possible_moves
        for key, move in enumerate(possible_moves):
            new_board = list(board)
            new_board = self.update_board(move[0], move[1], active_turn)
            scores[key] = self.get_ai_move(new_board, not active_turn, depth)

        if self.active_turn != active_turn:
            move = max(scores, key=scores.get)
            print 'nextmove'
            print move
            self.next_move = possible_moves[move]
        else:
            move = min(scores, key=scores.get)

        print scores
        return scores[move]


