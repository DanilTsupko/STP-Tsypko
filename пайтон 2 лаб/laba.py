import random

print("СОРТУВАННЯ")
def List_sort (list):
    list = [random.randrange(0, 50) for _ in range(20)]
    list1=list
    print(list1)
    list.sort()
    print(list)
List_sort(list)
print('')
##Za znacheniam
print("За послідовністю")
def List_pos(list):
    list = ([random.randrange(0, 50) for _ in range(20)])
    list.sort(reverse=True)
    print(list)
List_pos(list)
## list min
print('')
print("Мінім елемент")
def List_min(list):
    list = [random.randrange(0, 50) for _ in range(20)]
    print(list)
    list.sort()
    print("min element", *list[:5])
List_min(list)
## list max
print('')
print("Макселемент")
def List_max(list):
    list = [random.randrange(0, 50) for _ in range(20)]
    print(list)
    list.sort()
    print("min element", *list[-5:])
List_max(list)
print('')
print('Серд ареф')
def List_serArf(list):
    list = [random.randrange(0, 50) for _ in range(20)]
    print(list)
    print('Середнє арф' , sum(list)/len(list))
List_serArf(list)
print('')
## bez povtor
print('Список без повтору')
def List_BezPov(list):
    list = [random.randrange(0, 5) for _ in range(5)]
    print('Початковий (можливе повторення)' ,  list)
    list1 = set(list)
    print(list1)
List_BezPov(list)

print('Виклик елемента ')
def posh_elemen(list):
 a = [random.randrange(0,50) for _ in range(10)]
 print (a)
 if 5 in a :
     print("Число (5) є в списку ")
 else :
     print("Числа (5) немає")

posh_elemen(list)


