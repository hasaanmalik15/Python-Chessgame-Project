# implementation of unit tests

import pytest

from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5,2)
def test_location2index2():
    assert location2index("a1") == (1,1)
def test_location2index3():
    assert location2index("z1") == (26,1)
def test_location2index4():
    assert location2index("z26") == (26,26)


def test_index2location1():
    assert index2location(5,2) == "e2"
def test_index2location2():
    assert index2location(1,1) == "a1"
def test_index2location3():
    assert index2location(26,1) == "z1"
def test_index2location4():
    assert index2location(26,26) == "z26"

wb1 = Bishop(2,5,True)
wb2 = Bishop(4,4,True)
wb3 = Bishop(3,1,True)
wb4 = Bishop(5,5,True)
wb5 = Bishop(4,1,True)

wk1 = King(3,5,True)
wk1a = King(2,5,True)


bb1 = Bishop(3,3,False)
bb2 = Bishop(5,3,False)
bb3 = Bishop(1,2,False)

bk1 = King(2,3,False)


B1 = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1])
B2 = (5, [bb1, bb2, wb3, wb4, bk1, wk1])
B3 = (5, [wb5, bb3, wb2, bb2, wb1, wk1, bk1])


def test_is_piece_at1():
    assert is_piece_at(2,2, B1) == False
def test_is_piece_at2():
    assert is_piece_at(3,3, B1) == True
def test_is_piece_at3():
    assert is_piece_at(4,2, B1) == False
def test_is_piece_at4():
    assert is_piece_at(2,3, B1) == True

def test_piece_at1():
    assert piece_at(3,3, B1) == bb1
def test_piece_at2():
    assert piece_at(2,3, B1) == bk1
def test_piece_at3():
    assert piece_at(2,5, B1) == wb1
def test_piece_at4():
    assert piece_at(1,5, B1) == None

def test_can_reach1():
    assert wb2.can_reach(5,5, B1) == True
def test_can_reach2():
    assert wb1.can_reach(4, 7, B1) == True
def test_can_reach3():
    assert wb5.can_reach(6, 3, B1) == True
def test_can_reach4():
    assert wb1.can_reach(2, 2, B1) == False


def test_can_move_to1():
    assert wb2.can_move_to(5,5, B1) == False
def test_can_move_to2():
    assert bb2.can_move_to(3, 1, B1) == True
def test_can_move_to3():
    assert wb4.can_move_to(7, 7, B1) == False
def test_can_move_to4():
    assert wk1.can_move_to(4, 4, B1) == False


def test_move_to1():
    wb3a = Bishop(5,3,True)
    Actual_B = wb3.move_to(5,3, B1)
    Expected_B = (5, [wb3a, wb1, wk1, wb2, bk1, bb1]) 

    #check if actual board has same contents as expected 
    assert Actual_B[0] == 5

    for piece1 in Actual_B[1]: #we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


    for piece in Expected_B[1]:  #we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to2():
    wb3a = Bishop(5, 3, True)
    Actual_B = wb3.move_to(5, 3, B1)
    Expected_B = (5, [wb3a, wb1, wk1, wb2, bk1, bb1])
    assert Actual_B[0] == 5
    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_move_to3():
    wb1a = Bishop(1, 4, True)
    Actual_B = wb1.move_to(1, 4, B1)
    Expected_B = (5, [wb1a, wk1, wb2, wb3, bk1, bb1, bb2])
    assert Actual_B[0] == 5
    for piece1 in Actual_B[1]:
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[1]:
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found


def test_is_check1():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3])
    assert is_check(True, B2) == True
def test_is_check2():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2])
    assert is_check(False, B2) == False
def test_is_check3():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3, wb4])
    assert is_check(True, B2) == True
def test_is_check4():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2])
    assert is_check(False, B2) == False


def test_is_checkmate1():
    B3 = (5, [wk1a, wb4, bk1, bb2, bb3, wb3, wb5])
    assert is_checkmate(False, B3) == True
def test_is_checkmate2():    
    B3 = (5, [wk1, wb4, bk1, bb2, bb3, wb3, wb5])
    assert is_checkmate(True, B3) == False
def test_is_checkmate3():
    B3 = (5, [wk1, wb4, bk1, bb2, bb3])
    assert is_checkmate(False, B3) == False
def test_is_checkmate4():
    B3 = (5, [wk1, wb4, bk1, bb2, bb3])
    assert is_checkmate(True, B3) == False

def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board2():
    B = read_board("board_examp2.txt")
    assert B[0] == 5

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B2[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B2[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

def test_read_board3():
    B = read_board("board_examp3.txt")
    assert B[0] == 7

    for piece in B[1]:  #we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B3[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found

    for piece1 in B3[1]: #we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(piece) == type(piece1):
                found = True
        assert found