import enum
import os, sys
import math
import re
import timeit

def startup_code():

    current_working_directory = __file__.rsplit( '/', 1 )[0]

    with open( current_working_directory + '/D7_Input.txt', 'r' ) as file:
        input_list = file.read().splitlines()

    return list( input_list )


'''
Class Tree. Tree.root contains a Node object that represents its root,
while Tree.children contains references to its child Nodes. Finally,
Tree.Nodes contains a list of tuples representing all nodes found within
the tree (we use this function to find instances of Shiny Gold bags). 
'''
class Tree():

    def __init__(self, root_node):
        self.root = root_node
        self.children = []
        self.Nodes = []

    def addNode(self, node_obj):
        self.children.append(node_obj)

    '''
    Instantiates a list of all nodes the tree contains,
    then checks the Node.key (stored as a tuple) for each
    and returns true if we find any instance of a Shiny Gold bag.
    '''
    def can_contain_sg(self):
        if len(self.Nodes) == 0:
            self.getAllNodes()
        for n in self.Nodes:
            if n[0] == "shiny gold":
                return True
        return False

    '''
    Instantiate the recursive search for the number of child bags
    '''
    def total_num_bags_inside(self):
        answer = 0
        if self.children != []:
            for child in self.children:
                answer += child.number_of_child_bags()
        return answer
        
    def getAllNodes(self):
        self.Nodes.append((self.root.key, self.root.data))
        for child in self.children:
            self.Nodes.append((child.key, child.data))
        for child in self.children:
            if child.getChildNodes(self.Nodes) != None:
                child.getChildNodes(self.Nodes)

        # Debug print statements
        # print("\nTree Root: "+ self.root.key)
        # print(*self.Nodes, sep = "\n\t")
        # print('Tree Size:' + str(len(self.Nodes))+"\n")

'''
Node class of our Tree. Node.key contains the color of the node,
while Node.data contains the quantity of bags that fit.
'''
class Node():

    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.children = []

    '''
    Recursively count the number of child bags a node contains
    '''
    def number_of_child_bags(self):
        if len(self.children) == 0:
            return self.data
        answer = self.data
        for child in self.children:
            answer += (self.data * child.number_of_child_bags())
        return answer

    def addNode(self, node_obj):
        self.children.append(node_obj)

    def getChildNodes(self,Tree):
        for child in self.children:
            if child.children:
                child.getChildNodes(Tree)
                Tree.append((child.key, child.data))
            else:
                Tree.append((child.key, child.data))
        

'''
Build the baggage ruleset given the puzzle input.
Each line begins with the color of the bag we're
adding, then subsequently gives the rules for that color.
If the rules for the color contains the word 'no other',
then we're talking about a leaf node of the tree we'll build.
Otherwise, we use a regular expression to capture the number
and color for each rule definition and add them as a dictionary
where the key is the color of bag within the ruleset and the value
is the quantity of those bags our current color can hold.
'''
def process_baggage_rules(input_list):
   
    baggage_rules = {}
    for rule in input_list:
        rule_root = " ".join(rule.split(" ")[0:2])
        if "no other" in rule:
            baggage_rules[rule_root] = {None}
        else:
            baggage_rules[rule_root] = {}
            regex = re.compile(r'([\d]+)\s([\w]+\s[\w]+)\sbag[s]?')
            allowed_bags_in_rule = regex.findall(rule)
            for allowed_bag in allowed_bags_in_rule:
                bag_color, bag_color_qty = allowed_bag[1], int(allowed_bag[0])
                baggage_rules[rule_root][bag_color] = bag_color_qty

    # Debug Code
    # print("\nRules Data Structure\n")
    # for key, value in baggage_rules.items():
    #     print('  ', key, '->', value)

    return baggage_rules


'''
Recursive function to add children to the baggage tree. We
first get all the children we'll need to add given the baggage
ruleset. Then, assuming of course there are children to add,
we go through each child and create a new node for the child,
then recursively call the function to add the child's children,
and finally when that returns (because eventually we hit no more
children to add), attach that resulting new child node to the current.
'''
def add_children_to_baggage_tree(baggage_key, baggage_rules, current_node):

    children_to_add = baggage_rules[baggage_key]

    if None in children_to_add:
        return

    # Memoization time! If we've already calculated
    # the current node's children, there's no reason
    # for us to do so again...
    if baggage_key in memo:
        #print("cache hit: {}".format(baggage_key))
        current_node.children = memo[baggage_key]
        return

    for child_key, qty in children_to_add.items():
        new_child_node = Node(child_key, qty)
        add_children_to_baggage_tree(child_key, baggage_rules, new_child_node)
        current_node.addNode(new_child_node)

    # In the name of memoization, cache the children!
    if baggage_key not in memo:
        #print("cache add: {}".format(baggage_key))
        memo[baggage_key] = current_node.children

'''
We build a "baggage tree" by taking in a color of bag for our
root node and the dictionary of baggage rules built previously.
'''
def build_baggage_tree(baggage_key, baggage_rules):
    
    # Intantiate the root of the baggage tree
    root_node = Node(key = baggage_key, data = 1)
    baggage_tree = Tree(root_node)

    # Grab the children we'll need to add to the root of
    # the baggage tree and, if there are children to add,
    # begin a recursive function that continually adds
    # new children until we've exhausted them
    children_to_add = baggage_rules[baggage_key]

    if None in children_to_add:
        return baggage_tree

    for child_key, qty in children_to_add.items():
        new_child_node = Node(child_key, qty)
        add_children_to_baggage_tree(child_key, baggage_rules, new_child_node)
        baggage_tree.addNode(new_child_node)
    
    return baggage_tree


'''
Build a baggage tree for every possible color combination, then
use the Tree.can_contain_sg() function to determine if that tree
with root color contains any instances of a Shiny Gold bag. Count
these instances up for the answer.
'''
def star_13_solution(baggage_rules):

    answer = 0
    for color in baggage_rules.keys():
        colored_tree = build_baggage_tree(color, baggage_rules)
        color_contains_sg = colored_tree.can_contain_sg()
        if color_contains_sg and color != "shiny gold":
            answer += 1

    return answer


'''
Build a baggage tree with Shiny Gold as our root node,
then use the Tree.total_num_bags_inside() function to
count the number of children bags we must have given
the baggage rules.
'''
def star_14_solution(baggage_rules):

    return build_baggage_tree("shiny gold", baggage_rules).total_num_bags_inside()


memo = {}
if __name__ == "__main__":
    input_list = startup_code()
    baggage_rules = process_baggage_rules(input_list)

    start = timeit.default_timer()
    print( "Star 13 Solution: {}".format(star_13_solution(baggage_rules)) )
    stop = timeit.default_timer()
    print( '  Runtime: {}s'.format(stop - start) ) 

    start = timeit.default_timer()
    print( "Star 14 Solution: {}".format(star_14_solution(baggage_rules)) )
    stop = timeit.default_timer()
    print( '  Runtime: {}s'.format(stop - start) )