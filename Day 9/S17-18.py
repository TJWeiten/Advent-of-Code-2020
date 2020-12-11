import enum
import os, sys
import math
from collections import deque

def startup_code(debug = False):

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    filename = "/D9_Input"
    if debug:
        filename += "Test"
    with open( current_working_directory + filename + '.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( map(int, input_list) )


'''
Slice a preamble of specified length then for each p in that preamble,
subtract it from our target, slice a new list without that element, then
see if the resulting target-p is in the new preamble. Return target once
we've identified a number for which there is no pair sum.
'''
def star_17_solution(input_list, preamble_length):

    for i in range(preamble_length, len(input_list)):
        preamble = input_list[i-preamble_length:i]
        target = input_list[i]
        sum_found = False
        for p in range(len(preamble)):
            search_preamble = preamble[:p] + preamble[p+1:]
            if (target-preamble[p]) in search_preamble:
                sum_found = True
                break
        if not sum_found:
            return target


'''
If we're smaller than our search target, make our contiguous list bigger;
else make the list smaller. Return when we find a list whose sum is target.
'''
def star_18_solution(input_list, target):

    i, j = 0, 1
    while (i < len(input_list)):
        current_sum = sum(input_list[i:j+1])
        if current_sum == target:
            return min(input_list[i:j+1]) + max(input_list[i:j+1])
        elif current_sum < target:
            j += 1
        else:
            i += 1

    return None


if __name__ == "__main__":
    input_list = startup_code(debug=False)
    print( "Star 17 Solution: {}".format(star_17_solution(input_list, 25)) )
    print( "Star 18 Solution: {}".format(star_18_solution(input_list, 756008079)) )