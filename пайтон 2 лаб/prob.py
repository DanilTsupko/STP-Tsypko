import random
x = ['a', 'a', 'a', 'f', 'h', 'k', 'k', 1]
r = [x[0]]
i = 1
j = 0
while i < len(x):
    if r[j] != x[i]:
        r.append(x[i])
        j += 1
    i += 1
#print (r)


list = [random.randint(0,30) for _ in range(20)]
print(list)