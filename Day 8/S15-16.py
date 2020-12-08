import enum
import os, sys
import math
import re
import timeit
import time

def startup_code(debug = False):

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    filename = "/D8_Input"
    if debug:
        filename += "Test"
    with open( current_working_directory + filename + '.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )


class MachineState:

    def __init__(self, accumulator=0, idx=0):
        self.accumulator = accumulator
        self.idx = idx
        self.op_history = []
        self.Command = MachineState.CommandParser(self)

    def reset_op_history(self):
        self.op_history = []

    def add_op_history(self, idx):
        self.op_history.append(idx)

    def visualize_state(self):
        print("\nCurrent Machine State:")
        print("  accumulator = {}".format(self.accumulator))
        print("  idx = {}".format(self.idx))

    class CommandParser:

        def __init__(self, MachineState):
            self.MachineState = MachineState

        def acc(self, arg):
            self.MachineState.accumulator += arg
            self.MachineState.idx += 1

        def jmp(self, arg):
            self.MachineState.idx += arg

        def nop(self):
            self.MachineState.idx += 1


'''
Begin at instruction indexed at zero and perform the correct command.
Keep track of the indicies of all the instructions we've run and if we
ever land on an instruction we've read previously, then in our toy
machine, we must have gotten stuck in an infinite loop (there is no 
branching in this toy assembly language). We return the value of the 
accumulator and False to indicate execution of code lead to a infinite loop.
'''
def run_assembly(ops):

    Machine = MachineState()

    while (Machine.idx < len(ops)):

        # Halt execution if loop detected
        if Machine.idx in Machine.op_history:
            return (Machine.accumulator, False)
        else:
            Machine.add_op_history(Machine.idx)

        # Prepare current idx for execution
        current_op = ops[Machine.idx].split(" ")
        current_cmd, current_arg = current_op[0], int(current_op[1])

        # Execute specified command
        if "acc" == current_cmd:
            Machine.Command.acc(current_arg)
        elif "jmp" == current_cmd:
            Machine.Command.jmp(current_arg)
        else: # nop
            Machine.Command.nop()
        
    # Program terminated successfully
    return (Machine.accumulator, True)


'''
Run the assembly code until we detect an infinite loop
and return the value of the accumulator.
'''
def star_15_solution(input_list):

    return run_assembly(input_list)[0]


'''
Brute force solution. Duplicate the list of instructions and change
one line at a time. If the program failed (exited with status False),
we try swapping the next nop or jmp instruction. Continue until the
program executes successfully (exists with status True).
'''
def star_16_solution(input_list):

    new_ops = input_list.copy()
    last_op_swapped = 0

    program_fully_executed = False
    while( True ):

        program_execution_results = run_assembly(new_ops)
        program_fully_executed = program_execution_results[1]

        if not program_fully_executed:
            # Shuffle the next instruction
            new_ops = input_list.copy()
            for i in range(last_op_swapped+1, len(new_ops)):
                if "jmp" in input_list[i]:
                    new_ops[i] = new_ops[i].replace("jmp", "nop")
                    last_op_swapped = i
                    break
                if "nop" in input_list[i]:
                    new_ops[i] = new_ops[i].replace("nop", "jmp")
                    last_op_swapped = i
                    break
        else:
            return program_execution_results[0]


if __name__ == "__main__":
    input_list = startup_code(debug=False)
    print( "Star 15 Solution: {}".format(star_15_solution(input_list)) )
    print( "Star 16 Solution: {}".format(star_16_solution(input_list)) )