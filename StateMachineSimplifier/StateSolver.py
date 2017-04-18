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
    numsorted = 0
    sorted_bnums = []
    while numsorted < len(arr):
        sorted_bnums.append([])
        for i in range (0, len(arr)):
             if arr[i].count("1") == numsorted:
                sorted_bnums[numsorted].append(arr[i])
           
        numsorted += 1

    # Remove any empty boxes
    limit = len(sorted_bnums)
    count = 0
    while count < limit:
        if len(sorted_bnums[count]) == 0:
            sorted_bnums.pop(count)
            limit -= 1
        else:
            count += 1

    # In case arr only had 1 term return array
    if len(sorted_bnums) <= 1:
        sorted_bnums.append(arr)
    return sorted_bnums

# Variable length
numVars = 3

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


# Flag for user input
inputting = True
# User prompts for which state they enter
prompts = ["Current State", "Next State when X = 0",
           "Next State when X = 1","Output"]
# Track if inputted all columns
count = 0
# Store data for transition table, 2D array
table = [["0","0","1","0"],
         ["1","2","1","0"],
         ["2","0","3","0"],
         ["3","2","1","1"]]
# Store row of table and added to table when full
"""arr = []
print("Transition Table - Enter all values as decimal numbers\n")
while inputting:
    
    # Prompt user to fill out Transition Table
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

# Convert inputted decimal numbers to binary numbers
bnums = []
for row in table:
    nums = []
    for col in row:
        minterm = bin(int(col)).replace("0b","",1)

        # Add 0's for shorter numbers
        if len(minterm) < numVars-1:
            minterm = "0"*((numVars-1)-len(minterm)) + minterm
            
        nums.append(minterm)
    bnums.append(nums)

# Find all terms for each equation
A = []
B = []
Z = []
for row in bnums:
    #A+ terms
    if list(row[1])[0] == "1":
        A.append("0" + row[0])
    elif list(row[2])[0] == "1":
        A.append("1" + row[0])
    #B+ terms
    if list(row[1])[1] == "1":
        B.append("0" + row[0])
    elif list(row[2])[1] == "1":
        B.append("1" + row[0])
    #Output terms
    if row[3][1] == "1":
        Z.append("-" + row[0][0] + row[0][1])

print(Z)
# Sort each array for solving
A = sortTerms(A)
B = sortTerms(B)
Z = sortTerms(Z)

print("Sorted: ")
print(Z)
print("-------------------------------")

# Perform Quine McCluskey method and store result
A = quine(A)
B = quine(B)
Z = quine(Z)

print("Quine: ")
print(Z)
print("-------------------------------")

# Extract prime implicants and store result
A = getPrimeImplicants(A)
B = getPrimeImplicants(B)
Z = getPrimeImplicants(Z)

print("Primes: ")
print(Z)
print("-------------------------------")

# Find essential prime implicants and store result
A = getEssentials(A)
B = getEssentials(B)
Z = getEssentials(Z)

print("Essentials: ")
print(Z)
print("-------------------------------")

# Show results
print(getEquation(A))
print(getEquation(B))
print(getEquation(Z))



    
            
