# recommendation-engine

A simplified version of the A-Priori **a**ssociation **r**ule **min**ing algorithm, in Python. Hence, `armin.py`. 

`python3 armin.py input_filename output_filename min_support_percentage min_confidence`

where:
* `input_filename` is the name of the file that contains market basket data. The format for the input file is provided below. A sample file `input.txt` is provided together with this repository.  

## A-Priori Algorithm

The A-Priori algorithm utilizes the subset property for frequent itemsets, enabling significant pruning of the space of possible itemset combinations. Assuming a provided min support percentage and a min confidence, the i-th step of the algorithm works as follows:

**Step i:**  

• Consider all the candidate frequent itemsets of size i. Let’s name them CFI(i).  
• Count how many times each itemset in CFI(i) appears in our input data. This is the support count,
which is turned into the support percentage by dividing with the total number of transactions.  
• The itemsets in CFI(i) whose support percentage is at least as much as the min support percentage
become the verified frequent itemsets, or VFI(i).  
• Using itemsets in VFI(i) generate all plausible candidate itemsets of size +1, i.e., CFI(i + 1). This makes use of the subset property. For example, for ABC to be in CFI(3), all of AB, BC, and AB need to be in VFI(2).  

This process starts with CFI(1) being all individual items and terminates on Step k, when CFI(k + 1) is empty. 

The above process generates all the frequent itemsets, i.e., VFI(i), for 1 <= i <= k. For every frequent itemset we need to generate all possible association rules and keep only the rules whose support is greater or equal to the min support percentage and their confidence is greater or equal to the min confidence. To generate all possible rules from a frequent itemset, we generate all possible 2-partitions of the itemset (one will be the left-hand-side of the association rule and the other will be the right-hand-side), where neither partition is empty. For example, if {A,B,C} is a frequent itemset, then we should check the following association rules:  

* A=>B,C  
* B=>A,C  
* C=>A,B  
* A,B=>C  
* A,C=>B  
* B,C=>A 

and compute their support and confidence. Note that the support of all these rules is the same as the support of the frequent itemset from which they came, i.e., {A,B,C}.

---

> **Input Format:** The input data should be provided as a CSV file, in the following format:  
`transaction_id, item_1, item_2, item_3, ...`   
> for example: 
```
1, A100, A105, A207  
2, A207  
3, A100, A105  
```
> Notes:  
> * Item names could consist of either numbers (0-9) or characters (a-zA-z) or combinations of numbers and characters. No spaces or puncuation characters are allowed in item names.   
> * The CSV files may or may not contain whitespace between values.

* `output_filename` is the name of the file that stores the required output of the program. The file contains the frequent item sets and the association rules that the engine discovered after processing the submitted input data.

> **Output Format:** The output data is provided as a CSV file, where every row is in one of the following formats:  
`S, support_percentage, item_1, item_2, item_3, ...`  
> to denote that this is a frequent item**s**et or:  
`R, support_percentage, confidence, item_4, item_5, ..., ’=>’, item_6, item_7, ...  `  
> to denote that this is an association **r**ule. The keys "S" and "R" are verbatim and no other substitution is needed. 
> It should be noted that the items listed in the frequent itemset case (item 1, item 2, item 3, ...) should be in lexicographic order, the items listed to the left of the => sign in the association rule case (item 4, item 5, ...) should be in lexicographic order and so should the items listed in the right size of the => sign in the association rule case (item 6, item 7, ...).  
> The `support_percentage` should be the support percentage (expressed as a floating number between 0 and 1 with 4 decimal points) for the specific frequent itemset or for the specific association rule (and both should be above the user-specified min_support_percentage).  
> The `confidence` should be the confidence percentage (expressed as a floating number between 0 and 1 with 4 decimal points) for the specific association rule (and should be above the user-specified min_confidence).  
> You should list in the output file all the frequent itemsets that you discover in the input file (S) and all the association rules that you can generate using the A-Priori method (R), that satisfy the min support percentage and min confidence requirements.  
>
> Here’s an example output file:
```
S, 0.3000, A105 
S, 0.2500, A100 
S, 0.2000, A100, A207
S, 0.2000, A105, A207
S, 0.1500, A100, A105, A207
R, 0.1500, 0.5000, A105, ’=>’, A100, A207
```

> The repository contains three output files as follows:  

| Input Filename | Output Filename | Minimum Support Percentage | Minimum Confidence |  
| --- | --- | --- | ---  |  
| input.csv | output.sup=0.5,conf=0.7.csv | 0.5 | 0.7 |  
| input.csv | output.sup=0.5,conf=0.8.csv | 0.5 | 0.8 |  
| input.csv | output.sup=0.6,conf=0.8.csv | 0.6 | 0.8 |  


* `min_support_percentage` is the minimum support percentage for an itemset / association rule to be considered frequent, e.g., 5%. 
    
* `min_confidence` is the minimum confidence for an association rule to be significant, e.g., 50%. 

An example call to the program:  
`python3 armin.py input.csv output.csv 0.5 0.7`

