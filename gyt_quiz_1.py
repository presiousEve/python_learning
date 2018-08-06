# Written by Yuting GUO and Eric Martin for COMP9021
#!/usr/bin/env python


import sys
from random import seed, randrange
from collections import Counter

try:
    arg_for_seed = int(input('Enter an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
x = randrange(10 ** 10)
sum_of_digits_in_x = 0 

L = [randrange(10 ** 8) for _ in range(10)]
first_digit_greater_than_last = 0
same_first_and_last_digits = 0
last_digit_greater_than_first = 0

distinct_digits = [0] * 9

min_gap = 10
max_gap = -1

first_and_last = set()

#---------------------------funtion1--------------------------------------
a = x
i = 0
Lx = []

while i < 10:
	Lx.append(a % 10)
	#Lx[i] = a % 10
	#can not use this^
	a = a // 10
	i = i + 1

Lx.reverse()#return turn around the list, do not need =
sum_of_digits_in_x = sum(Lx)

#--------------------------funtion2---------------------------------------
first = []
last = []
i = 0
while i < 10:
    first.append(L[i] // (10 ** (len(str(L[i])) - 1)))#list中整数的长度
    last.append(L[i] % 10)
    i = i + 1

#first.reverse()
#last.reverse()

j = 0
while j < 10:
    if first[j] > last[j]:
        first_digit_greater_than_last = first_digit_greater_than_last + 1
    elif first[j] == last[j]:
        same_first_and_last_digits = same_first_and_last_digits + 1
    elif first[j] < last[j]:
        last_digit_greater_than_first = last_digit_greater_than_first + 1
    j = j + 1

#------------------------------------funtion3---------------------------------
list_L = []
for i in L:
	list_L.append({v for v in str(i)})
#print (L3)

list_count = []
for i in list_L:
	list_count.append(len(i))#len是记元素个数，如果要所有长度要先变成str型
#print (list_count)

c = Counter(list_count)
#print (c)
#print (c[6])

list_temp = []#虽然c是kv形式但不是dict，i里面存的是c当前的值，不是计数
for i in c:
	list_temp.append(i)
	
for i in range(0, 9):
	if i in list_temp:
		distinct_digits[i] = c[i]
	else:
		distinct_digits[i] = 0
	#print (distinct_digits[i])
#print (distinct_digits)
	
#-----------------------------------funtion4----------------------------------
k = 0
L4 = []
while k < 10:
	L4.append(first[k] - last[k])
	k = k + 1
#取list中每个数的绝对值
absL = list(map(abs, L4))#'map' return 'iterators', have to use list
#absL.reverse()

max_gap = max(absL)
min_gap = min(absL)

#-----------------------------------funtion5-----------------------------------
list_first_and_last = []
for i in range(0, 10):
	list_first_and_last.append([first[i],last[i]])
#print (list_first_and_last)

list_first_and_last_num = []
for i in range(0, 10):
	list_first_and_last_num.append(list_first_and_last.count(list_first_and_last[i]))
print (list_first_and_last_num)

max_num = max(list_first_and_last_num)

for i in range(0, 10):
	if max_num == list_first_and_last_num[i]:
		first_and_last.add(tuple(list_first_and_last[i]))#用add别用upadte

print()
print('x is:', x)
print('L is:', L)
print()
print(f'The sum of all digits in x is equal to {sum_of_digits_in_x}.')
print()
print(f'There are {first_digit_greater_than_last}, {same_first_and_last_digits} '
      f'and {last_digit_greater_than_first} elements in L with a first digit that is\n'
      '  greater than the last digit, equal to the last digit,\n'
      '  and smaller than the last digit, respectively.'
     )
print()
for i in range(1, 9):
    if distinct_digits[i]:
        print(f'The number of members of L with {i} distinct digits is {distinct_digits[i]}.')
print()
print('The minimal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {min_gap}.'
     )
print('The maximal gap (in absolute value) between first and last digits\n'
      f'  of a member of L is {max_gap}.')
print()
print('The number of pairs (f, l) such that f and l are the first and last digits\n'
      f'of members of L is maximal for (f, l) one of {sorted(first_and_last)}.'
     )
