import sys
def get_partitions(n, max_val=None):
    if max_val is None:
        max_val = n
    
    result = []
    current = []
    
    def backtrack(remaining, max_val):
        if remaining == 0:
            result.append(list(current))
            return
        
        # Versuche Summanden von max_val bis 1
        for i in range(min(remaining, max_val), 0, -1):
            current.append(i)
            backtrack(remaining - i, i) # Nächster Summand darf nicht größer sein
            current.pop()
            
    backtrack(n, max_val)
    return result

# Beispiel: Alle Partitionen von 4
n = int(sys.argv[1])
print(get_partitions(n))
# Ausgabe: [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]]   
