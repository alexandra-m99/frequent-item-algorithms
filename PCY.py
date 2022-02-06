#COMP 4250 Project 1
#Name: Alexandra Murphy
#ID: 104757431
#-----------------------------
import time
import itertools
from collections import Counter

#begins timing program
start = time.time()

num_of_baskets = 88162
supp_percent = 0.1
ds_percent = 1
k = 9883
hash_bucket = {}

#dividing the dataset into different chunks and calculate support
dataset = ds_percent*num_of_baskets
dataset = round(dataset)
support = supp_percent*dataset
support = round(support)

#PASS 1
#--------
#Create the baskets from txt file and cycle through baskets and keep count of all items
singletons = {}
basket_items = {}
basket_list = []
with open("retail.txt") as input_file:
    for i in range(dataset):
        basket = next(input_file).strip().split()
        for b in basket:        #cycle through basket to count each item
            if(b in singletons.keys()):
                singletons[b]+=1
            else:
                singletons[b] = 1
        basket_pairs = list(itertools.combinations(basket,2))   #find pairs in basket

        for b in basket_pairs:  #cycle through basket to count pairs
            if(b in basket_items.keys()):
                basket_items[b]+=1
            else:
                basket_items[b] = 1;
        basket_list.append(basket)

#initialize the hashing bucket table
for i in range(k):
    hash_bucket[i] = 0;

#hash pairs to buckets 
for c in basket_items:
    hash_function = ((int(c[0]))*(int(c[1])))%k
    hash_bucket[hash_function]+=basket_items[c]
    basket_items[c] = hash_function

#Between Pass 1 and Pass2
#-------------------------
#replacing buckets with bit vector (1 = frequent, 0 = not frequent)
for i in hash_bucket:
    if(hash_bucket[i] >= support):
        hash_bucket.update({i:1})
    else:
        hash_bucket.update({i:0})

#Find C2 and add to list for Pass 2
C2_list = []
count = 0
for c in basket_items:
    if(hash_bucket[basket_items[c]] == 1): #only add to C2 if value in bit vector is 1
        if(c[0] in singletons and c[1] in singletons): #check that both items in pair are frequent on their own
            C2_list.append(c)
            count+=1
print("There are", count, "candidate pairs.\n") 

#PASS 2
#--------
pair_occurence = {}
C2_count = Counter(C2_list)
#use Counter to count pair occurences in C2
for pair, count in C2_count.items():
    pair_occurence.update(Counter({pair:count}))

#Cycle through baskets in list to create pairs and count the occurences
for b in basket_list:
    pairs = set(itertools.combinations(b,2))
    for p in pairs:
        if(p in pair_occurence.keys()):
            pair_occurence[p]+=1

#create list to further prune pairs that appear less than support
prune = []
for i in pair_occurence:
    if(pair_occurence[i] < support):
        prune.append(i)
        
#remove pairs that appear in the prune list - these will not be counted as frequent
for i in prune:
    del pair_occurence[i]
 
#print occurence of each frequent pair
for key, value in pair_occurence.items():
    print("Pair", key, "occurs", value, "times.");

#stops timing program
print("\nProgram Run Time:", round(time.time() - start,2), "seconds.")
