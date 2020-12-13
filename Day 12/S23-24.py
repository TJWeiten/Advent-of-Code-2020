import enum
import os, sys
import math
import copy

def startup_code(debug = False):

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    filename = "/D12_Input"
    if debug:
        filename += "Test"
    with open( current_working_directory + filename + '.txt', 'r' ) as file:
        input_list = file.read().splitlines()
        
    return list( input_list )


class Ship():

    def __init__(self):
        self.x = 0
        self.y = 0
        self.Waypoint = Ship.Waypoint()

    def move_to_waypoint(self, num_times):
        self.x += (self.Waypoint.x * num_times)
        self.y += (self.Waypoint.y * num_times)
    
    class Waypoint():

        def __init__(self):
            self.x = 10
            self.y = 1

        '''
        Determine the number of quadrants our rotation will move us, then
        change the signs and values of x and y according to the rules.
        '''
        def rotate(self, direction, num_degrees):
            quadrant_rotation = (num_degrees % 360) // 90
            l_direction_modifier = 1 if direction == "L" else -1
            r_direction_modifier = 1 if direction == "R" else -1
            if   quadrant_rotation == 1:
                self.x, self.y = (-1 * l_direction_modifier) * self.y, (-1 * r_direction_modifier) * self.x
            elif quadrant_rotation == 2:
                self.x, self.y = (-1) * self.x, (-1) * self.y
            elif quadrant_rotation == 3:
                self.x, self.y = (-1 * r_direction_modifier) * self.y, (-1 * l_direction_modifier) * self.x

        def move(self, compass, distance):
            if   compass == "N": self.y += distance
            elif compass == "E": self.x += distance
            elif compass == "S": self.y -= distance
            elif compass == "W": self.x -= distance


'''
Simple parsing of parameters, nothing more.
'''
def star_23_solution(input_list):

    # 0 = east, 90 north, 180 west, 270 south
    # dict is (dx,dy)
    headings = {0: (1,0), 90: (0,1), 180: (-1,0), 270: (0,-1)}

    x, y, h = 0, 0, 0
    for i in input_list:
        cmd, parameter = i[0], int(i[1:])
        if   cmd == "N": y += parameter
        elif cmd == "E": x += parameter
        elif cmd == "S": y -= parameter
        elif cmd == "W": x -= parameter
        elif cmd == "L": h = (h + parameter) % 360
        elif cmd == "R": h = (h - parameter) % 360
        elif cmd == "F":
            x += (headings[h][0] * parameter)
            y += (headings[h][1] * parameter)
        else:
            raise ValueError()

    return abs(x) + abs(y)


'''
Parse the command and pass the appropriate action to the Ship object.
'''
def star_24_solution(input_list):

    ship = Ship()

    for i in input_list:
        cmd, parameter = i[0], int(i[1:])
        if   cmd == "N" or cmd == "E" or cmd == "S" or cmd == "W": 
            ship.Waypoint.move(cmd, parameter)
        elif cmd == "L" or cmd == "R": 
            ship.Waypoint.rotate(cmd, parameter)
        elif cmd == "F":
            ship.move_to_waypoint(parameter)
        else:
            raise ValueError()

    return abs(ship.x) + abs(ship.y)


if __name__ == "__main__":
    input_list = startup_code(debug=False)
    print( "Star 21 Solution: {}".format(star_23_solution(input_list)) )
    print( "Star 22 Solution: {}".format(star_24_solution(input_list)) )