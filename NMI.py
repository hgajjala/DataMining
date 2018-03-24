    
from sklearn.metrics.cluster import normalized_mutual_info_score
with open("C:\General\Big Data\MCS-DS\CS 412 Introduction to DataMining\Assignments\Assignment-4\Files\partitions.csv", "r") as f1:
   
 data1 = f1.readlines()
 

with open("C:\General\Big Data\MCS-DS\CS 412 Introduction to DataMining\Assignments\Assignment-4\Files\clustering_5.csv", "r") as f2:
 
 data2 = f2.readlines()
 
 

print (normalized_mutual_info_score(data1, data2))
