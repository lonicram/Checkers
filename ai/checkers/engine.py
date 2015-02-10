import copy
import copy_reg
import types
from time import sleep
from random import randint
from multiprocessing import Pool


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Engine:

    def __init__(self, state, turn):
        self.player = True
        self.state = state
        self.next_move = ''
        self.active_player = turn
        self.signs = {
            True: 'pawn_white',
            False: 'pawn_black'
        }

    def get_available_moves_for_pawn(self, pawn_cords, board='', turn=''):
        turn = self.active_player if turn == '' else turn
        board = self.state if board == '' else copy.deepcopy(board)
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
            if turn is False:
                row = pawn_cords[0] + vector[0]
            else:
                row = pawn_cords[0] - vector[0]

            col = pawn_cords[1] + vector[1]

            try:
                value = board[row][col]
                if row > -1 and col > -1:
                    # test if field is empty
                    if value is None and vector in expect_that_empty:
                        available_moves.append([row, col])
                    # test if field next to pawn which we will take is empty
                    # both backward and forward beating
                    elif value == self.signs[not turn]:
                        if turn is False:
                            b_row = row + vector[0]
                        else:
                            b_row = row - vector[0]

                        b_col = col + vector[1]
                        if b_row > -1 and b_col > -1:
                            field_after_jump = board[b_row][b_col]
                            if field_after_jump is None:
                                available_moves.append([b_row, b_col])

            except (KeyError, IndexError):
                # TODO:add something
                pass

        return available_moves

    def update_board(self, start_coord, end_coord, board='', turn=''):
        turn = self.active_player if turn == '' else turn
        board = self.state if board == '' else copy.deepcopy(board)
        feature_state = board
        # check if player has made a beating
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
                    start_coord[0] - 1,
                    start_coord[1] + 1
                ]

            feature_state[removed_pawn[0]][removed_pawn[1]] = 'beaten'

        sign = self.signs[turn]
        feature_state[start_coord[0]][start_coord[1]] = None
        feature_state[end_coord[0]][end_coord[1]] = sign

        return list(feature_state)

    def check_game_result(self, state, get_white_number=False):
        white = 0
        black = 0
        for row in state:
            for field in row:
                if field == 'pawn_white':
                    white += 1
                elif field == 'pawn_black':
                    black += 1

        if black == 0:
            return 100
        if white == 0:
            return -100

        if get_white_number:
            return white
        return 0

    def get_possible_moves(self, state='', turn=''):
        '''
        Funcion returns moves:
        [pawn cords, target coords]
        '''
        av_moves = []
        state = self.state if state == '' else state
        turn = self.active_player if turn == '' else turn
        for row_key, row in enumerate(state):
            for col_key, field in enumerate(row):
                if field == self.signs[turn]:
                    pawn = [row_key, col_key]
                    moves = self.get_available_moves_for_pawn(pawn, state, turn)
                    if moves != []:
                        for move in moves:
                            av_moves.append([pawn, move])

        return av_moves

    def get_ai_move(self, board=[], active_turn='', depth=0):
        '''
        minmax algorithm in very simple version
        '''

        if active_turn == '':
            active_turn = self.player

        game_result = self.check_game_result(board)
        if game_result != 0:
            return game_result

        possible_moves = self.get_possible_moves(board, active_turn)
        if not possible_moves:
            return game_result

        # print possible_moves
        if depth == 5:
            return self.check_game_result(board, True)
        depth += 1
        scores = {}
        pools = []
        if depth == 1:
            for key, move in enumerate(possible_moves):
                new_board = self.update_board(move[0], move[1], board, active_turn)
                c_board = copy.deepcopy(new_board)
                arguments = [c_board, not active_turn, depth]
                pool = Pool(processes=4)
                pools.append(pool.apply_async(self.get_ai_move, arguments))

            for key, pool in enumerate(pools):
                # wait for results
                scores[key] = pool.get()
                pool.close()
        else:

            for key, move in enumerate(possible_moves):
                new_board = self.update_board(move[0], move[1], board, active_turn)
                c_board = copy.deepcopy(new_board)
                scores[key] = self.get_ai_move(c_board, not active_turn, depth)


        if self.player == active_turn:
            move = max(scores, key=scores.get)
            self.next_move = possible_moves[move]
        else:
            move = min(scores, key=scores.get)

        return scores[move]
