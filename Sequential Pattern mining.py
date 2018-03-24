from collections import Counter
from collections import defaultdict

def fpd(C, support):
	f = Counter()
	n = len(C)
	index = defaultdict(set)
	for i in range(n):
		index[C[i]].add(i)

	while index:
		indexp = defaultdict(set)
		for u in index:
			if len(index[u]) >= support:
				f[u] = len(index[u])
				for j in index[u]:
					if j + 1 < n:
						up = u + " " + C[j+1]
						index[up].update(index[u].add(j+1))
		index = indexp
	return f