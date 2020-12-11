import enum
import os, sys
import math
from collections import Counter

def startup_code(debug = False):

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    filename = "/D10_Input"
    if debug:
        filename += "Test"
    with open( current_working_directory + filename + '.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( map(int, input_list) )


'''

'''
def star_19_solution(input_list):

    joltage_adapters = sorted(input_list)
    previous_adapter = 0
    diffs_dict = {1:0, 2:0, 3:1} # we start 3 at 1 because the last will always be 3 lower than your device
    for j in joltage_adapters:
        diffs_dict[j-previous_adapter] += 1
        previous_adapter = j

    return diffs_dict[1] * diffs_dict[3]


'''
Honestly, this solution was beyond me. I am still trying to figure out how
it exactly works.
'''
def star_20_solution(input_list):

    joltage_adapters = sorted(input_list)
    joltage_adapters.append(joltage_adapters[-1] + 3)

    dp = Counter()
    dp[0] = 1

    for jolt in joltage_adapters:
        dp[jolt] = dp[jolt - 1] + dp[jolt - 2] + dp[jolt - 3]
        #print("Jolt: {}\n  dp[jolt]: {}\n".format(jolt, dp[jolt]))

    #print(dp)

    return dp[joltage_adapters[-1]]


if __name__ == "__main__":
    input_list = startup_code(debug=False)
    print( "Star 19 Solution: {}".format(star_19_solution(input_list)) )
    print( "Star 20 Solution: {}".format(star_20_solution(input_list)) )