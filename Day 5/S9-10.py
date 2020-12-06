import enum
import os, sys
import math
import re

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D5_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )


'''
Binary search off of a coded string, 
given an index range we're searching and
return the index we end up at
'''
def binary_search(binary_str, low, high):
    for i, c in enumerate(binary_str):
        if c == "F" or c == "L":
            high = high-((high-low)//2) - 1
        else:
            low = low+((high-low)//2) + 1
    return low


'''
Figure out for all the boarding passes we have access to,
what all their seat id's are
'''
def build_seat_ids(input_list):
    seat_ids = []
    for boarding_pass in input_list:
        row_str, seat_str = boarding_pass[0:7], boarding_pass[7:]
        seat_row = binary_search(row_str, 0, 127)
        seat_column = binary_search(seat_str, 0, 7)
        seat_ids.append(seat_row * 8 + seat_column)
    return seat_ids


'''
Just find the max boarding pass
'''
def star_9_solution(seat_ids):

    return max(seat_ids)


'''
Find the gap seat by using the mathematical property that
our missing seat must be equal to the sum of all seats minus
the sum of all seats present except ours
'''
def star_10_solution(seat_ids):
    
    return sum( range( min(seat_ids), max(seat_ids) + 1 ) ) - sum(seat_ids)


if __name__ == "__main__":
    input_list = startup_code()
    seat_ids = build_seat_ids(input_list)
    print( "Star 9 Solution: {}".format(star_9_solution(seat_ids)) )
    print( "Star 10 Solution: {}".format(star_10_solution(seat_ids)) )