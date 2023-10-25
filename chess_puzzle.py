# implementation of the game

import random

def location2index(loc: str) -> tuple[int, int]:
    col, row = loc[0], loc[1:]
    x = (ord(col) + 1) - ord('a')
    y = int(row)
    return (x, y)
    '''converts chess location to corresponding x and y coordinates'''


def index2location(x: int, y: int) -> str:
    x, y = chr(int(x) + 96), str(y)
    col_row = x, y
    col_row_str = ''.join(col_row)
    return str(col_row_str)
    '''converts  pair of coordinates to corresponding location'''


class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B'''
    for pc in B[1]:
        if pc.pos_x == pos_X and pc.pos_y == pos_Y:
            return True
    return False


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for pc in B[1]:
        if pc.pos_x == pos_X and pc.pos_y == pos_Y:
            return pc
    return None


class Bishop(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''
        if abs(pos_X - self.pos_x) == abs(pos_Y - self.pos_y):
            x_new_dir = 0
            y_new_dir = 0
            if pos_X > self.pos_x:
                x_new_dir = 1
            else:
                x_new_dir = -1

            if pos_Y > self.pos_y:
                y_new_dir = 1
            else:
                y_new_dir = -1

            new_x, new_y = self.pos_x + x_new_dir, self.pos_y + y_new_dir
            while new_x != pos_X and new_y != pos_Y:
                if (is_piece_at(new_x, new_y, B)):
                    return False
                new_x += x_new_dir
                new_y += y_new_dir

            if piece_at(pos_X, pos_Y, B) is not None and piece_at(pos_X, pos_Y, B).side == self.side:
                return False

            return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''

        if not self.can_reach(pos_X, pos_Y, B):
            return False

        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):
            return False

        cap_pc = None

        if is_piece_at(pos_X, pos_Y, B) == True:
            cap_pc = piece_at(pos_X, pos_Y, B)

        new_B = (B[0], [])
        for pc in B[1]:
            if pc is not self and pc is not cap_pc:
                new_B[1].append(pc)
            elif pc is self:
                new_B[1].append(Bishop(pos_X, pos_Y, self.side))

        if is_check(self.side, new_B):
            return False

        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        cap_pc = None
        if is_piece_at(pos_X, pos_Y, B) == True:
            cap_pc = piece_at(pos_X, pos_Y, B)

        new_B = (B[0], [])
        for pc in B[1]:
            if pc is not self and pc is not cap_pc:
                new_B[1].append(pc)
            elif pc is self:
                new_B[1].append(Bishop(pos_X, pos_Y, self.side))

        return new_B


class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''


        if piece_at(pos_X, pos_Y, B) is not None and piece_at(pos_X, pos_Y, B).side == self.side:
            return False

        x_diff = abs(self.pos_x - pos_X)
        y_diff = abs(self.pos_y - pos_Y)

        if (x_diff == 1 and y_diff == 0) or (x_diff == 0 and y_diff == 1) or (x_diff == 1 and y_diff == 1):
            return True
        else:
            return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''

        if not self.can_reach(pos_X, pos_Y, B):
            return False

        if not (1 <= pos_X <= B[0] and 1 <= pos_Y <= B[0]):
            return False

        cap_pc = None

        if is_piece_at(pos_X, pos_Y, B) == True:
            cap_pc = piece_at(pos_X, pos_Y, B)

        new_B = (B[0], [])
        for pc in B[1]:
            if pc is not self and pc is not cap_pc:
                new_B[1].append(pc)
            elif pc is self:
                new_B[1].append(King(pos_X, pos_Y, self.side))

        if is_check(self.side, new_B):
            return False

        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        cap_pc = None

        if is_piece_at(pos_X, pos_Y, B) == True:
            cap_pc = piece_at(pos_X, pos_Y, B)

        new_B = (B[0], [])
        for pc in B[1]:
            if pc is not self and pc is not cap_pc:
                new_B[1].append(pc)
            elif pc is self:
                new_B[1].append(King(pos_X, pos_Y, self.side))

        return new_B


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
    for pc in B[1]:
        if isinstance(pc, King) and pc.side == side:
            pos_X, pos_Y = pc.pos_x, pc.pos_y
            break
    for pc2 in B[1]:
        if pc2.side != side and pc2.can_reach(pos_X, pos_Y, B):
            return True
    return False


def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints:
    - use is_check
    - use can_move_to
    '''
    if not is_check(side, B):
        return False

    for pc in B[1]:
        if pc.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if pc.can_move_to(x, y, B):
                        new_B = pc.move_to(x, y, B)
                        if not is_check(side, new_B):
                            return False
        break
    return True


def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints:
    - use is_check
    - use can_move_to
    '''
    if is_check(side, B):
        return False

    for pc in B[1]:
        if pc.side == side:
            for x in range(1, B[0] + 1):
                for y in range(1, B[0] + 1):
                    if pc.can_move_to(x, y, B):
                        new_B = pc.move_to(x, y, B)
                        if not is_check(side, new_B):
                            return False

    return True


def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
    file = open(filename, 'r')
    B_size = int(file.readline().strip())
    if B_size < 3 or B_size > 26:
        raise IOError('Board size invalid:')
    white_pc = file.readline().strip().split(",")
    if len(white_pc) <= 0:
        raise IOError('No white pieces')
    king_count = 0
    bishop_count = 0
    for pc in white_pc:
        pc = pc.strip()
        if pc[0:1] == 'K':
            king_count += 1
        elif pc[0:1] == 'B':
            bishop_count += 1

    if king_count != 1:
        raise IOError('Invalid King setup')
    if bishop_count < 1:
        raise IOError('Invalid Bishop setup')

    board_setup = []
    for pc in white_pc:
        pc = pc.strip()
        pc_type = pc[0:1]
        pc_col = pc[1:2]
        pc_row = pc[2:]
        loc_index = location2index(pc_col + pc_row)
        if pc_type.upper() == 'K':
            board_setup.append(King(loc_index[0], loc_index[1], True))
        elif pc_type.upper() == 'B':
            board_setup.append(Bishop(loc_index[0], loc_index[1], True))
        else:
            raise IOError('Invalid piece')

    black_pc = file.readline().strip().split(",")
    if len(black_pc) <= 0:
        raise IOError('No black pieces')
    king_count = 0
    bishop_count = 0
    for pc in black_pc:
        pc = pc.strip()
        if pc[0:1] == 'K':
            king_count += 1
        elif pc[0:1] == 'B':
            bishop_count += 1

    if king_count != 1:
        raise IOError('Invalid King setup')
    if bishop_count < 1:
        raise IOError('Invalid Bishop setup')

    for pc in black_pc:
        pc = pc.strip()
        pc_type = pc[0:1]
        pc_col = pc[1:2]
        pc_row = pc[2:]
        loc_index = location2index(pc_col + pc_row)
        if pc_type.upper() == 'K':
            board_setup.append(King(loc_index[0], loc_index[1], False))
        elif pc_type.upper() == 'B':
            board_setup.append(Bishop(loc_index[0], loc_index[1], False))
        else:
            raise IOError('Invalid piece')

    file.close()
    return B_size, board_setup


def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    file = open(filename, 'w')
    file.write(str(B[0]) + '\n')
    for pc in B[1]:
        if isinstance(pc, King) and pc.side == True:
            loc = index2location(pc.pos_x, pc.pos_y)
            file.write('K' + loc + ',')
        elif isinstance(pc, Bishop) and pc.side == True:
            loc = index2location(pc.pos_x, pc.pos_y)
            file.write('B' + loc + ',')
    file.write('\n')
    for pc in B[1]:
        if isinstance(pc, King) and pc.side == False:
            loc = index2location(pc.pos_x, pc.pos_y)
            file.write('K' + loc + ',')
        elif isinstance(pc, Bishop) and pc.side == False:
            loc = index2location(pc.pos_x, pc.pos_y)
            file.write('B' + loc + ',')
    file.write('\n')
    file.close()


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere

    Hints:
    - use methods of random library
    - use can_move_to
    '''
    black_pc = []
    for pc in B[1]:
        if pc.side == False:
            black_pc.append(pc)
    random.shuffle(black_pc)

    for pc in black_pc:
        black_moves = []
        for x in range(1, B[0] + 1):
            for y in range(1, B[0] + 1):
                black_moves.append((x, y))
    random.shuffle(black_moves)

    for m in black_moves:
        if pc.can_move_to(m[0], m[1], B):
            return (pc, m[0], m[1])

    raise ValueError('No moves available for black pieces.')


def conf2unicode(B: Board) -> str:
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
    unicode_board = [['\u2001' for i in range(B[0])] for j in range(B[0])]
    for pc in B[1]:
        if isinstance(pc, King):
            if pc.side == True:
                unicode_board[abs(pc.pos_y - B[0])][pc.pos_x - 1] = '♔'
            else:
                unicode_board[abs(pc.pos_y - B[0])][pc.pos_x - 1] = '♚'
        if isinstance(pc, Bishop):
            if pc.side == True:
                unicode_board[abs(pc.pos_y - B[0])][pc.pos_x - 1] = '♗'
            else:
                unicode_board[abs(pc.pos_y - B[0])][pc.pos_x - 1] = '♝'

    s = ''
    for row in unicode_board:
        s += ''.join(row) + '\n'

    return s


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    filename = input("File name for initial configuration: ")
    B = None
    side_move = 0
    while True:
        try:
            B = read_board(filename)
            uni_board = conf2unicode(B)
            print("The initial configuration is: \n" + uni_board)
            break
        except FileNotFoundError:
            filename = input("This is not a valid file. File name for initial configuration: ")
        except IOError:
            filename = input("This is not a valid file. File name for initial configuration: ")

    while True:
        if side_move % 2 == 0:
            new_white_move = input("Next move of White: ")
            if new_white_move.lower() == "quit" and B is None:
                print("Terminated")
                quit()
            elif new_white_move.lower() == "quit" and B is not None:
                save_new_board = input("File name to store the configuration: ")
                save_board(save_new_board, B)
                print("The game configuration saved. ")
                quit()

            if len(new_white_move) < 4 or len(new_white_move) > 6:
                print("This is not a valid move.")
                continue

            initial_move = check_user_move(new_white_move)[0]
            initial_move_index = location2index(initial_move)
            dest_move = check_user_move(new_white_move)[1]
            dest_move_index = location2index(dest_move)
            if not is_piece_at(initial_move_index[0], initial_move_index[1], B):
                print("No piece found at the given location")
                continue
            pc = piece_at(initial_move_index[0], initial_move_index[1], B)
            if not pc.side:
                print("Piece at the given location is not white")
                continue
            if not pc.can_move_to(dest_move_index[0], dest_move_index[1], B):
                print("This is not a valid move.")
                continue
            B = pc.move_to(dest_move_index[0], dest_move_index[1], B)
            print(conf2unicode(B))
            if is_checkmate(True, B):
                print("Game over. White wins. ")
                exit()
            elif is_stalemate(True, B):
                print("Game over. Stalemate.")
                exit()
            side_move += 1

        else:
            new_black_move = find_black_move(B)
            B = new_black_move[0].move_to(new_black_move[1], new_black_move[2], B)
            print("Next move of Black is " + index2location(new_black_move[0].pos_x, new_black_move[0].pos_y) + index2location(
                new_black_move[1], new_black_move[2]) + ". The configuration after Black's move is: ")
            print(conf2unicode(B))
            if is_checkmate(False, B):
                print("Game over. Black wins. ")
                exit()
            elif is_stalemate(False, B):
                print("Game over. Stalemate.")
                exit()
            side_move += 1
            continue


def check_user_move(user_move: str) -> tuple[str, str]:
    if user_move[2].isdigit():
        initial_move = user_move[0:3]
        dest_move = user_move[3:]
        return initial_move, dest_move
    else:
        initial_move = user_move[0:2]
        dest_move = user_move[2:]
        return initial_move, dest_move


if __name__ == '__main__':  # keep this in
    main()