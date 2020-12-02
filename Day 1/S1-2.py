import os, sys

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/S1_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( map(int, input_list) )

'''
Search for the solution by sorting, then starting at the extremes of 
the list and making your way inwards—if you're bigger than the search_target,
then you must pick a number that makes you smaller; else, you need to
pick a number that makes you smaller. Return if we found the answer,
or return False if no solution was found (index i passes index j).
'''
def star_1_solution(input_list, search_target):

    input_list.sort(reverse = True)

    i, j = 0, len(input_list)-1
    while ( True ):
        sum_to_check = input_list[i] + input_list[j]
        if sum_to_check == search_target:
            return "{} * {} = {}".format(input_list[i], input_list[j], \
                input_list[i] * input_list[j])
        elif sum_to_check > search_target:
            i += 1
        else:
            j -= 1
        
        if i > j:
            return False

'''
The solution for Star 2 is essentially the same as Star 1, but
this time we must iterate through the first index (k), then
repeat the procedure from Star 1. This time, if we fail to identify
two numbers at index i and j that can reach our search target minus
the list at index k, we move to the next k and start the search again.
Failure is indicated by exhausting the k range.
'''
def star_2_solution(input_list, search_target):
    
    input_list.sort(reverse = True)

    for k in range(len(input_list)-2):

        narrowed_search_target = search_target - input_list[k]
        i, j = k + 1, len(input_list)-1
        while ( True ):
            sum_to_check = input_list[i] + input_list[j]
            if sum_to_check == narrowed_search_target:
                return "{} * {} * {} = {}".format(input_list[k], input_list[i], input_list[j], \
                    input_list[k] * input_list[i] * input_list[j])
            elif sum_to_check > narrowed_search_target:
                i += 1
            else:
                j -= 1
            
            if i > j:
                break
    
    return False


if __name__ == "__main__":
    input_list = startup_code()
    print( "Star 1 Solution: {}".format(star_1_solution(input_list, 2020)) )
    print( "Star 2 Solution: {}".format(star_2_solution(input_list, 2020)) )