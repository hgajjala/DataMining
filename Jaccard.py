    
import itertools
from sklearn.metrics import jaccard_similarity_score
with open("C:\General\Big Data\MCS-DS\CS 412 Introduction to DataMining\Assignments\Assignment-4\Files\partitions.csv", "r") as f1:
   
 data1 = f1.readlines()
 

with open("C:\General\Big Data\MCS-DS\CS 412 Introduction to DataMining\Assignments\Assignment-4\Files\clustering_5.csv", "r") as f2:
 
 data2 = f2.readlines()
 

def jaccard(data1, data2):

    n11 = n10 = n01 = 0
    n = len(data1)
    # TODO: Throw exception if len(labels1) != len(labels2)
    for i, j in itertools.combinations(range(n), 2):
        comembership1 = data1[i] == data1[j]
        comembership2 = data2[i] == data2[j]
        if comembership1 and comembership2:
            n11 += 1
        elif comembership1 and not comembership2:
            n10 += 1
        elif not comembership1 and comembership2:
            n01 += 1
    return float(n11) / (n11 + n10 + n01)

print(jaccard(data1, data2))