
import sys
from itertools import chain, combinations
from collections import defaultdict

# --- GET INPUT DATA ---
def generateData(INPUT_FILENAME): # reads from the file, yeilds a generator
    file_iter = open(INPUT_FILENAME, 'r')
    for line in file_iter:
        line = removeTID(line)
        record = frozenset(line.split(','))
        yield record

def removeTID(line):
    line = line.strip().rstrip(',')  # Remove trailing comma if exists and new line character
    line = line.split(',') # turn to list 
    line.remove(line[0]) # removing TID (first elements of the list)
    line = ','.join(line) # turn back to string
    return line

def getUniqueItemsetANDTransactions(data_iterator):
    transactions = list()
    unique_items = set()
    for record in data_iterator: # for every "line"
        current_transaction = frozenset(record) # use frozen set so that items are not immutable -> ORDER IS NOT GUARANTEED TO BE PRESERVED! 
        transactions.append(current_transaction) # add current to the list of transactions
        for item in current_transaction:
            unique_items.add(frozenset([item])) 
    return unique_items, transactions

### --- CORE ALGORITHM ---
def runApriori(data_iter, min_support_percentage, min_confidence):

    itemset, transactions = getUniqueItemsetANDTransactions(data_iter) # getting the data from the input
    master_itemset = dict() # master dict (k: number of items in the itemset, v: set of the itemsets)
    frequent_itemsets = defaultdict(int) # (k: itemsets, v: support count); will be populated inside a function; would initialize to 0
    candidate_itemset_size_one = returnItemsWithMinSupport(itemset, transactions, min_support_percentage, frequent_itemsets) # populates one item itemsets and counts in frequent_itemsets

    candidate_itemsets = candidate_itemset_size_one
    k = 2 # start with 2 because do refer to k - 1 (one item itemset)
    while(candidate_itemsets != set([])): # while did not reach the end
        master_itemset[k-1] = candidate_itemsets # add verified to the master itemsets
        candidate_itemsets = joinSet(candidate_itemsets, k) # join with itself to get candidate for itemset of the length one bigger
        verified_itemsets = returnItemsWithMinSupport(candidate_itemsets, transactions, min_support_percentage, frequent_itemsets) # verify the itemsets from the candidate one
        candidate_itemsets = verified_itemsets # new candidate are verified (to write back to master on a new iteration)
        k = k + 1

    #printMasterItemset(master_itemset)
    
    final_items = [] # holds items (tuple, support percentage)
    for n, length_N_itemsets in master_itemset.items(): # adding every itemset + its support percentage to the final set
        final_items.extend([(tuple(item), getSupportPercentage(item, frequent_itemsets, transactions)) for item in length_N_itemsets]) # using extend because want to add every individual item

    final_rules = [] # holds rules (itemset_left, itemset_right), confidence)
    for itemset_length, itemsets in list(master_itemset.items())[1:]: # keys start from 1 sized items
        for item in itemsets: # for each item (tuple) in the set of itemsets 
            local_subsets = map(frozenset, [subset for subset in getSubsets(item)]) # creating a frozenset of all the subsets for the item
            #print(list(local_subsets))
            for current_subset in local_subsets: # current_subset -> itemset_left
                remain = item.difference(current_subset) # in item but not in the current subset -> itemset_right
                #print("item", item, "current subset", current_subset, "remain", remain)
                if len(remain) > 0: # if there is a difference, then get the confidence
                    confidence = getSupportPercentage(item, frequent_itemsets, transactions)/getSupportPercentage(current_subset, frequent_itemsets, transactions)
                    if confidence >= min_confidence: # take only the ones tha pass the test (min_confidence)
                        final_rules.append(((tuple(current_subset), tuple(remain)), confidence))

    return final_items, final_rules


### --- LOGISTICS HELPER FUNCTIONS ---
def joinSet(itemset, length): # Joins a set (itemset from args) with itself (using union) and returns the n-element itemsets (spesified by length args)
    return set([current_item.union(another_item) for current_item in itemset for another_item in itemset if len(current_item.union(another_item)) == length])

def returnItemsWithMinSupport(itemset, transactions, min_support_percentage, frequent_itemsets): # calculates the support percentage for items in the itemset; returns a subset of the itemset (items satisfy minimim support percentage)
    min_support_itemsets = set() # holds itemsests that meet min support threshold
    local_itemsets_counts = defaultdict(int) # k: itemset, v: count; calculated counts for n-item itemsets

    for current_item in itemset: # # calculates counts (for local and semi-global); itemset is an n-item itemset
        for current_transaction in transactions: # a list of transactions
                if current_item.issubset(current_transaction): # if item was bought, increase count
                        frequent_itemsets[current_item] += 1 # populate the main frequent itemset; initializes to 0 at first and then adds 1
                        local_itemsets_counts[current_item] += 1 # populate the local_itemsets_counts

    for current_item, count in local_itemsets_counts.items(): # populates min_support_itemsets
        support_percentage = float(count)/len(transactions) # calculates current support percentage
        if support_percentage >= min_support_percentage: # compare if meet the threshold
                min_support_itemsets.add(current_item) # take only those that meet the threshold

    return min_support_itemsets

def getSupportPercentage(item, frequent_itemsets, transactions): # returns the support percentage for an item
    support_count = frequent_itemsets[item]
    transactions_total = len(transactions)
    return float(support_count / transactions_total) 

def getSubsets(input_array): # Returns subsets of arr (using itertools lib)
    return chain(*[combinations(input_array, i + 1) for i, a in enumerate(input_array)])

def getUnionSupport(item, itemset_left, itemset_right): # gets the support for union to output for rules; a separate function because don't store support counts globally
    union = tuple(sorted(set(itemset_left).union(set(itemset_right)))) # make a union out of 2 sides of the rule; sort for comparison; set to tuple so that can compare
    for item, support in sorted(items): # contain support counts
        item = tuple(sorted(item)) # sort for comparison
        if item == union: # if found a set corresponding to union
            support_union = support # get the support for the union
    return support_union # return the support percentage for the union

### --- OUTPUT ---
def outputResults(items, rules):
    OUTPUT_FILENAME = sys.argv[2]
    output_file = open(OUTPUT_FILENAME, 'a') # open file to append

    # WRITE SUPPORTT PERCENTAGES
    items = [(tuple(sorted(tpl)), flt) for tpl, flt in items] # sort tuples within and reassign (because tuples are immutable)
    for item, support in sorted(sorted(items), key=lambda x: len(x[0])): # sort as much as possible + by the number of values 
        output_file.write(writeSetToOutputFile(support, sorted(item)) + '\n') # write to the file the returned string
        
    # WRITE RULES
    for rule, confidence in sorted(sorted(rules), key=lambda x: len(x[0])): # sort as much as possible
        itemset_left, itemset_right = rule # let each side of the rule
        support_union = getUnionSupport(item, itemset_left, itemset_right) # get the union to calculate the support
        output_file.write(writeRuleToOutputFile(support_union, confidence, itemset_left, itemset_right) + '\n') # write to the file the returned string

    output_file.close() # close the output file

# --- OUTPUT HELPER FUNCTIONS
def writeSetToOutputFile(support_percentage, itemset): # returns a formatted string for support percentage entry
    output_line = ",".join(['S', str(support_percentage), ','.join([str(item) for item in itemset])])
    print(output_line)
    return output_line   

def writeRuleToOutputFile(support_count, confidence,  itemset_left, itemset_right): # returns a formatted string for rule entry
    formatted_confidence = "{0:.4f}".format(confidence) # format confidence to have 4 digits after the dot
    output_line = ",".join(['R', str(support_count), str(formatted_confidence), ','.join([str(item) for item in sorted(itemset_left)]), "'=>'", ','.join([str(item) for item in sorted(itemset_right)])])
    print(output_line)
    return output_line

# DEBUG FUNCTIONS
def printMasterItemset(itemset):
    for n, items in itemset.items():
        for item in items:
            print(item)

def printItemset(itemset):
    for items in itemset:
        print(items)

### --- MAIN ---
if __name__ == "__main__":

    INPUT_FILENAME = sys.argv[1] # getting args
    OUTPUT_FILENAME = sys.argv[2]
    MIN_SUPPORT_PERCENTAGE = float(sys.argv[3])
    MIN_CONFIDENCE = float(sys.argv[4])

    input_file = generateData(INPUT_FILENAME)

    items, rules = runApriori(input_file, MIN_SUPPORT_PERCENTAGE, MIN_CONFIDENCE)
    outputResults(items, rules)