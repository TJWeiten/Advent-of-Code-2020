import enum
import os, sys
import math
import re

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D4_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )

class Passport():

    def __init__(self, pid=None, cid=None, ecl=None, hcl=None, hgt=None, eyr=None, iyr=None, byr=None):
        self.pid = pid
        self.cid = cid
        self.ecl = ecl
        self.hcl = hcl
        self.hgt = hgt
        self.eyr = eyr
        self.iyr = iyr
        self.byr = byr

    '''
    Checks if all the passport fields are present
    '''
    def passport_fields_present(self):
        # Remeber, since we forgot our passport and want to sneak through,
        # we should ignore a missing CID field
        for key in vars(self):
            if (getattr(self, key) == None) and (key != "cid"):
                return False
        return True

    '''
    Checks every field's (except CID's) value to see if it is valid
    '''
    def valid_passport_fields(self):
        fields = {
                    'pid':self.has_valid_pid,
                    'ecl':self.has_valid_ecl,
                    'hcl':self.has_valid_hcl,
                    'hgt':self.has_valid_hgt,
                    'eyr':self.has_valid_eyr,
                    'iyr':self.has_valid_iyr,
                    'byr':self.has_valid_byr
                 }
        for func in fields:
            if fields[func]() == False:
                return False
        return True

    '''
    Validity check functions
    '''
    # Valid iff 9 digits (leading 0's okay)
    def has_valid_pid(self): 
        regex = re.compile(r'[\d]{9}')
        return bool(regex.fullmatch(str(self.pid)))
    # Valid if one of amb, blu, brn, gry, grn, hzl, oth
    def has_valid_ecl(self): 
        regex = re.compile(r'(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)')
        return bool(regex.fullmatch(str(self.ecl)))
    # Valid if # followed by exactly six characters 0-9 or a-f, ignoring case
    def has_valid_hcl(self): 
        regex = re.compile(r'#[a-f0-9]{6}', flags=re.I)
        return bool(regex.fullmatch(str(self.hcl)))
    # Valid if a two or three digit number, followed by cm or in, 
    # and constrainted by certain sizes
    def has_valid_hgt(self):
        regex = re.compile(r"[\d]{2,3}((cm)|(in))")
        if bool(regex.fullmatch(str(self.hgt))):
            hgt = int(self.hgt[:-2])
            if "cm" in self.hgt:
                return True if hgt >= 150 and hgt <= 193 else False
            elif "in" in self.hgt:
                return True if hgt >= 59 and hgt <= 76 else False
        else:
            return False
    # Valid if at least 2020 and at most 2030
    def has_valid_eyr(self): 
        try:
            eyr = int(self.eyr)
            return True if eyr >= 2020 and eyr <= 2030 else False
        except:
            return False
    # Valid if at least 2010 and at most 2020
    def has_valid_iyr(self): 
        try:
            iyr = int(self.iyr)
            return True if iyr >= 2010 and iyr <= 2020 else False
        except:
            return False
    # Valid if at least 1920 and at most 2002
    def has_valid_byr(self): 
        try:
            byr = int(self.byr)
            return True if byr >= 1920 and byr <= 2002 else False
        except:
            return False

    '''
    String representation of Passport object for debugging purposes
    '''
    def __str__(self):
        passport_str = "Passport("
        for key in vars(self):
            attr = getattr(self, key)
            attr_str = "{} = {}"
        attr_str = ', '.join(key + " = %s" % getattr(self, key) for key in vars(self))
        return passport_str + attr_str + ")"


'''
Turn each passport into a Passport object.
'''
def process_passports(input_list):
    input_list.append("") # append a blank to the end of the file, so we parse it as a full passport
    passports = []
    passport_str = ""
    for i in input_list:
        if i != "":
            passport_str += " " + i
        else: # found end of current passport
            current_passport = Passport()
            for attr in passport_str.strip().split(" "):
                attr = attr.split(":")
                setattr(current_passport, attr[0], attr[1])
            passports.append(current_passport)
            passport_str = ""
    return passports
            

'''
Sum of valid passports where no field missing.
'''
def star_7_solution(input_list):

    return sum(pssprt.passport_fields_present() for pssprt in input_list)


'''
Sum of valid passports where no field is missing 
and contents of each passport's fields are valid
'''
def star_8_solution(input_list):
    
    return sum(pssprt.valid_passport_fields() for pssprt in input_list)


if __name__ == "__main__":
    input_list = startup_code()
    passports = process_passports(input_list)
    print( "Star 7 Solution: {}".format(star_7_solution(passports)) )
    print( "Star 8 Solution: {}".format(star_8_solution(passports)) )