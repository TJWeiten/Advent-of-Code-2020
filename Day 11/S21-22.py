import enum
import os, sys
import math
import copy

def startup_code(debug = False):

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    filename = "/D11_Input"
    if debug:
        filename += "Test"
    with open( current_working_directory + filename + '.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    input_list = [list(row) for row in input_list]
        
    return list( input_list )


'''
Quick print the board in a more readable manner.
'''
def print_board(seating):
    print()
    for row in seating:
        row_str = ""
        for c in row:
            row_str += c
        print(row_str)
    print()


'''
Check all the adjacent cells around a given row and column [with the ruleset for Star 21].

    If we are currently an empty seat (L) and find an occupied seat (#), we should return False 
    because an empty seat cannot change if there is a single occupied seat near it.

    If we are currently seated (#), we count the number of empty seats (L's) surrounding me,
    returning False if it is less than 4 and True if it is greater than or equal to 4.
'''
def sufficient_adjacent_seats_for_state_change_s21(seating, row, col, current_status):

    adj = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]

    count = 0
    for dx, dy in adj:
        # if we're not out of bounds
        if (0 <= row + dy < len(seating)) and (0 <= col + dx < len(seating[0])):
            if seating[row + dy][col + dx] == "#":
                # we're an empty seat and we should break if we find a single #
                if current_status == "L":
                    return False
                else:
                    count += 1

    if current_status == "L":
        return True
    else:
        return count >= 4


'''
Check all the adjacent cells around a given row and column [with the ruleset for Star 22].

    If we are currently an empty seat (L) and find an occupied seat (#), we should return False 
    because an empty seat cannot change if there is a single occupied seat near it.

    If we are currently seated (#), we count the number of empty seats (L's) surrounding me,
    returning False if it is less than 4 and True if it is greater than or equal to 4.
'''
def sufficient_adjacent_seats_for_state_change_s22(seating, row, col, current_status):

    adj = [(i,j) for i in (-1,0,1) for j in (-1,0,1) if not (i == j == 0)]

    count = 0
    for dx, dy in adj:
        # if we're not out of bounds, increase a multiplier that keeps searching
        # out further in each direction until it finds a seat or leaves the board
        search_multiplier = 1
        in_bounds = (0 <= row + (dy*search_multiplier) < len(seating)) and \
                    (0 <= col + (dx*search_multiplier) < len(seating[0]))
        while in_bounds and seating[row + (dy*search_multiplier)][col + (dx*search_multiplier)] == ".":
            search_multiplier += 1
            in_bounds = (0 <= row + (dy*search_multiplier) < len(seating)) and \
                        (0 <= col + (dx*search_multiplier) < len(seating[0]))
        if (0 <= row + (dy*search_multiplier) < len(seating)) and (0 <= col + (dx*search_multiplier) < len(seating[0])):
            if seating[row + (dy*search_multiplier)][col + (dx*search_multiplier)] == "#":
                # we're an empty seat and we should break if we find a single #
                if current_status == "L":
                    return False
                else:
                    count += 1

    if current_status == "L":
        return True
    else:
        return count >= 5


'''
For every seat on the board, process whether or not we have sufficient seats adjacent to it
for a state change, then change the state of the seat if needed.
'''
def process_board_state_change(seating, star):
    new_seating = copy.deepcopy(seating)
    rows, cols = len(seating), len(seating[0])
    for i in range(rows):
        for j in range(cols):
            if seating[i][j] == "L":
                if star == "21":
                    if sufficient_adjacent_seats_for_state_change_s21(seating, i, j, "L"):
                        new_seating[i][j] = "#"
                else:
                    if sufficient_adjacent_seats_for_state_change_s22(seating, i, j, "L"):
                        new_seating[i][j] = "#"
            elif seating[i][j] == "#":
                if star == "21":
                    if sufficient_adjacent_seats_for_state_change_s21(seating, i, j, "#"):
                        new_seating[i][j] = "L"
                else:
                    if sufficient_adjacent_seats_for_state_change_s22(seating, i, j, "#"):
                        new_seating[i][j] = "L"
            else:
                pass
    return new_seating


'''
Continue altering the board according to the rules until the board
no longer is changing; then return the resulting board.
'''
def return_board_equilibrium(seating, star, print_seating=False):

    i = 0
    if print_seating: print("Round", i); print_board(seating)
    previous_board = copy.deepcopy(seating)
    while (True):
        i += 1
        seating = process_board_state_change(seating, star)
        if print_seating: print("Round", i); print_board(seating)
        if seating == previous_board:
            break
        else:
            previous_board = copy.deepcopy(seating)
    return seating


'''
Acquire the state of the board in equilibrium, then count the number
of filled seats.
'''
def star_21_solution(seating, debug):

    final_board = return_board_equilibrium(seating, "21", debug)

    cnt = 0
    for row in final_board:
        for c in row:
            if c == "#":
                cnt += 1

    return cnt


'''
Acquire the state of the board in equilibrium (using the Star 22 ruleset), 
then count the number of filled seats.
'''
def star_22_solution(seating, debug):

    final_board = return_board_equilibrium(seating, "22", debug)

    cnt = 0
    for row in final_board:
        for c in row:
            if c == "#":
                cnt += 1

    return cnt


if __name__ == "__main__":
    debug = False
    input_list = startup_code(debug)
    print( "Star 21 Solution: {}".format(star_21_solution(input_list, debug)) )
    print( "Star 22 Solution: {}".format(star_22_solution(input_list, debug)) )