#COMP 4250 Project 1
#Name: Alexandra Murphy
#ID: 104757431
#-----------------------------
import time
import itertools
from collections import Counter

#start timing program
start = time.time()

num_of_baskets = 88162
supp_percent = 0.1
ds_percent = 1

#dividing the dataset into different chunks and calculate support
dataset = ds_percent*num_of_baskets
dataset = round(dataset)
support = supp_percent*dataset
support = round(support)

print("\nThe dataset is", dataset, "baskets.")
print("The support is", round(supp_percent*100), "% of dataset -> Counting pairs that appear in at least", support, "baskets.")
print("\nC1: All integers from the retail.txt file.")

#Create a list of integers from the txt file
singletons = []
with open("retail.txt") as input_file:
    for i in range(dataset):
        line = next(input_file).strip()
        singletons.append(line.split())

#generate C1 from file list above
C1_list = []
for i in singletons:
    for j in i:
        C1_list.append(j)

#uses Counter to count all singletons from C1 and their occurence but only if the count is greater than or equal to support, as the other items are not needed
C1_count = Counter(C1_list)
item_occurence = {}
for itm, count in C1_count.items():
    if(count >= support):
        item_occurence.update(Counter({itm:count}))

#Creates the L1 list based on the item occurence 
L1_list = [i for i in item_occurence.keys()]
print("\nL1: ", L1_list)

#Creates the possible pairs from L1 in order to generate C1
candidate_pairs = list(itertools.combinations(L1_list,2))

#initialize list C2 to hold all the candidate pairs and keep count of occurences
C2_list = []
count = 0
for i in singletons:
    for j in candidate_pairs:
        if((j[0] in i) and (j[1] in i)):
            C2_list.append(j)
            count+=1
print("\nC2: There are ", count, " candidate pairs.")

#uses Counter to keep count of each pair from C2 and to count and keep occurrence of pairs only if >= support
C2_count = Counter(C2_list)
pairs_occurence = {}
for pair,count in C2_count.items():
    if(count >= support):
        pairs_occurence.update(Counter({pair:count}))

print("\nL2:")
for key, value in pairs_occurence.items():
    print("Pair", key, "occurs", value, "times.")

#Create the L2 list with all frequent pairs as generated from Counter and count frequent pairs
count = 0
L2_list = []
for i in pairs_occurence.keys():
    L2_list.append(i)
    count+=1

print("\nThere are", count, "frequent pairs.")
print("\nProgram Run Time:", round(time.time()-start,2), "seconds.")
