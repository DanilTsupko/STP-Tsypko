import random
list = [random.randrange(0,50)for _ in range(20)]
list1= list
print(list)
#### 5 min elementov
list.sort()
print("min element" , *list[:5])
#### 5 max elementov
list.sort()
print("max element" , *list[-5:])
### index
ind = min(list)
print(list.index(ind) + ind)
print(list1[0:])## випадково по зростаню
## sort
list.sort()
print('Сортування' , list)
## sered aref
print ('sered aref' ,  sum(list)/len(list))


