'''
C1- candidate set one
    I1: 6
    I2: 4
    ...
L1- C1 but filtered with min support count

1. Generate C1
2. Generate L1
3. Generate C2 (Ck) by taking all combinations from L1 (Lk-1)
    [I1, I2]
    ...
4. Get the count of all elements in Ck
5. Compare with min support to get Lk
6. Repeat till no new Ck can be formed
'''

from itertools import combinations

def load_data(filename):
    transactions = []
    with open(filename, 'r') as file:
        next(file)  # Skip the header line
        for line in file:
            parts = line.strip().split(",")
            items = parts[1:]  # Get all items after TID
            transactions.append(items)
    return transactions

def get_frequent_1_itemsets(transactions, min_sup):
    # Count occurrences of each item
    item_counts = {}
    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
    
    # Filter items based on min support
    L1 = {}
    for item, count in item_counts.items():
        if count >= min_sup:
            L1[frozenset([item])] = count # frozenset because it's immutable, so can be used as dictionary key
    return L1

def apriori_gen(Lk_minus_1, k):
    # Generate candidate k-itemsets from (k-1)-itemsets
    Ck = []
    items = list(Lk_minus_1)
    
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            l1 = list(items[i])
            l2 = list(items[j])
            
            l1.sort()
            l2.sort()

            # Join step: combine sets if they match in the first (k-2) elements
            '''
            Apriori principle- If an itemset is frequent all its subsets are also frequent
            '''
            if l1[:k-2] == l2[:k-2]:
                candidate = frozenset(l1) | frozenset(l2)

                # Prune step: check if all (k-1)-subsets of the candidate are in Lk_minus_1
                if has_infrequent_subset(candidate, Lk_minus_1):
                    continue
                
                Ck.append(candidate)
    
    return Ck

def has_infrequent_subset(candidate, Lk_minus_1):
    # Check if candidate has any (k-1)-itemset not in Lk_minus_1
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in Lk_minus_1:
            return True
    return False

def generate_frequent_itemsets(transactions, min_sup):
    # Generate L1, the 1-item frequent itemsets
    L = []
    Lk = get_frequent_1_itemsets(transactions, min_sup)
    L.append(Lk)
    
    k = 2
    while Lk:
        # Generate candidate itemsets Ck
        Ck = apriori_gen(Lk, k)
        
        # Count occurrences of each candidate itemset in transactions
        candidate_counts = {c: 0 for c in Ck}
        
        for transaction in transactions:
            transaction_set = frozenset(transaction)
            for candidate in Ck:
                if candidate.issubset(transaction_set):
                    candidate_counts[candidate] += 1
        
        # Filter candidates to create the next level of frequent itemsets Lk
        Lk = {c: count for c, count in candidate_counts.items() if count >= min_sup}
        
        if Lk:
            L.append(Lk)
        
        k += 1
    
    return L

# Set the minimum support
min_sup = 2

# Load data and generate frequent itemsets
filename = "apriori.txt"  
transactions = load_data(filename)
frequent_itemsets = generate_frequent_itemsets(transactions, min_sup)

# Print the frequent itemsets
for level, itemsets in enumerate(frequent_itemsets, start=1):
    print(f"Frequent {level}-itemsets:")
    for itemset, count in itemsets.items():
        print(f"{list(itemset)}: {count}")