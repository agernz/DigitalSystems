import platform
import os
"""State Machine Simplifier
    Adam Gernes
"""

# Clear console
def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Sort a group of terms into smaller groups based on # of 1's
# Return sorted array
def sortTerms(arr):
    numones = 0
    numsorted = 0
    sorted_bnums = []
    while numsorted < len(arr):
        group = []
        for term in arr:
             if term.count("1") == numones:
                 numsorted += 1
                 group.append(term)
        # Add group to list as long as there are terms in the group
        if len(group) > 0:
            sorted_bnums.append(group)
        numones += 1

    return sorted_bnums

# Variable length
numVars = 3
# State assignment length
digits = numVars-1

# Perform the Quine McCluskey method
# Mark used values with a '*',
#   unmarked values are prime implicants
# Returns the table of all values, marked and unmarked,
#   as a 3D array
def quine(sorted_bnums):  
    # Do each Column
    index_col = 0
    cols = []
    cols.append(sorted_bnums)

    # Repeat until only one box in column
    while len(cols[index_col]) > 1:
        index = 0
        # Add next column
        cols.append([])
        
        # Compare adjacent rows, add to new column
        while index < len(cols[index_col])-1:
            arr = []
            cur_box = cols[index_col][index]
            next_box = cols[index_col][index+1]
            index += 1
            # All numbers in current box
            for i in range(0, len(cur_box)):
                # Against all numbers in next box
                for x in range(0, len(next_box)):
                    diffcount = 0
                    diffi = 0
                    # Compare each digit
                    for y in range(0, numVars):
                        # Count different digits
                        if cur_box[i][y] != next_box[x][y]:
                            diffcount += 1
                            diffi = y

                    # Only 1 digit varies, add to next column
                    if diffcount == 1:
                        # Take only to size of digit since end
                        # may contain a star
                        b = cur_box[i][:numVars]
                        b = list(b)                
                        b[diffi] = "-"
                        arr.append("".join(b))
                            
                        # Mark values as used if not already marked
                        if not cur_box[i].endswith("*"):
                            cur_box[i] += "*"
                        if not next_box[x].endswith("*"):
                            next_box[x] += "*"

            cols[index_col+1].append(arr)
        index_col += 1
    return cols

# Extract prime implicants from a 3D array
#   returned by Quine
# Return array of prime implicants
def getPrimeImplicants(Qtable):
    primes = []
    for i in range(0, len(Qtable)):
        for x in range(0, len(Qtable[i])):
            for y in range(0, len(Qtable[i][x])):
                implicant = Qtable[i][x][y]
                if not implicant.endswith("*"):
                    # Do not add duplicats
                    if not implicant in primes:
                        primes.append(Qtable[i][x][y])
    return primes

# Stores all possibilites of prime implicants as
#   an array ofdecimal numbers
# Arrays are than compared to one another to determine
#   if a prime implicant is actually essential
# Returns an array of essential prime implicants
def getEssentials(primes):
    dash = "-"
    decimals = []
    # Turn binary number into the decimal numbers it represents
    for p in primes:
        indexes = []
        nums = []
        x = 0
        # Store position of dashes 
        for i in range(0,len(p)):
            if p[i] == dash:
                indexes.insert(0,i)

        # Create all possible numbers
        prime = p.replace(dash,"0")
        nums.append(int(prime, 2))
        for i in range(0, len(indexes)*2-1):
            # Replace dash with a 1
            temp = list(prime)
            temp[indexes[x]] = "1"
            temp = "".join(temp)
            # Store decimal number
            nums.append(int(temp, 2))

            x += 1
            # When x > than the last dash index that index is removed and
            # x is reset. This fills in every zero with a 1
            if x >= len(indexes):
                prime = temp
                indexes.pop()
                x = 0
                
        decimals.append(nums)

    # Extract essential prime implicants
    prime_index = 0
    for d in decimals:
        collisions = []
        for other in decimals:
            if d != other:
                for i in d:
                    for j in other:
                        if i == j:
                            if not i in collisions:
                                collisions.append(i)

        if len(collisions) >= len(d):
            decimals.remove(d)
            primes.pop(prime_index)
            prime_index -= 1
        prime_index += 1

    return primes

# Forms a Boolean Equation from essential
#   prime implicants
# Returns equation
def getEquation(essentials):
    equation = ""
    for i in range(0, len(essentials)):
        letter = 88
        for char in essentials[i]:
            if char == "0":
                equation += chr(letter) + "'"
            elif char == "1":
                equation += chr(letter)
            letter += 1
            if letter == 89:
                letter = 65
        if i < len(essentials)-1:
            equation += " + "
    return equation

# Convert state table to transition table
# Return transition table
def convert(table):
    bnums = []
    for row in table:
        nums = []
        for col in row:

            if len(col) >= digits:
                minterm = states[int(col[digits-1])][0]
            else:
                minterm = col

            # Add 0's for shorter numbers
            if len(minterm) < digits:
                minterm = "0"*((digits)-len(minterm)) + minterm
                
            nums.append(minterm)
        bnums.append(nums)
    return bnums


# Flag for user input
inputting = True
# Store row of table and added to table when full
arr = []
# User prompts for which state they enter
prompts = ["Current State", "Next State when X = 0",
           "Next State when X = 1","Output"]
# Track if inputted all columns
count = 0

# Store data for state table, 2D array
table = [["s0","s0","s1","0"],
         ["s1","s2","s1","0"],
         ["s2","s0","s3","0"],
         ["s3","s2","s1","1"]]

# Store all state assignments, each has a value to use in permutation
states = [["00",1],["01",2],["10",3],["11",4]]


"""print("State Table - Enter all values as decimal numbers\n")
while inputting:
    
    # Prompt user to fill out state Table
    arr.append(int(raw_input("Enter the {0}: ".format(prompts[count]))))
    count += 1
    # Finished row
    if count >= len(prompts):
        table.append(arr)
        arr = []
        count = 0
        answer = raw_input("Add another state?\nEnter 'q' to quit: ")
        if answer.lower() == 'q':
            inputting = False"""

def bestTotal(arr):
    total = 0
    for i in arr:
        total += len(i)
    return total

permutation = True
end = len(states)-1
best = []
bestStates = 0
for i in range(0, len(table[0])-1):
    best.append("x"*(len(table[0])*numVars))
while permutation:
    # Create transmission table from state table and state assignments
    Ttable = convert(table)
    # Find all terms for each equation
    A = []
    B = []
    Z = []
    for row in Ttable:
        #A+ terms
        if row[1][0] == "1":
            A.append("0" + row[0])
        if row[2][0] == "1":
            A.append("1" + row[0])
        #B+ terms
        if row[1][1] == "1":
            B.append("0" + row[0])
        if row[2][1] == "1":
            B.append("1" + row[0])
        #Output terms
        if row[3][1] == "1":
            Z.append("-" + row[0][0] + row[0][1])

    # Sort each array for solving
    A = sortTerms(A)
    B = sortTerms(B)
    Z = sortTerms(Z)

    # Perform Quine McCluskey method and store result
    A = quine(A)
    B = quine(B)
    Z = quine(Z)

    # Extract prime implicants and store result
    A = getPrimeImplicants(A)
    B = getPrimeImplicants(B)
    Z = getPrimeImplicants(Z)

    # Find essential prime implicants and store result
    A = getEssentials(A)
    B = getEssentials(B)
    Z = getEssentials(Z)

    # Show results
    equationA = getEquation(A)
    equationB = getEquation(B)
    equationZ = getEquation(Z)
    print("State Assignments: S0={0}, S1={1}, S2={2}, S3={3}"
          .format(states[0][0],states[1][0],states[2][0],states[3][0]))
    print("A+: " + equationA)
    print("B+: " + equationB)
    print("Z:  " + equationZ)
    print("---------------------------------------------------")

    # Check for smallest equation
    total = len(equationA) + len(equationB) + len(equationZ)
    totalarr = [equationA, equationB, equationZ]
    if total < bestTotal(best):
        bestStates = states
        for i in range(0, len(best)):
            best[i] = totalarr[i]
    
    index = 0
    # Swap last two digits
    temp = states[end]
    states[end] = states[end-1]
    states[end-1] = temp

    # Create transmission table from state table and state assignments
    Ttable = convert(table)
    # Find all terms for each equation
    A = []
    B = []
    Z = []
    for row in Ttable:
        #A+ terms
        if row[1][0] == "1":
            A.append("0" + row[0])
        if row[2][0] == "1":
            A.append("1" + row[0])
        #B+ terms
        if row[1][1] == "1":
            B.append("0" + row[0])
        if row[2][1] == "1":
            B.append("1" + row[0])
        #Output terms
        if row[3][1] == "1":
            Z.append("-" + row[0][0] + row[0][1])

    # Sort each array for solving
    A = sortTerms(A)
    B = sortTerms(B)
    Z = sortTerms(Z)

    # Perform Quine McCluskey method and store result
    A = quine(A)
    B = quine(B)
    Z = quine(Z)

    # Extract prime implicants and store result
    A = getPrimeImplicants(A)
    B = getPrimeImplicants(B)
    Z = getPrimeImplicants(Z)

    # Find essential prime implicants and store result
    A = getEssentials(A)
    B = getEssentials(B)
    Z = getEssentials(Z)

    # Show results
    equationA = getEquation(A)
    equationB = getEquation(B)
    equationZ = getEquation(Z)
    print("State Assignments: S0={0}, S1={1}, S2={2}, S3={3}"
          .format(states[0][0],states[1][0],states[2][0],states[3][0]))
    print("A+: " + equationA)
    print("B+: " + equationB)
    print("Z:  " + equationZ)
    print("---------------------------------------------------")

    # Check for smallest equation
    total = len(equationA) + len(equationB) + len(equationZ)
    totalarr = [equationA, equationB, equationZ]
    if total < bestTotal(best):
        bestStates = states
        for i in range(0, len(best)):
            best[i] = totalarr[i]
    
    
    # Store index of end of group
    last = -1
    for i,e in reversed(list(enumerate(states))):
        if not e[1] > last:
            index = i
            break
        last = e[1]

    # Re-order group
    # Swap first digit with next highest
    least = 999
    index2 = 0
    for i,e in list(enumerate(states[index+1:])):
        # Find next higehst
        if (abs(e[1]-states[index][1]) < least) and e[1] > states[index][1]:
            least = abs(e[1]-states[index][1])
            # Store index
            index2 = i + index + 1

    # Swap
    temp = states[index]
    states[index] = states[index2]
    states[index2] = temp

    # Order other digits
    states[index+1:] = sorted(states[index+1:])      

    # Check for end
    for i,e in reversed(list(enumerate(states))):
        if e[1] > last:
            permutation = False

print("Best Equations")
print("State Assignments: S0={0}, S1={1}, S2={2}, S3={3}"
        .format(states[0][0],states[1][0],states[2][0],states[3][0]))
for b in best:
    print(b)



    
            
