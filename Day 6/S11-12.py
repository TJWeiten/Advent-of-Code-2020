import enum
import os, sys
import math
import re

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D6_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )


'''
I'm sorry today's solution is a bit ugly because I'm 
throwing it together at 2:30AM, but basically concatante
each persons answers into their group and return the list
'''
def process_customs_sheets_s11(input_list):
    group_answers = []
    filled_customs_fields = []
    for person in input_list:
        if person == "":
            filled_customs_fields = sorted(set(filled_customs_fields))
            group_answers.append(filled_customs_fields)
            filled_customs_fields = []
        else:
            filled_customs_fields += list(person)

    return group_answers


'''
Instead of concat, we append each person's list of answers so we
can use a set intersection in the solution function
'''
def process_customs_sheets_s12(input_list):
    group_answers = []
    filled_customs_fields = []
    for person in input_list:
        if person == "":
            filled_customs_fields = sorted(filled_customs_fields)
            group_answers.append(filled_customs_fields)
            filled_customs_fields = []
        else:
            filled_customs_fields.append(list(person))

    return group_answers


'''
Sum length of each group, which can only contain unique answers
due to being cast as a set
'''
def star_11_solution(processed_customs_sheets):

    sum_of_answers = 0
    for group in processed_customs_sheets:
        sum_of_answers += len(group)

    return sum_of_answers


'''
For each group, concat all the member's answers
then sum those together
'''
def star_12_solution(processed_customs_sheets):

    sum_of_answers = 0
    for group in processed_customs_sheets:
        intersected_set = set(group[0])
        for i in range(1,len(group)):
            intersected_set = intersected_set.intersection(group[i])
        sum_of_answers += len(intersected_set)
    
    return sum_of_answers


if __name__ == "__main__":
    input_list = startup_code()
    input_list.append("")
    processed_customs_sheets_s11 = process_customs_sheets_s11(input_list)
    processed_customs_sheets_s12 = process_customs_sheets_s12(input_list)
    #print(processed_customs_sheets_s12)
    print( "Star 11 Solution: {}".format(star_11_solution(processed_customs_sheets_s11)) )
    print( "Star 12 Solution: {}".format(star_12_solution(processed_customs_sheets_s12)) )