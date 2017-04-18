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
numVars = int(input("Enter the number of Variables: "))

# Input minterms
numMin = input("How many minterms do you need to enter?: ")
bnums = []
for i in range (0, int(numMin)):
    minterm = input("Enter minterm: ")

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
                    b = list(cur_box[i])
                    # Remove * to avoid stacking of *s
                    if cur_box[i].endswith("*"):
                        b.pop()

                    b[diffi] = "-"

                    # Only add if not in array
                    if not "".join(b) in arr:
                        arr.append("".join(b))
                        
                    # Mark values as used if not already marked
                    if not cur_box[i].endswith("*"):
                        cur_box[i] += "*"
                    if not next_box[x].endswith("*"):
                        next_box[x] += "*"

        cols[index_col+1].append(arr)

    index_col += 1

clear_screen()
for i in range(0, len(cols)):
    print("-----------------")
    print("|    Column {0}    |".format(i+1)) 
    print("-----------------")
    for x in range(0, len(cols[i])):
        for y in range(0, len(cols[i][x])):
            print(cols[i][x][y])       
        print("-----------------") 
