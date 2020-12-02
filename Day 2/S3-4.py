import enum
import os, sys
import re

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D2_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )


class PasswordPolicy:
    def __init__(self, minimum, maximum, character):
        self.min = int(minimum)
        self.max = int(maximum)
        self.char = character

'''
Read each line of the input and split on the dividing ':' character,
then use regular expressions to create a PasswordPolicy object
to store the relevant 'rules' for the password. Finally, use
regular expressions to quickly count the occurences of the desired
character from the password policy and see if its in the valid range.
'''
def star_3_solution(input_list):

    valid_count = 0
    for line in input_list:
        line = line.split(":")
        password_policy_str, password_str = line[0].strip(), line[1].strip()
        password_policy_groups = re.match(r'([\d]+)-([\d]+)\s([\w]+)', password_policy_str).groups()
        password_policy = PasswordPolicy( 
                            password_policy_groups[0], # min
                            password_policy_groups[1], # max
                            password_policy_groups[2]  # char
                            )
        times_char_repeated = len(re.findall(r'[' + password_policy.char + ']', password_str))
        if times_char_repeated >= password_policy.min and times_char_repeated <= password_policy.max:
            valid_count += 1

    return valid_count


'''
Star 4 is the same procedure as Star 3, but instead we only check two 
characters of the password at the 'min' and 'max' index. It is valid if
and only if it appears once.
'''
def star_4_solution(input_list):
    
    valid_count = 0
    for line in input_list:
        line = line.split(":")
        password_policy_str, password_str = line[0].strip(), line[1].strip()
        password_policy_groups = re.match(r'([\d]+)-([\d]+)\s([\w]+)', password_policy_str).groups()
        password_policy = PasswordPolicy( 
                                password_policy_groups[0], # min
                                password_policy_groups[1], # max
                                password_policy_groups[2]  # char
                            )
        min_char = password_str[password_policy.min-1] == password_policy.char
        max_char = password_str[password_policy.max-1] == password_policy.char
        if (min_char or max_char) and not (min_char and max_char):
            valid_count += 1

    return valid_count


if __name__ == "__main__":
    input_list = startup_code()
    print( "Star 3 Solution: {}".format(star_3_solution(input_list)) )
    print( "Star 4 Solution: {}".format(star_4_solution(input_list)) )