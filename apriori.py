from collections import defaultdict
import time

def create_initial(item_map, minimum_support):
    n = len(item_map)
    itemset = []
    for item in item_map.keys():
        transaction = item_map[item]
        c = len(transaction)
        support = 1.0 * c / n
        if support > minimum_support:
            iso = {'items': set([item]), 'set': transaction, 'count': c, 'support': support}
            itemset.append(iso)
    return itemset

def apriori_gen(itemsets, k):
    next_set = []
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            items1 = itemsets[i]['items']
            items2 = itemsets[j]['items']
            items3 = items1.union(items2)
            if len(items3) == k+1:
                next_set.append(items3)
    return next_set

def all_matches(itemsets, transaction):
    matches = []
    unique_check = {}
    for itemset in itemsets:
        iset = itemset.intersection(transaction)
        if len(iset) == len(itemset):
            key = str(sorted(list(iset)))
            try:
                unique_check[key] += 1
            except KeyError:
                unique_check[key] = 0
                matches.append(iset)
    return matches

def apriori(transactions, minimum_support, verbose=False):
    itemsets = []
    item_map = defaultdict(set)
    for t, elements in enumerate(transactions):
        for element in elements:
            item_map[element].add(t)
    s = time.time()
    L_1 = create_initial(item_map, minimum_support)
    itemsets.append(L_1)
    if verbose:
        print 'create initial:', time.time() - s, len(itemsets[0])
    k = 1
    lt = len(transactions)
    while len(itemsets[k-1]) > 0:
        s = time.time()
        C_k = apriori_gen(itemsets[k-1], k)
        occurance = {}
        max_count = 0
        for itemset in C_k:
            matches = set()
            for i, item in enumerate(itemset):
                tmatches = item_map[item].copy()
                if i==0:
                    matches = tmatches
                else:
                    matches = matches.intersection(tmatches)
            if len(matches) > 0:
                name = str(itemset)
                c = 1.0 * len(matches)
                occurance[name] = {'items': itemset, 'set': itemset, 'count': c, 'support': c / lt}
        L_k = []
        for itemset, iso in occurance.items():
            if iso['support'] > minimum_support:
                L_k.append(iso)
        itemsets.append(L_k)
        if verbose:
            print 'Iteration #', k, time.time() - s
        k += 1
    s = time.time()
    ret = [item for sublist in itemsets for item in sublist]
    return ret
