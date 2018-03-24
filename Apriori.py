"""
Description     : Simple Python implementation of the Apriori Algorithm

Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence

    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""
from __future__ import division
import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
from math import ceil
from copy import copy, deepcopy
lines = []
def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])


def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet


def joinSet(itemSet, length):
        """Join a set with itself and returns the n-element itemsets"""
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])


def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()

    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 1
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


def printResults(items, rules):
    """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
    #for item, support in sorted(items, key=lambda (item, support): support):
    #    print " %.3f : %s" % (support, str(item))
    for item, support in items :
        print support,':',item
    print "\n------------------------ RULES:"
    for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


def dataFromFile(fname):
        """Function which reads from the file and yields a generator"""
        file_iter = open(fname, 'rU')
        for line in file_iter:
                line = line.strip()                        # Remove trailing comma
                record = frozenset(line.split(' '))
                yield record

def part1(fname):
        """Function which reads from the file and yields a generator"""
        categories ={}
        file_iter = open(fname, 'rU')
        global totalCategories
        totalCategories = 0
        for line in file_iter:
                line = line.strip()                        # Remove trailing comma
                totalCategories += 1
                record = frozenset(line.split(' '))
                for e in record:
                    
                    if  e not in categories:
                        categories[e]=1
                    else:
                        categories[e]+=1
        
        for e, v in categories.items():
            if( v >= minSupport):
                print v,':',e
        

def printfile(fname):
        """Function which reads from the file and yields a generator"""
        categories ={}
        file_iter = open(fname, 'rU')
        global totalCategories
        totalCategories = 0
        for line in file_iter:
                line = line.strip()                        # Remove trailing comma
                totalCategories += 1
                record = line.split(' ')
                size = record.__len__()
                orderedarray =[size ]
                orderedarray[0] = record.__getitem__(size-1)
                i =0
                for x in range(0,(size-1)):
                    orderedarray.append(record[x])
                    i+=1
                
                for y in range(0,size) :
                    if(y == 0) :
                        z = orderedarray[y] +':'
                    elif (y < (size-1)):
                        z = orderedarray[y] +';'
                    else:
                        z = orderedarray[y]
                    print z,    
                    
                print '\t'

def readFile(file):
    
    file_iter = open(file, 'rU')
    corpus =[]
     
    for line in file_iter:
        line = line.strip()                        # Remove trailing comma
        record = line.split(' ')
        lines.append(line)
        for e in record:            
            corpus.append(e)
    tlines = len(lines)
    return corpus

def findInLines(phrase, support):
    count=0
    for l in lines:
        occurences = l.count(phrase)
        if occurences >= 1:
            count +=1
    if count >= support:
        return True
    


def fpd(file, support):
    f = dict()
    index = dict()
    c = readFile(file)
    length = len(c)
    rejected = list()
    for i in range(0,length-1):
        if c[i] not in index.keys():
            index[c[i]] = set()
            index[c[i]].add(i)
        else:
            index[c[i]].add(i)        
    
    while bool(index):
        indexprime = dict()

        for u in index.keys():
            s = len(index[u])
            if s >= support :
                f[u] = s
                for j in index[u] :
                    up=""
                    if j != length -1:
                        up = u + " " + c[j+1]
                    else:
                        continue

                    if up not in rejected:
                        if up not in indexprime.keys():
                            if findInLines(up,support):
                                indexprime[up] = set()
                                indexprime[up].add(j+1)
                            else:
                                rejected.append(up)
                        else:
                            indexprime[up].add(j+1)
        index.clear()
        index = deepcopy(indexprime)
    return f
    


if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    minSupport = options.minS
    minConfidence = options.minC

    inFile = None
    if options.input is None:
            inFile = sys.stdin
    elif options.input is not None:
                           
 #       part1(options.input)
 #      printfile(options.input)
        f =  fpd(options.input,minSupport)
        for k in f.keys():
            for l in lines:
                occurences = l.count(k)
                if occurences > 1:
                    occurences -=1
                    f[k] -= occurences 
    
                
        for k, v in f.items():
            if v >= minSupport:
                print v,':',
                words = k.split(' ')
                for w in words:
                    print w,';',

            print "\t"
 #       inFile = dataFromFile(options.input) 
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')


  #  items, rules = runApriori(inFile, minSupport, minConfidence)

    #printResults(items, rules)
