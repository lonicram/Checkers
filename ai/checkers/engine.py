
class Engine:

    def __init__(self, state, active_turn):
        self.state = state
        self.active_turn = active_turn
        self.signs = {
            True : 'white',
            False : 'black'
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

        for vector in expect_that_empty:
            # black always at the botto - assumption
            if self.active_turn == False:
                row = pawn_cords[0] + vector[0]
            else:
                row = pawn_cords[0] - vector[0]

            col = pawn_cords[1] + vector[1]

            try:
                value = self.state[row][col]
                if row > -1 and col > -1:
                    # test if field is empty
                    if value is None:
                        available_moves_empty.append([row, col])
                    # test if field next to pawn which we will take is empty
                    elif value == self.signs[not self.active_turn]:
                        if self.active_turn == False:
                            b_row = row + vector[0]
                        else:
                            b_row = row - vector[0]

                        b_col = col + vector[1]
                        field_after_jump = self.state[b_row][b_col]
                        if field_after_jump is None:
                            available_moves_empty.append([b_row, b_col])

            except (KeyError, IndexError):
                # TODO:add something
                pass

        return available_moves_empty
