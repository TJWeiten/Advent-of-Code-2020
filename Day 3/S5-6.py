import enum
import os, sys
import math

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D3_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )

'''
Take the input list and parse it into a two dimensional
array to ensure it is intuitive to index in future steps.
'''
def process_map(input_list):
    map_view = []
    for i, line in enumerate(input_list):
        map_view_line = [char for j, char in enumerate(line)]
        map_view.append(map_view_line)
    return map_view
            

'''
Process the map, then simply iterate through it
counting the number of trees we reach along the way.
'''
def star_5_solution(input_list):

    tree_map = process_map(input_list)
    line_length = len(input_list[0])
    number_lines = len(input_list)

    y, x, tree_count = 0, 0, 0
    while( y < number_lines - 1 ):
        y += 1
        x = (x + 3) % line_length
        if tree_map[y][x] == '#':
            tree_count += 1

    return tree_count


'''
The same as Star 5, but now we iterate over a list of several 
different potential slopes.
'''
def star_6_solution(input_list):
    
    tree_map = process_map(input_list)
    line_length = len(input_list[0])
    number_lines = len(input_list)

    slopes_to_check = [(1,1),(1,3),(1,5),(1,7),(2,1)] # (down, right)

    tree_count = []

    for slope in slopes_to_check:

        y, x, tree_count_for_slope = 0, 0, 0

        while( y + slope[0] < number_lines ):
            y += slope[0]
            x = (x + slope[1]) % line_length
            if tree_map[y][x] == '#':
                tree_count_for_slope += 1
        
        tree_count.append(tree_count_for_slope)

    return math.prod(tree_count)


if __name__ == "__main__":
    input_list = startup_code()
    print( "Star 5 Solution: {}".format(star_5_solution(input_list)) )
    print( "Star 6 Solution: {}".format(star_6_solution(input_list)) )