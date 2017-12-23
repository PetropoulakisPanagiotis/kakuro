from csp import *
import itertools
import time

# Kakuro problem #
class Kakuro(CSP):

    def __init__(self,variables,domains,neighbors,constraints,blankVar):
        self.blankVar = blankVar # For debug
        self.totalTime = None # Total time pass to solve problem
        self.val = None # For result

        CSP.__init__(self,variables,domains,neighbors,constraints)

    def solveBT(self):

        # Solve problem with pure backtracking #

        # Count total time for backtrack algorithm #
        start = int(round(time.time() * 1000))

        result = backtracking_search(self,)

        end = int(round(time.time() * 1000))

        if not result:
            self.val = "There isn't solution in given problem\n"

        self.val = "Problem solved with pure backtracking\n"
        self.val += "Results: \n"

        for i in range(self.blankVar):
            self.val += "X" 
            self.val += str(i + 1)
            self.val += " = "
            self.val += str(result[i + 1])

        self.totalTime = end - start
        self.val += "Total time in milliseconds: "
        self.val += str(end - start) + "\n"

    def solveFCMRVLCV(self):

        start = int(round(time.time() * 1000))

        result = backtracking_search(self,select_unassigned_variable=mrv,order_domain_values=lcv,inference=forward_checking)

        end = int(round(time.time() * 1000))

        if not result:
            self.val = "There isn't solution in given problem\n"

        self.val = "Problem solved with FC + (MRV,LCV)\n"
        self.val += "Results: \n"

        for i in range(self.blankVar):
            self.val += "X" 
            self.val += str(i + 1)
            self.val += " = "
            self.val += str(result[i + 1])
            self.val += "\n"

        self.totalTime = end - start
        self.val += "Total time in milliseconds: "
        self.val += str(end - start) + "\n"

    def solveMACMRVLCV(self):

        start = int(round(time.time() * 1000))

        result = backtracking_search(self,select_unassigned_variable=mrv,order_domain_values=lcv,inference=mac)

        end = int(round(time.time() * 1000))

        if not result:
            self.val = "There isn't solution in given problem\n"

        self.val = "Problem solved with MAC + (MRV,LCV)\n"
        self.val += "Results: \n"

        for i in range(self.blankVar):
            self.val += "X" 
            self.val += str(i + 1)
            self.val += " = "
            self.val += str(result[i + 1])
            self.val += "\n"

        self.totalTime = end - start
        self.val += "Total time in milliseconds: "
        self.val += str(end - start) + "\n"

    def getTotalTime(self):
        return self.totalTime

    def printResult(self):
        print (self.val)

    def getNAssigns(self):
        return self.nassigns

# Cartesian of list of lists #
# Example: [[1],[2,3]]       #
# Result: [(1,2),(1,3)]      #

def cartesian(lists):
    if lists == []:
        return [()]

    return [x + (y,) for x in cartesian(lists[:-1]) for y in lists[-1]]

# Get total variables by given sums and blank variables #
# For example: x1 + x2 = 3. sums = [["x1","x2",3]] and  #
# blankVar == 2                                         #
# getVariables() -> [1,2,3]                             #

def getVariables(sums,blankVar):
    return [i + 1 for i in range(len(sums) + blankVar)]

# Get domains by given sums and blank variables         #
# For example: x1 + x2 = 3. sums = [["x1","x2",3]] and  #
# blankVar == 2                                         #
# getDomains() -> var1 and  var2: 1,2,3,4,5,6,7,8,9     #
# var3(x1 + x2 = 3) = [[1,2,["x1","x2"]],...,]          #

def getDomains(sums,blankVar):
    domains = {}
    values = [1,2,3,4,5,6,7,8,9]

    # Fix domains of blank variables #
    for i in range(blankVar):
        domains[i + 1] = [j for j in values]

    # Fix domains of sums             #
    # ("x1","x2",3) -> (1,2) or (2,1) #

    # Find domain of every sum #
    for i in range(len(sums)):
        productItems = [] # For example: [[1,2],[5,3]]

        # Fix productItems: x1 + x2 = 3: productItems is a list of 2 * values #
        # 2 * values -> two lists                                             #
        # Find cartesian of two elements                                      #
        for element in sums[i]:
            # Count total blank variables in current sum #
            if not isinstance(element,int): # Overpass int(result of sum)
                productItems.append(values)

        # Find cartesian for variables included in sum #
        totalValues = cartesian(productItems)
        fixValues = []

        # Keep valid values: x1 + x2 = 3 -> (1,2) or (2,1) not (2,2)

        # For every element in cartesian: (1,2) for example #
        for item in totalValues:
            count = 0

            # Find sum of current item: 1 + 3 = 3 #
            for element in item:
                count += element

            if count == sums[i][-1]: # Valid value (1,2) == ("x1","x3",3)
                newItem = []
                newItem = list(item)


                # In (1,2) we append and the id of sum                   #
                # In simple words (1,2) is from the sum of "x1" + "x2"   #
                # This is usefull for constraints                        #
                newItem.append((sums[i][0:len(sums[i])- 1]))
                fixValues.append(newItem)

        domains[i + (blankVar + 1)] = fixValues

    return domains


# Get neighbors by given sums and blank variables       #
# For example: x1 + x2 = 3. sums = [("x1","x2",3)] and  #
# blankVar == 2                                         #
# getNeighbors() -> var1: 2,3  var2 :1,3                #
# var3: 1,2                                             #

def getNeighbors(sums,blankVar):
        neighbors = {}

        # Fix Blank variables #
        for i in range(blankVar):
            currentNeighbors = [] # Neighbors of current variable

            # Find current variable in sums #
            count = 0 # Number of sum

            for item in sums:
                if "x" + str(i + 1) in item: # Variable participates in current sum
                    for element in item: # Add neighbors in current sum
                        # Skip myself and result of sum #
                        if (not isinstance(element,int)) and (element != "x" + str(i + 1)):
                            currentNeighbors.append(int(element[1:])) # "x1" skip 'x' add 1

                    # Variable is neighbor with sum variable  #
                    # First sum has id (blankVar + 1)         #
                    currentNeighbors.append(count + (blankVar + 1))

                count += 1

            # Keep our neighbors sorted #
            currentNeighbors.sort() # Fix list

            neighbors[i + 1] = currentNeighbors

        # Find neighbors of sums #
        for i in range(len(sums)):
            currentNeighbors = [] # Neighbors of current variable

            # For current sum find variables that participate in sum #
            # x1 + x2 = 3. var3 has 1,2 as neighbors                 #

            for element in sums[i]:
                if not isinstance(element,int): # Skip result of sum
                    currentNeighbors.append(int(element[1:])) # "x1" skip 'x' add 1

            currentNeighbors.sort()

            neighbors[i + (blankVar + 1)] = currentNeighbors

        return neighbors

# Check if given values are valid #
# A and B should be neighbors     #

def getConstraints(A,a,B,b):

    # A,B are blank variables #
    if isinstance(a,int) :
        if isinstance(b,int):
            return a != b # Neighbors should have different value


    # A,B are blank variables #
    if isinstance(b,int):
        if isinstance(a,int):
            return a != b

    # A is blank variable #
    if isinstance(a,int):
        metaData = b[-1] # Take string: [1,2,["x1","x2"]]
        # metData = ["x1","x2"]

        # Find where A exists in B #
        pos = 0

        for item in metaData:
            if A == int(item[1:]): # From Xi skip X and keep i
                if b[pos] == a: # X1 should have the value of 1 for example
                    return True
                break
            pos += 1

    # B is blank variable #
    if isinstance(b,int):
        metaData = a[-1]

        # Find where B exists in A #
        pos = 0
        for item in metaData:
            if B == int(item[1:]):
                if a[pos] == b:
                    return True
                break
            pos += 1

    return False

# Every model is a kakuro game                             #
# Model calculates variables, domains etc for current game #

# Sums: information of sums #

# Example of sums: [["x1","x2",2],["x2","x3",4]] #

class Model():

    def __init__(self,sums,blankVar):
        self.sums = sums
        self.blankVar = blankVar
        self.variables = getVariables(sums,blankVar)
        self.domains = getDomains(sums,blankVar)
        self.neighbors = getNeighbors(sums,blankVar)
        self.constraints = getConstraints

    def getVariables(self):
        return self.variables

    def getDomains(self):
        return self.domains

    def getNeighbors(self):
        return self.neighbors

    def getConstraints(self):
        return self.constraints

    # For debug #
    def getBlankVar(self):
        return self.blankVar;

# You can find 6 different kakuro puzzles here #

# Given problem #
puzzle1 = [ ["x1","x2",3], ["x3","x4","x5","x6",10], ["x7","x8",3], ["x1","x3",4], 
            ["x2","x4",3], ["x5","x7",6], ["x6","x8",3]
        ]
blankVar1 = 8

# Puzzle2: grid 8 x 8 easy #
puzzle2 = [ ["x1","x2",4], ["x3","x4",4], ["x5","x6","x7","x8",16],
            ["x9","x10","x11",6], ["x12","x13",3], ["x14","x15",12],
            ["x16","x17",4], ["x18","x19","x20","x21","x22",15],
            ["x23","x24","x25","x26","x27",16], ["x28","x29",4], ["x30","x31",4],
            ["x32","x33",3], ["x34","x35","x36",7], ["x37","x38","x39","x40",11], 
            ["x41","x42",4], ["x43","x44",3], ["x5","x12","x16","x23",19], 
            ["x34","x41",3], ["x6","x13","x17","x24",10], ["x35","x42",4],
            ["x1","x7",3], ["x25","x30","x36",7], ["x2","x8",4], 
            ["x18","x26","x31",8], ["x14","x19","x27",7], ["x37","x43",3],
            ["x9","x15","x20",14], ["x38","x44",4], ["x3","x10",4], 
            ["x21","x28","x32","x39",11], ["x4","x11",5], 
            ["x22","x29","x33","x40",10]
        ]
blankVar2 = 44

# Puzzle3: grid 8x8 intermediate #
puzzle3 = [ ["x1","x2","x3",12], ["x4","x5","x6",19],
            ["x7","x8","x9","x10",28], ["x11","x12","x13",9],
            ["x14","x15","x16","x17","x18",35], ["x19","x20",13],
            ["x21","x22","x23","x24",13], ["x25","x26","x27","x28",27],
            ["x29","x30",15], ["x31","x32","x33","x34","x35",16],
            ["x36","x37","x38",6], ["x39","x40","x41","x42",12],
            ["x43","x44","x45",20], ["x46","x47","x48",21], ["x1","x7",9],
            ["x19","x25",12], ["x36","x43",8], ["x2","x8","x14","x20","x26",22],
            ["x37","x44",12], ["x3","x9","x15",23], ["x27","x31", "x38", "x45",16],
            ["x10","x16",16], ["x28","x32",9], ["x17","x21",11], ["x33","x39",10],
            ["x4","x11","x18","x22",30], ["x34","x40","x46",16], ["x5","x12",4],
            ["x23","x29","x35","x41","x47",16], ["x6","x13",9], ["x24","x30",12],
            ["x42","x48",11]
        ]
blankVar3 = 48

# Puzzle4: grid 9x11 easy #
puzzle4 = [ ["x1","x2",14], ["x3","x4",11], ["x5","x6",4],
            ["x7","x8","x9","x10","x11",30], ["x12","x13","x14",12],
            ["x15","x16",4], ["x17","x18","x19",23], ["x20","x21",9],
            ["x22","x23",10], ["x24","x25",11], ["x26","x27","x28","x29","x30",25],
            ["x31","x32","x33",22], ["x34","x35",4], ["x36","x37",12],
            ["x38","x39","x40",24], ["x41","x42","x43","x44","x45",16],
            ["x46","x47",17], ["x48","x49",3], ["x50","x51",4],
            ["x52","x53","x54",6], ["x55","x56",4], ["x57","x58","x59",6],
            ["x60","x61","x62","x63","x64",26], ["x65","x66",11], ["x67", "x68",11],
            ["x69","x70",14], ["x1","x7",14], ["x20","x26",13], ["x38","x46",17],
            ["x57","x65",5], ["x2","x8","x15","x21","x27",16],
            ["x39","x47","x52","x58","x66",28], ["x9","x16",8], ["x28","x34","x40",12],
            ["x53","x59",3], ["x3","x10",16], ["x29","x35",8], ["x48","x54",3],
            ["x4","x11",12], ["x22","x30",16], ["x41","x49",3], ["x60","x67",12], 
            ["x17","x23",9], ["x36","x42",12], ["x61","x68",16], ["x12","x18",10], 
            ["x31","x37","x43",17], ["x55","x62",3],
            ["x5","x13","x19","x24","x32",17], ["x44","x50","x56","x63","x69",15],
            ["x6","x14",12], ["x25","x33",17], ["x45","x51",7], ["x64","x70",12]
        ]
blankVar4 = 70

# Puzzle5: grid 9x11 intermediate #
puzzle5 = [ ["x1","x2",9], ["x3","x4",9], ["x5","x6",16], ["x7","x8","x9",14],
            ["x10","x11","x12","x13","x14",24], ["x15","x16","x17","x18",10], ["x19","x20",8], 
            ["x21","x22",12], ["x23","x24",5], ["x25","x26","x27",15], ["x28","x29",8],
            ["x30","x31","x32","x33","x34",31], ["x35","x36","x37","x38","x39",30],
            ["x40","x41","x42","x43","x44",30], ["x45","x46", 15], ["x47","x48","x49",20], 
            ["x50","x51",14], ["x52","x53",13], ["x54","x55",16], ["x56","x57","x58","x59",12], 
            ["x60","x61","x62","x63","x64",32], ["x65","x66","x67",24], ["x68","x69",13],
            ["x70","x71",14], ["x72","x73",16], ["x7","x15","x21","x28",11], ["x40","x47",14],
            ["x60","x68",17], ["x1","x8","x16","x22","x29",19], 
            ["x41","x48","x54","x61","x69",17], ["x2","x9","x17",21], 
            ["x35","x42","x49","x55","x62",35], ["x18","x23",3], ["x36","x43",9],
            ["x63","x70",17], ["x3","x10",7], ["x24","x30","x37","x44","x50",34],
            ["x64","x71",13], ["x4","x11",14], ["x31","x38",8], ["x51","x56",14],
            ["x12","x19","x25","x32","x39",32], ["x57","x65","x72",20],
            ["x5","x13","x20","x26","x33",34], ["x45","x52","x58","x66","x73",28],
            ["x6","x14",10], ["x27","x34",7], ["x46","x53","x59","x67",26]
        ]
blankVar5 = 73

# Puzzle6: grid 9x11 expert #
puzzle6 = [ ["x1","x2",6], ["x3","x4",14], ["x5","x6",10], ["x7","x8",8],
            ["x9","x10","x11","x12","x13",34], ["x14","x15","x16","x17",13],
            ["x18","x19",8], ["x20","x21","x22","x23",20], ["x24","x25","x26","x27",13],
            ["x28","x29",12], ["x30","x31","x32","x33","x34",29],
            ["x35","x36","x37","x38","x39",15], ["x40","x41","x42","x43","x44",28],
            ["x45","x46",12], ["x47","x48","x49","x50",10], ["x51","x52","x53","x54",21],
            ["x55","x56",5], ["x57","x58","x59","x60",14],  ["x61","x62","x63","x64","x65",19],
            ["x66","x67",11], ["x68","x69",5], ["x70","x71",9], ["x72","x73",9],
            ["x1","x7",7], ["x20","x28",8], ["x40","x47",9], ["x61","x68",3],
            ["x2","x8","x14","x21","x29",15], ["x41","x48","x55","x62","x69",15],
            ["x15","x22",12], ["x35","x42","x49","x56","x63",17], ["x16","x23",10],
            ["x36","x43","x50",10], ["x64","x70",3], ["x3","x9","x17",20],
            ["x30","x37","x44",21], ["x57","x65","x71",19], ["x4","x10",16],
            ["x24","x31","x38",19], ["x51","x58",11], ["x11","x18","x25","x32","x39",15],
            ["x52","x59",17], ["x5","x12","x19","x26","x33",16],
            ["x45","x53","x60","x66","x72",28], ["x6","x13",15], ["x27","x34",10],
            ["x46","x54",6], ["x67","x73",3]
        ]
blankVar6 = 73

"""
# Exercise 2 #
model1  = Model(puzzle1,blankVar1)

# Solve kakuro with fc + mrv + lcv #
problem1 = Kakuro(model1.getVariables(),model1.getDomains(),model1.getNeighbors(),model1.getConstraints(),model1.getBlankVar())

problem1.solveFCMRVLCV()
problem1.printResult()

# Solve same kakuro problem with mac + mrv + lcv #
problem1 = Kakuro(model1.getVariables(),model1.getDomains(),model1.getNeighbors(),model1.getConstraints(),model1.getBlankVar())

problem1.solveMACMRVLCV()
problem1.printResult()

"""


# Exercise 3 #
# Keep all puzzles and make calculations #
puzzles = [puzzle1,puzzle2,puzzle3,puzzle4,puzzle5,puzzle6]
blankVars = [blankVar1,blankVar2,blankVar3,blankVar4,blankVar5,blankVar6]

# For debug #
puzzlesId = ["5 x 4 very easy","8 x 8 easy",
            "8 x 8 intermediate", "9 x 11 easy",
            "9 x 11 intermediate", "9 x 11 expert"
        ]

print ("\n6 puzzles solved. Every puzzle solved 15 times\n")
print ("Results: ")

# Winner is based on time #
# Keep how many times FC and MAC wins #
winFC = 0
winMAC = 0

# Make calculations for every puzzzle #
for i in range(6):
    totalTime1 = 0 # For fc
    totalTime2 = 0 # For mac
    extraAssigns1 = 0 # Calculate how many extra assigns current algorithm made
    extraAssigns2 = 0

    # Run 15 times every puzzle #
    for times in range(15):

        # Current puzzle #
        model = Model(puzzles[i],blankVars[i])

        # Solve puzzle with FC #
        problem1 = Kakuro(model.getVariables(),model.getDomains(),model.getNeighbors(),model.getConstraints(),model.getBlankVar())

        problem1.solveFCMRVLCV()

        # Fix results #
        totalTime1 += problem1.getTotalTime()
        extraAssigns1 += (problem1.getNAssigns() - blankVars[i])

        # Solve current puzzle with MAC #
        problem2 = Kakuro(model.getVariables(),model.getDomains(),model.getNeighbors(),model.getConstraints(),model.getBlankVar())

        problem2.solveMACMRVLCV()

        # Fix results #
        totalTime2 += problem2.getTotalTime()
        extraAssigns2 += (problem2.getNAssigns() - blankVars[i])

    # Find average time and extra assigns #
    totalTime1 = totalTime1 / float(15)
    totalTime2 = totalTime2 / float(15)
    extraAssigns1 = extraAssigns1 / float(15)
    extraAssigns2 = extraAssigns2 / float(15)

    # Print results #

    print (puzzlesId[i])
    print ("--------------------------------------------------------")
    print ("Puzzle %d needs: %f milliseconds with FC(MRV,LCV)"  % (i + 1,totalTime1))
    print ("Extra assigns with FC(MRV,LCV): %d" % extraAssigns1)
    print ("\nPuzzle %d needs: %f milliseconds with MAC(MRV,LCV)" %(i + 1,totalTime2))
    print ("Extra assigns with MAC(MRV,LCV): %d" % extraAssigns2)

    if(totalTime1 < totalTime2):
        print ("--> FC wins")
        winFC += 1

    elif(totalTime1 > totalTime2):
        print ("--> MAC wins")
        winMAC += 1

    else:
        print ("--> We have a tie")
        winMAC += 1
        winFC += 1

    print ("\n")

# Based on time #
print ("And the winner algorithm is: ")

if winFC > winMAC:
    print ("FC!!!")

elif winFC < winMAC:
    print ("MAC!!!")

else:
    print ("We have a tie!!!")

# Editor:
# sdi1500129
# Petropoulakis Panagiotis
