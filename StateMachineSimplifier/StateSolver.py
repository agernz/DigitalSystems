import platform
import os
"""Quine McCluskey Algorithim
    Adam Gernes
"""

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

# Input number of variables
numVars = 4#int(input("Enter the number of Variables: "))

# Input minterms
numMin = "8"#input("How many minterms do you need to enter?: ")
tempnums = [0,2,3,6,8,9,12,13]
bnums = []
for i in range (0, int(numMin)):
    minterm = tempnums[i]#input("Enter minterm: ")

    # Convert minterm to binary
    minterm = bin(int(minterm)).replace("0b","",1)

    # Add 0's for shorter numbers
    if len(minterm) < numVars:
        minterm = "0"*(numVars-len(minterm)) + minterm
    
    bnums.append(minterm)

# Sort into groups based on # of 1's
numsorted = 0
sorted_bnums = []
while numsorted < len(bnums):
    sorted_bnums.append([])
    for i in range (0, len(bnums)):
         if bnums[i].count("1") == numsorted:
            sorted_bnums[numsorted].append(bnums[i])
       
    numsorted += 1


# Remove empty boxes
limit = len(sorted_bnums)
count = 0
while count < limit:
    if len(sorted_bnums[count]) == 0:
        sorted_bnums.pop(count)
        limit -= 1
    else:
        count += 1

# Do each Column
index_col = 0
cols = []
primes = []
cols.append(sorted_bnums)

# Repeat until only one box in column
while len(cols[index_col]) > 2:
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
                    b = cur_box[i][:4]
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

# Extract prime implicants
for i in range(0, len(cols)):
    for x in range(0, len(cols[i])):
        for y in range(0, len(cols[i][x])):
            implicant = cols[i][x][y]
            if not implicant.endswith("*"):
                # Do not add duplicats
                if not implicant in primes:
                    primes.append(cols[i][x][y])


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

# Form Equation
equation = ""
for i in range(0, len(primes)):
    letter = 65
    for char in primes[i]:
        if char == "0":
            equation += chr(letter) + "'"
        elif char == "1":
            equation += chr(letter)
        letter += 1
    if i < len(primes)-1:
        equation += " + "

print(equation)
    
            
