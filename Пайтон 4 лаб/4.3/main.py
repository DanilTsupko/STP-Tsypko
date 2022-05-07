data = [set(open(i).read().split()) for i in ('Avr1.txt', 'Avr2.txt')]
diff = data[0].difference(data[1])
if diff:
    print(diff)
else:
    print('Не існує різниці ')