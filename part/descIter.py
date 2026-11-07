import sys
def uniquePartitions(n):
    ans = []
    p = [0] * n
    k = 0
    p[k] = n
    
    while True:
        ans.append(p[:k + 1].copy())
        
        remVal = 0
        # Finde das rechtsste Element > 1
        while k >= 0 and p[k] == 1:
            remVal += p[k]
            k -= 1
            
        if k < 0:
            break
            
        p[k] -= 1
        remVal += 1
        
        # Verteile den Rest auf gleich große Teile
        while remVal > p[k]:
            p[k + 1] = p[k]
            remVal -= p[k]
            k += 1
        p[k + 1] = remVal
        k += 1
        
    return ans   


# n = 65
n = int(sys.argv[1])

print(uniquePartitions(n))
