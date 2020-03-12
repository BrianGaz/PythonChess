import sys
import copy
from itertools import cycle
#import chessgui
import os
#import pygame
#import flaskchess

a = ["wR", "wp", 0, 0, 0, 0, "bp", "bR"]
b = ["wN", "wp", 0, 0, 0, 0, "bp", "bN"]
c = ["wB", "wp", 0, 0, 0, 0, "bp", "bB"]
d = ["wQ", "wp", 0, 0, 0, 0, "bp", "bQ"]
e = ["wK", "wp", 0, 0, 0, 0, "bp", "bK"]
f = ["wB", "wp", 0, 0, 0, 0, "bp", "bB"]
g = ["wN", "wp", 0, 0, 0, 0, "bp", "bN"]
h = ["wR", "wp", 0, 0, 0, 0, "bp", "bR"]


SELECTED_PIECE = ""

files = [a, b, c, d, e, f, g, h]
files_str = ["a", "b", "c", "d", "e", "f", "g", "h"]
files_dict = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h}


def pawn_upgrade():
    teams = ["wp", "bp"]
    for team in teams:
        p_loc = search_board(team)
        for line in p_loc:
            for p in line:
                # print (p)
                upgrade = ""
                # print (check_square(p)[0])
                # print (p[1])
                if check_square(p)[0] == "w" and p[1] == "8":
                    while upgrade not in ["Q", "R", "B", "N"]:
                        upgrade = input("Choose which piece to upgrade your pawn to: Q,R,B,N\n")
                elif check_square(p)[0] == "b" and p[1] == "1":
                    # print("@")
                    while upgrade not in ["Q", "R", "B", "N"]:
                        upgrade = input("Choose which piece to upgrade your pawn to: Q,R,B,N\n")
                if upgrade != "":
                    files_dict[p[0]][int(p[1]) - 1] = check_square(p)[0] + upgrade
                    print("pawn upgraded")


def check_square(square):
    # print (square)
    col = square[0]
    row = int(square[1]) - 1
    # print (files_dict)
    return files_dict[col][row]


def check_line(line, piece):
    file_str = files_str[files.index(line)]
    # print(file_str)
    piece_index = []
    if piece not in line:
        return piece_index
    else:
        counter = 0
        while counter < len(line):
            if line[counter] == piece:
                piece_index.append(file_str + str(counter + 1))
            counter += 1
        return piece_index


def check_line_by_str(file_str, piece):
    line = files_dict[file_str]
    piece_index = []
    if piece not in line:
        return piece_index
    else:
        counter = 0
        while counter < len(line):
            if line[counter] == piece:
                piece_index.append(file_str + str(counter + 1))
            counter += 1
        return piece_index


def search_board(piece):
    coords = []
    for file_str in files_str:
        # print(line)
        # print(check_line(line,piece))
        coords.append(check_line_by_str(file_str, piece))
    '''
    for line in files:
      #print(line)
      #print(check_line(line,piece))
      coords.append(check_line(line, piece))
    '''
    return coords


def check_inbounds(square, possible_moves):
    new_moves = []
    for move in possible_moves:
        file_index = files_str.index(square[0]) + move[0]
        if -1 < file_index < 8:
            rank_index = int(square[1]) + move[1] - 1
            if -1 < rank_index < 8:
                new_moves.append(move)
    return new_moves


def move_to_coord(square, moves):
    conversion = []
    file = square[0]
    file_index = files_str.index(file)
    rank = square[1]
    # print (square)
    # print (moves)
    for move in moves:
        conversion.append(files_str[file_index + move[0]] + str(int(rank) + move[1]))
    return conversion


def K_moves(square):
    """
    K_moves = [(0,1),(1,1),(1,0),(0,-1),(-1,-1),(-1,0),(1,-1),(-1,1)]
    K_moves = check_inbounds(square,K_moves)
    K_moves = check_allies(square,K_moves)
    """
    K_moves = move_options(square)
    K_coords = move_to_coord(square, K_moves)
    team = check_square(square)[0]
    K_moves_remove = []
    for new_move in K_moves:
        temp_board = copy.deepcopy(files)
        # print (temp_board)
        # print (files)
        # move(square, new_move)
        # print (moves)
        # print(piece)
        piece = check_square(square)
        new_loc = move_to_coord(square, [new_move])
        # print (new_loc)
        new_loc = new_loc[0]
        # print (new_loc)
        file = files_dict[new_loc[0]]
        file_index = files_str.index(new_loc[0])
        rank = int(new_loc[1]) - 1

        file[rank] = piece

        file = files_dict[square[0]]
        file_index = files_str.index(square[0])
        rank = int(square[1]) - 1
        file[rank] = 0
        piece = check_square(square)

        # print (files)
        K_coord = move_to_coord(square, [new_move])
        # print (new_move)
        # print (K_coord)
        try:
            cc_tf, cc_loc = check_check(K_coord[0])
            if cc_tf == True:
                # print (K_coords)
                remove_index = K_coords.index(K_coord[0])
                # print (remove_index)
                # print (K_moves)
                K_moves_remove.append(K_moves[remove_index])
                # print (K_moves[remove_index])
                # K_coords.remove(K_coord[0])
            # print (files)
            reset_board(temp_board)
        except:
            reset_board(temp_board)
    for remove in K_moves_remove:
        K_moves.remove(remove)
    return K_moves


def reset_board(temp_board):
    global a, b, c, d, e, f, g, h, files, files_dict
    a = temp_board[0]
    b = temp_board[1]
    c = temp_board[2]
    d = temp_board[3]
    e = temp_board[4]
    f = temp_board[5]
    g = temp_board[6]
    h = temp_board[7]
    files = [a, b, c, d, e, f, g, h]
    files_dict = {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h}


def check_allies(square, possible_moves):
    new_moves = []
    for move in possible_moves:
        file_index = files_str.index(square[0]) + move[0]
        rank_index = (files[file_index])[int(square[1]) + move[1] - 1]
        if rank_index == 0:
            new_moves.append(move)
        elif check_square(square)[0] != rank_index[0]:
            if check_square(square)[1] == "p" and move[0] == 0:
                break
            new_moves.append(move)
            if check_square(square)[1] != "N" and check_square(square)[1] != "p":
                if check_square(square)[1] != "K":
                    break
        elif rank_index[0] == check_square(square)[0] and check_square(square)[1] != "N":
            if check_square(square)[1] != "K":
                break
    return new_moves


def ally_check_break(square, ):
    team = check_square(square)[0]
    w_pieces = ["wK", "wQ", "wB", "wN", "wR", "wp"]
    b_pieces = ["bK", "bQ", "bB", "bN", "bR", "bp"]
    if team == "w":
        team = w_pieces
    else:
        team = b_pieces
    checker_pos = check_check(square)[1]
    # print('checker_pos ' + str(checker_pos))
    options = []
    coords = []
    distance = 0
    if checker_pos[0] == square[0]:  # if checker in same file
        distance = int(checker_pos[1]) - int(square[1])
        if distance > 0:
            while distance > 0:
                coords.append((0, distance))
                distance -= 1
        else:
            while distance < 0:
                coords.append((0, distance))
                distance += 1
    elif checker_pos[1] == square[1]:  # if checker in same rank
        distance = files_str.index(checker_pos[0]) - files_str.index(square[0])
        # print (distance)
        if distance > 1:
            while distance > 1:
                coords.append((distance, 0))
                distance -= 1
        else:
            while distance < -1:
                coords.append((distance, 0))
                distance += 1

    else:  # diagonal check
        file_distance = int(square[1]) - int(checker_pos[1])
        rank_distance = files_str.index(square[0]) - files_str.index(checker_pos[0])
        if file_distance > 1 and rank_distance > 1:
            while file_distance > 0 and rank_distance > 0:
                coords.append((file_distance, rank_distance))
                file_distance -= 1
                rank_distance -= 1
        elif file_distance < -1 and rank_distance < -1:
            while file_distance < 0 and rank_distance < 0:
                coords.append((file_distance, rank_distance))
                file_distance += 1
                rank_distance += 1
        elif file_distance > 1 and rank_distance < -1:
            while file_distance > 0 and rank_distance < 0:
                coords.append((file_distance, rank_distance))
                file_distance -= 1
                rank_distance += 1
        elif file_distance > -1 and rank_distance < 1:
            while file_distance < 0 and rank_distance > 0:
                coords.append((file_distance, rank_distance))
                file_distance += 1
                rank_distance -= 1

    check_los = move_to_coord(square, coords)
    for ally_piece in team:
        for ally_loc_list in search_board(ally_piece):
            for ally in ally_loc_list:
                moves = move_options(ally)
                for moves_moves in moves:
                    try:
                        ally_move_coords = move_to_coord(ally, moves_moves)
                    except:
                        ally_move_coords = move_to_coord(ally, moves)
                    for coord in ally_move_coords:
                        if coord in check_los:
                            if ally_piece[1] != "K":
                                piece = check_square(ally)[1]
                                if piece == "p":
                                    if ally[0] == coord[0]:
                                        options.append(coord)
                                        break
                                    else:
                                        options.append(ally[0] + coord)
                                        break
                                options.append(piece + coord)

    for option in options:  # checks that a piece is not already protecting the king
        temp_board = copy.deepcopy(files)
        notation_move(check_square(square)[0], option, [])
        if check_check(square) != ():
            options.remove(option)
        reset_board(temp_board)

    return options


def check_check(square):
    value = ()
    w_pieces = ["wK", "wQ", "wB", "wN", "wR", "wp"]
    b_pieces = ["bK", "bQ", "bB", "bN", "bR", "bp"]

    if check_square(square) == 0:
        if square[1] == "1":
            enemies = b_pieces
        if square[1] == "8":
            enemies = w_pieces
    elif check_square(square)[0] == "w":
        enemies = b_pieces
    else:
        enemies = w_pieces

    for enemy in enemies:
        for enemy_loc_list in search_board(enemy):
            for enemy_loc in enemy_loc_list:
                for moves in move_options(enemy_loc):
                    if enemy[1] == "K":
                        moves = move_options(enemy_loc)
                    coords = move_to_coord(enemy_loc, moves)
                    for coord in coords:
                        if coord == square:
                            value = (True, enemy_loc)
    return value


def move_options(square):
    # print (square)
    # print (files)
    # print (e)
    # print (check_square(square))
    piece = check_square(square)[1]
    team = check_square(square)[0]
    if piece == "K":
        moves = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        moves = check_inbounds(square, moves)
        moves = check_allies(square, moves)

        return moves
    if piece == "p":
        if team == "w":
            moves = [(0, 1)]
            if square[1] == "2":
                moves.append((0, 2))
            moves = check_inbounds(square, moves)
            moves = check_allies(square, moves)
            p_take = [(1, 1), (-1, 1)]
            p_take = check_inbounds(square, p_take)
            for move in p_take:
                if p_take == []:
                    break
                file_index = files_str.index(square[0]) + move[0]
                rank_index = (files[file_index])[int(square[1]) + move[1] - 1]
                if rank_index == 0:
                    pass
                elif rank_index[0] == "b":
                    moves.append(move)
        else:
            moves = [(0, -1)]
            if square[1] == "7":
                moves.append((0, -2))
            moves = check_inbounds(square, moves)
            moves = check_allies(square, moves)
            p_take = [(1, -1), (-1, -1)]
            p_take = check_inbounds(square, p_take)
            for move in p_take:
                if p_take == []:
                    break
                file_index = files_str.index(square[0]) + move[0]
                rank_index = (files[file_index])[int(square[1]) + move[1] - 1]
                if rank_index == 0:
                    pass
                elif rank_index[0] == "w":
                    moves.append(move)
        return [moves]

    if piece == "Q":
        pos_pos_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        pos_neg_moves = [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)]
        neg_pos_moves = [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
        neg_neg_moves = [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]
        pos_file_moves = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        neg_file_moves = [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
        pos_rank_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        neg_rank_moves = [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]

        all_moves = [pos_pos_moves, pos_neg_moves, neg_pos_moves, neg_neg_moves, pos_file_moves, neg_file_moves,
                     pos_rank_moves, neg_rank_moves]

        all_moves = [check_inbounds(square, moves) for moves in all_moves]
        all_moves = [check_allies(square, moves) for moves in all_moves]

        return all_moves
    if check_square(square)[1] == "B":
        pos_pos_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
        pos_neg_moves = [(1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7)]
        neg_pos_moves = [(-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
        neg_neg_moves = [(-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7)]

        all_moves = [pos_pos_moves, pos_neg_moves, neg_pos_moves, neg_neg_moves]
        # print(all_moves)

        all_moves = [check_inbounds(square, moves) for moves in all_moves]
        # print(all_moves)

        all_moves = [check_allies(square, moves) for moves in all_moves]
        return all_moves

    if check_square(square)[1] == "R":
        pos_file_moves = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]
        neg_file_moves = [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
        pos_rank_moves = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        neg_rank_moves = [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0)]

        all_moves = [pos_file_moves, neg_file_moves, pos_rank_moves, neg_rank_moves]
        all_moves = [check_inbounds(square, moves) for moves in all_moves]
        all_moves = [check_allies(square, moves) for moves in all_moves]

        return all_moves

    if check_square(square)[1] == "N":
        new_moves = []
        possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        possible_moves = check_inbounds(square, possible_moves)
        # if square has ally on it, move not possible
        for move in possible_moves:
            file_index = files_str.index(square[0]) + move[0]
            rank = files[file_index]
            rank_index = int(square[1]) + move[1] - 1
            if rank[rank_index] == 0:
                new_moves.append(move)
            elif (rank[rank_index])[0] != check_square(square)[0]:
                new_moves.append(move)
        possible_moves = check_allies(square, possible_moves)
        return [possible_moves]


def check_mate(king_loc):
    if check_check(king_loc) != ():
        if ally_check_break(king_loc) == []:
            if K_moves(king_loc) == []:
                print(check_check(king_loc))
                print(ally_check_break(king_loc))
                print(K_moves(king_loc))
                if check_square(king_loc)[0] == "w":
                    print("Checkmate! Black wins")
                    return True
                elif check_square(king_loc)[0] == "b":
                    print("Checkmate! White wins")
                    return True


def notation_move(team, notation, castle_info):
    if notation in ["OO", "OOO"]:  # castling
        print(castle_info)
        if notation == "OOO" and notation in castle_options(team, castle_info):
            if team == "w":
                files[2][0] = "wK"
                files[3][0] = "wR"
                files[0][0] = 0
                files[4][0] = 0
            else:
                files[2][7] = "bK"
                files[3][7] = "bR"
                files[0][7] = 0
                files[4][7] = 0
        elif notation == "OO" and notation in castle_options(team, castle_info):
            if team == "w":
                files[6][0] = "wK"
                files[5][0] = "wR"
                files[7][0] = 0
                files[4][0] = 0
            else:
                files[6][7] = "bK"
                files[5][7] = "bR"
                files[7][7] = 0
                files[4][7] = 0
    elif len(notation) == 2:  # the piece will be a pawn
        # line = files_dict[notation[0]]
        # print(line)
        pawns_inline = check_line_by_str(notation[0], team + "p")
        # print(pawns_inline)
        if len(pawns_inline) == 1:
            piece_loc = pawns_inline[0]
        else:  # Multiple pawns (same team) in  one line
            if team == "w":
                if notation[1] < pawns_inline[1][1]:
                    piece_loc = pawns_inline[0]
                elif notation[1] > pawns_inline[-1][1]:
                    piece_loc = pawns_inline[-1]
                else:
                    piece_loc = pawns_inline[1]
            else:
                if notation[1] > pawns_inline[1][1]:
                    piece_loc = pawns_inline[-1]
                elif notation[1] < pawns_inline[0][1]:
                    piece_loc = pawns_inline[0]
                else:
                    piece_loc = pawns_inline[1]

        move_distance = int(notation[1]) - int(piece_loc[1])

        if 2 < move_distance or move_distance < -2 or move_distance == 0:
            raise
        if team == "w" and move_distance < 0:
            raise
        if team == "b" and move_distance > 0:
            raise

        move_coord = (0, move_distance)
        # print(piece_loc)
        move(piece_loc, move_coord)

    elif len(notation) == 3:
        line = files_dict[notation[1]]

        if notation[0] in files_str:  # pawn trying to capture
            piece_char = "p"
        else:
            piece_char = notation[0]
        piece = team + piece_char

        if piece_char == "p":
            all_piece_coords = [check_line(files_dict[notation[0]], piece)]
        else:
            all_piece_coords = search_board(piece)

        pieces_to_move = []
        move_coords = []
        ep = None

        for piece_coords in all_piece_coords:
            if piece_coords != []:
                for piece_coord in piece_coords:
                    if piece_char == "K":
                        moves_list = [K_moves(piece_coord)]
                    else:
                        moves_list = move_options(piece_coord)
                        if piece_char == "p":
                            for ep in en_passant(team, castle_info):
                                if piece_coord == ep[0]:
                                    moves_list[0].append(ep[1])
                                    ep = True
                    for moves in moves_list:
                        move_squares = move_to_coord(piece_coord, moves)
                        for amove in move_squares:
                            if notation[1:] == amove:
                                if piece_coord not in pieces_to_move:
                                    pieces_to_move.append(piece_coord)
                                coord_index = move_squares.index(amove)
                                move_coords.append(moves[coord_index])
        if len(pieces_to_move) > 1:  # More than 1 possible piece to move
            # print(pieces_to_move)
            print("Please specify which " + notation[0] + " you'd like to move")
        else:
            move(pieces_to_move[0], move_coords[0], ep)
            if ep == True:  # make en passant actually take the peice
                if team == "w":
                    files_dict[notation[1]][int(notation[2]) - 2] = 0
                else:
                    files_dict[notation[1]][int(notation[2])] = 0

    elif len(notation) == 5:
        piece_coord = notation[1:3]
        desired_move = notation[3:]
        moves = move_options(piece_coord)
        moves_list = []
        moves_squares = []
        for options in moves:
            if options != []:
                if notation[0] == "R":
                    moves_squares.extend(move_to_coord(piece_coord, options))
                    moves_list.extend(options)
                else:
                    moves_squares.append(move_to_coord(piece_coord, options))
                    moves_list.append(options)

        if notation[0] == "R":
            pass
        else:
            moves_squares = moves_squares[0]

        if desired_move in moves_squares:
            move_index = moves_squares.index(desired_move)
            if notation[0] == "R":
                coord_move = moves_list[move_index]
            else:
                coord_move = moves_list[0][move_index]
            move(piece_coord, coord_move)


def move(square, move, ep=None):
    # print (square)
    piece = check_square(square)
    moves = move_options(square)
    # print (moves)
    # print(piece)
    if piece[1] == "Q":
        moves = moves[0] + moves[1] + moves[2] + moves[3] + moves[4] + moves[5] + moves[6] + moves[7]
    elif piece[1] == "p" or piece[1] == "N":
        moves = moves[0]
        if piece[1] == "p":
            if ep != None:
                moves.append(move)
    elif piece[1] == "R" or piece[1] == "B":
        moves = moves[0] + moves[1] + moves[2] + moves[3]
        # print(moves)
    elif piece[1] == "K":
        moves = K_moves(square)
    if move in moves:
        new_loc = move_to_coord(square, [move])
        # print (new_loc)
        new_loc = new_loc[0]
        # print (new_loc)
        file = files_dict[new_loc[0]]
        file_index = files_str.index(new_loc[0])
        rank = int(new_loc[1]) - 1

        file[rank] = piece

        file = files_dict[square[0]]
        file_index = files_str.index(square[0])
        rank = int(square[1]) - 1
        file[rank] = 0
    else:
        raise

SELECTED_SQUARE = ''

def gui(team):
    click2 = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for square in chessgui.square_list:
                    if pygame.mouse.get_pos()[0] in list(range(square[0], square[0] + 80)) \
                            and pygame.mouse.get_pos()[1] in list(range(square[1], square[1] + 80)):
                        for keyvalue in chessgui.square_dict:
                            if chessgui.square_dict[keyvalue] == square:
                                global SELECTED_PIECE
                                global SELECTED_SQUARE
                                if SELECTED_PIECE is "":
                                    SELECTED_PIECE = check_square(keyvalue)[1]
                                else:
                                    if check_square(keyvalue) == 0 or check_square(keyvalue)[0] != team:
                                        click2 = keyvalue
                                    else:
                                        SELECTED_PIECE = check_square(keyvalue)[1]
                                        SELECTED_SQUARE = keyvalue
                                if click2 is not "":
                                    if SELECTED_PIECE == "p":
                                        if SELECTED_SQUARE[0] == click2[0]:
                                            return click2
                                        else:
                                            return SELECTED_SQUARE[0] + click2
                                    else:
                                        return SELECTED_PIECE + click2

def update_screen():

        for file_index, line in enumerate(files):
            for square_index, square in enumerate(line, 1):
                line_str = files_str[file_index]
                square = line_str + str(square_index)
                square_contents = check_square(square)
                gui_sq = chessgui.square_dict[square]
                if square_contents != 0:
                    img = pygame.image.load(os.path.join('ChessSprites', square_contents + '.png')).convert_alpha()
                    img = pygame.transform.scale(img, (80, 80))
                    pygame.draw.rect(chessgui.ayy,
                                     tuple(pygame.Surface.get_at(chessgui.ayy, (gui_sq[0], gui_sq[1]))),
                                     chessgui.square_dict[square])
                    chessgui.ayy.blit(img, gui_sq)
                else:
                    pygame.draw.rect(chessgui.ayy,
                                     tuple(pygame.Surface.get_at(chessgui.ayy, (gui_sq[0], gui_sq[1]))),
                                     chessgui.square_dict[square])


        chessgui.pygame.display.update()


def gui_play():
    teams = ["w", "b"]
    castle_info = []


    update_screen()

    while True:
        for team in teams:
            if team == "w":
                opp_team = "b"
            else:
                opp_team = "w"

            team_king_loc = ""
            for line in search_board(team + "K"):
                if line != []:
                    team_king_loc = line[0]

            check_status = None
            if check_check(team_king_loc) != ():
                check_status = True

            #print(gui(team))

            try:
                if team == "w":

                    amove = gui(team)
                    #print(amove)
                    #amove = input("White's move:")
                    notation_move('w', amove, castle_info)
                    update_screen()
                else:
                    amove = gui(team)
                    #amove = input("Black's move:")
                    notation_move("b", amove, castle_info)
                    update_screen()
                if check_status == True:
                    team_king_loc = ""
                    for line in search_board(team + "K"):
                        if line != []:
                            team_king_loc = line[0]
                    if check_check(team_king_loc) != ():
                        raise
            except:
                print("Please choose a valid move.")
                if team == "w":
                    teams = ["w"]
                if team == "b":
                    teams = ["b"]
                break

            pawn_upgrade()


            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            if amove[0] in ["K", "R"]:  # for castling
                if amove[0] == "R":
                    castle_info.append((team, amove))
                else:
                    castle_info.append((team, amove[0]))

            if team == "w" and amove[1] == "4":
                castle_info.append((team, amove))
            elif team == "b" and amove[1] == "5":
                castle_info.append((team, amove))

            print()
            [print(line) for line in files]
            #yield files

            king_loc = ""
            for line in search_board(opp_team + "K"):
                if line != []:
                    king_loc = line[0]
            if check_check(king_loc) != ():
                if check_mate(king_loc) == True:
                    sys.exit()
                else:
                    if team == "w":
                        print("White king in check!")
                    else:
                        print("Black king in check!")

        else:
            if team == "w":
                teams = ["b", "w"]
            else:
                teams = ["w", "b"]



def play():
    teams = ["w", "b"]
    castle_info = []
    while True:
        for team in teams:

            if team == "w":
                opp_team = "b"
            else:
                opp_team = "w"

            team_king_loc = ""
            for line in search_board(team + "K"):
                if line != []:
                    team_king_loc = line[0]

            check_status = None
            if check_check(team_king_loc) != ():
                check_status = True

            try:
                if team == "w":
                    amove = input("White's move:")
                    notation_move('w', amove, castle_info)
                else:
                    amove = input("Black's move:")
                    notation_move("b", amove, castle_info)
                if check_status == True:
                    team_king_loc = ""
                    for line in search_board(team + "K"):
                        if line != []:
                            team_king_loc = line[0]
                    if check_check(team_king_loc) != ():
                        raise
            except:
                print("Please choose a valid move.")
                if team == "w":
                    teams = ["w"]
                if team == "b":
                    teams = ["b"]
                break

            pawn_upgrade()

            if amove[0] in ["K", "R"]:  # for castling
                if amove[0] == "R":
                    castle_info.append((team, amove))
                else:
                    castle_info.append((team, amove[0]))

            if team == "w" and amove[1] == "4":
                castle_info.append((team, amove))
            elif team == "b" and amove[1] == "5":
                castle_info.append((team, amove))

            print()
            [print(line) for line in files]

            king_loc = ""
            for line in search_board(opp_team + "K"):
                if line != []:
                    king_loc = line[0]
            if check_check(king_loc) != ():
                if check_mate(king_loc) == True:
                    sys.exit()
                else:
                    if team == "w":
                        print("White king in check!")
                    else:
                        print("Black king in check!")

        else:
            if team == "w":
                teams = ["b", "w"]
            else:
                teams = ["w", "b"]

def en_passant(team, castle_info):
    if team == "w":
        opp_team = "b"
    else:
        opp_team = "w"

    coords = []

    if team == "w":
        eligible = []
        for line in search_board(team + "p"):
            for piece in line:
                # print(piece)
                if piece[1] == "5":  # <--- only for white
                    eligible.append(piece)
        # print(eligible)
        for piece in eligible:
            file_index = files_str.index(piece[0])
            below_file = ""
            above_file = ""
            if file_index == 7:
                below_file = files_str[file_index - 1]
            elif file_index == 0:
                above_file = files_str[file_index + 1]
            else:
                above_file = files_str[file_index + 1]
                below_file = files_str[file_index - 1]
            above_p_jump = ("b", above_file + "5")
            below_p_jump = ("b", below_file + "5")
            pos_prev_above_move = ("b", above_file + "6")
            pos_prev_below_move = ("b", below_file + "6")

            poss_ep = []
            for p_jump in [above_p_jump, below_p_jump]:
                if castle_info == []:
                    break
                elif p_jump == castle_info[-1]:
                    poss_ep.append(p_jump[1][0] + str(int(p_jump[1][1]) + 1))

            for pos_prev_move in [pos_prev_above_move, pos_prev_below_move]:
                if pos_prev_move in castle_info:
                    if pos_prev_move[1] in poss_ep:
                        poss_ep.remove(pos_prev_move[1])

            for ep in poss_ep:
                checker_pos = ep
                square = piece
                rank_distance = int(checker_pos[1]) - int(square[1])
                file_distance = files_str.index(checker_pos[0]) - files_str.index(square[0])
                coords.append((piece, (file_distance, rank_distance)))
    else:
        eligible = []
        for line in search_board(team + "p"):
            for piece in line:
                if piece[1] == "4":
                    eligible.append(piece)
        for piece in eligible:
            file_index = files_str.index(piece[0])
            if file_index == 7:
                below_file = files_str[file_index - 1]
                below_p_jump = ("w", below_file + "4")
                p_jumps = [below_p_jump]
                pos_prev_below_move = ("w", below_file + "2")
                pos_prev_moves = [pos_prev_below_move]
            elif file_index == 0:
                above_file = files_str[file_index + 1]
                above_p_jump = ("w", above_file + "4")
                p_jumps = [above_p_jump]
                pos_prev_above_move = ("w", above_file + "2")
                pos_prev_moves = [pos_prev_above_move]
            else:
                above_file = files_str[file_index + 1]
                below_file = files_str[file_index - 1]
                above_p_jump = ("w", above_file + "4")
                below_p_jump = ("w", below_file + "4")
                p_jumps = [above_p_jump, below_p_jump]
                pos_prev_above_move = ("w", above_file + "2")
                pos_prev_below_move = ("w", below_file + "2")
                pos_prev_moves = [pos_prev_above_move, pos_prev_below_move]

            poss_ep = []
            for p_jump in p_jumps:
                if p_jump == castle_info[-1]:
                    poss_ep.append(p_jump[1][0] + str(int(p_jump[1][1]) - 1))

            for pos_prev_move in pos_prev_moves:
                if pos_prev_move in castle_info:
                    if pos_prev_move[1] in poss_ep:
                        poss_ep.remove(pos_prev_move[1])

            for ep in poss_ep:
                checker_pos = ep
                square = piece
                rank_distance = int(checker_pos[1]) - int(square[1])
                file_distance = files_str.index(checker_pos[0]) - files_str.index(square[0])
                coords.append((piece, (file_distance, rank_distance)))

    return coords


def castle_options(team, castle_info):
    if team == "w":
        long_castle_check_allies = ["b1", "c1", "d1"]
        long_castle_check_enemy = ["c1", "d1"]
        short_castle = ["f1", "g1"]

    else:
        long_castle_check_allies = ["b8", "c8", "d8"]
        long_castle_check_enemy = ["c8", "d8"]
        short_castle = ["f8", "g8"]

    top_rook_moves = ["Ra1", "Ra2", "Ra3", "Ra4", "Ra5", "Ra6", "Ra7", "Ra8", "Rb1", "Rc1", "Rd1", "Rb8", "Rc8", "Rd8"]
    bot_rook_moves = ["Rh1", "Rh2", "Rh3", "Rh4", "Rh5", "Rh6", "Rh7", "Rh8", "Rg1", "Rf1", "Rg8", "Rf8"]

    castle_opt = ["OOO", "OO"]

    if castle_info != []:
        for rook_move in castle_info:
            if rook_move[1] in top_rook_moves:
                castle_opt.remove("OOO")
            if rook_move[1] in bot_rook_moves:
                castle_opt.remove("OO")

    # check that long castle is not blocked by ally
    for square in long_castle_check_allies:
        if check_square(square) != 0:
            if "OOO" in castle_opt:
                castle_opt.remove("OOO")

    # check that long castle isnt blocked by enemy
    for square in long_castle_check_enemy:
        if check_check(square) != ():
            if "OOO" in castle_opt:
                castle_opt.remove("OOO")

    # check that short castle is not blocked by ally
    for square in short_castle:
        if check_square(square) != 0:
            if "OO" in castle_opt:
                castle_opt.remove("OO")
        # check that short castle isnt blocked by enemy
        else:
            if check_check(square) != ():
                if "OO" in castle_opt:
                    castle_opt.remove("OO")

    if castle_opt != []:  # castles available
        # king hasn't been moved
        if (team, "K") not in castle_info:
            return castle_opt

def convert_notation(raw_notation):
    new_notation = raw_notation.replace("x", "")
    new_notation = new_notation.replace("+", "")
    new_notation = new_notation.replace("-", "")

    new_notation = new_notation.split(" ")
    for notation in new_notation:
        if notation[0] in str(list(range(0, 10))):
            new_notation.remove(notation)

    for index, notation in enumerate(new_notation):
        if len(notation) == 4:
            remove_letter = notation[1]
            notation = notation.replace(remove_letter, "")
            new_notation[index] = notation

    return new_notation

def htmlplay(board, team, move):
    castle_info = []

    if team == "w":
        opp_team = "b"
    else:
        opp_team = "w"

    team_king_loc = ""
    for line in search_board(team + "K"):
        if line != []:
            team_king_loc = line[0]

    check_status = None
    if check_check(team_king_loc) != ():
        check_status = True

    try:
        if team == "w":
            amove = move
            notation_move('w', amove, castle_info)
        else:
            amove = move
            notation_move("b", amove, castle_info)
        if check_status == True:
            team_king_loc = ""
            for line in search_board(team + "K"):
                 if line != []:
                    team_king_loc = line[0]
            if check_check(team_king_loc) != ():
                raise
    except:
        print("Please choose a valid move.")
        if team == "w":
            teams = ["w"]
        if team == "b":
            teams = ["b"]

    pawn_upgrade()

    if amove[0] in ["K", "R"]:  # for castling
        if amove[0] == "R":
            castle_info.append((team, amove))
        else:
            castle_info.append((team, amove[0]))

    if team == "w" and amove[1] == "4":
        castle_info.append((team, amove))
    elif team == "b" and amove[1] == "5":
        castle_info.append((team, amove))

        #print()
        #[print(line) for line in files]

    king_loc = ""
    for line in search_board(opp_team + "K"):
        if line != []:
            king_loc = line[0]
    if check_check(king_loc) != ():
        if check_mate(king_loc) == True:
            sys.exit()
        else:
            if team == "w":
                print("White king in check!")
            else:
                print("Black king in check!")

def atest():
    return files



#play()

'''
moves = convert_notation("1. e4 c5 2. Nc3 Nc6 3. d3 d6 4. g3 g6 5. Bg2 Bg7 6. Ng1e2 e5 7. O-O Ng8e7 8. f4 f5 9. Nd5 O-O 10. Ne2c3 Nxd5 11. Nxd5 Be6 12. exf5 Bxf5 13. c3 Qd7 14. Be3 Ra8e8 15. Qb3 Kh8 16. Ra1d1 b5 17. Be4 Bxe4 18. dxe4 exf4 19. Bxf4 Rxe4 20. Qxb5 Rfe8 21. Rd2 h6 22. Rd2f2 Re1 23. Kg2 Rxf1 24. Rxf1 Rb8 25. Qe2 Qb7 26. b3 Nd4 27. Qe4 Nf5 28. Bd2 Ne7 29. c4 Nf5 30. g4 Nh4+ 31. Kg3 g5 32. Qe6 Qc6 33. Re1 Rf8 34. h3 Rf3+ 35. Kh2 Rf2+ 36. Kh1 Rxd2 37. Qf7 Kh7 38. Re7 Rd1+ 39. Kh2 Rd2+ 40. Kg1 Rd1+ 41. Kf2 1-0")

#moves = ["e4", "f5", "Qh5", "a6"]
#moves = ["e4", "c5", "Nf3", "d6", "d4", "cd4", "Nd4", "Nf6", "Nc3", "a6", "Be3", "e6", "Qd2", "Be7", "f3", "Nc6", "g4", "OO", "OOO","Nd4","Bd4","b5","g5","Nd7","h4","Rb8","Be3","Qa5","Kb1", "b4","Ne2","Nc5","Nd4","Bb7","h5","Rfd8","g6", "Bf6","gf7","Kf7","Rg1","Na4","Bh3","Nc3","bc3","bc3","Nb3","Be4","Qc1","Rb3","ab3","Rb8","fe4","Rb3","cb3","c2"]
teams = ["w","b"]
castle_info = []
for team, amove in zip(cycle(teams),moves):

  print(team, amove)

  notation_move(team, amove, castle_info)
  pawn_upgrade()

  king_loc = ""

  if team == "w":
    opp_team = "b"
  else:
    opp_team = "w"

  for line in search_board(opp_team + "K"):
    if line != []:
      king_loc = line[0]
  if check_check(king_loc) != ():
    if check_mate(king_loc) == True:
      sys.exit()
    else:
      if team == "w":
        print("Black king in check!")
      else:
        print("White king in check!")

  if amove[0] in ["K","R"]:
    if amove[0] == "K":
      castle_info.append((team,amove[0]))
    else:
      castle_info.append((team,amove))

  if team == "w" and amove[1] == "4":
    castle_info.append((team,amove))
  elif team == "b" and amove[1] == "5":
    castle_info.append((team,amove))
'''
