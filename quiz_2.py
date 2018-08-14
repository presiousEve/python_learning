# Written by Yuting GUO and Eric Martin for COMP9021

import sys
from random import seed, randint
from math import gcd
from fractions import Fraction#引入分数库
from collections import Counter

try:
    arg_for_seed, length, max_value = input('Enter three strictly positive integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, length, max_value = int(arg_for_seed), int(length), int(max_value)
    if arg_for_seed < 1 or length < 1 or max_value < 1:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(1, max_value) for _ in range(length)]
print('Here is L:')
print(L)
print

size_of_simplest_fraction = None
simplest_fractions = []

size_of_most_complex_fraction = None
most_complex_fractions = []

multiplicity_of_largest_prime_factor = 0

largest_prime_factors = []

#--------------定义分数list
fractions_list = []
for i in L:
	for j in L:
		if i <= j:
			fractions_list.append(Fraction(i, j))
		else:
		    continue
#print (fractions_list)

#----------------将分子分母分别存放在两个list中
numerator_list = []
denominator_list = []
for i in fractions_list:
	numerator_list.append(i.numerator)
	denominator_list.append(i.denominator)

size_of_simplest_fraction = len(str(min(numerator_list))) + len(str(min(denominator_list)))
size_of_most_complex_fraction = len(str(max(numerator_list))) + len(str(max(denominator_list)))

#---------------找最小位数分数和最大位数分数
simplest_fractions_list = []
most_complex_fractions_list = []

for i in fractions_list:
	#print (i)
	if (len(str(i.numerator)) == 1 and len(str(i.denominator)) == 1):#要用and不能用%
		simplest_fractions_list.append(i)
	    #print (i.numerator)
	    #print (i.denominator)
	elif (len(str(i.numerator)) == len(str(max(numerator_list))) and len(str(i.denominator)) == len(str(max(denominator_list)))):
		most_complex_fractions_list.append(i)

#如果分子分母最大都只有一位数，最复杂分数=最简单分数	
if (len(str(max(numerator_list))) == 1 and len(str(max(denominator_list))) == 1):
	most_complex_fractions_list = simplest_fractions_list
		
#---------------去除重复分数并按大小排列	
simplest_fractions_list = sorted(list(set(simplest_fractions_list)))
most_complex_fractions_list = sorted(list(set(most_complex_fractions_list)) ,reverse = True)
#print (simplest_fractions_list)

#将每个分数转化为list存在list里
for i in simplest_fractions_list:
	simplest_fractions.append([i.numerator, i.denominator])
for i in most_complex_fractions_list:
	most_complex_fractions.append([i.numerator, i.denominator])
#print (simplest_fractions)

#定义一个分母list
denominator_list = []
for i in most_complex_fractions_list:
	denominator_list.append(i.denominator)
#print (denominator_list)

#---------------------定义一个获取质因数的方法，返回质因数list
def get_prime_num(num):
	prime = [2, 3, 5, 7, 11, 13, 17, 19]
	prime_list = []
	for i in prime:
		while num % i == 0:
			prime_list.append(i)
			num = num / i
	return prime_list

prime_denominator_list = []#存放分母质因数list的列表
for i in denominator_list:
    prime_denominator_list.append(get_prime_num(i))
#print (prime_denominator_list)

#质因数为key，次数为value存放在字典里
prime_count = []
for i in prime_denominator_list:
	for j in i:		
		prime_count.append((j, i.count(j)))#魔障了！直接在()给tuple赋值
#print (prime_count)

#定义两个list分别存放质因数和次数
prime_count_a = []
prime_count_b = []
for i in prime_count:
	prime_count_a.append(i[0])
	prime_count_b.append(i[1])
#print (prime_count_b)
multiplicity_of_largest_prime_factor = max(prime_count_b)

#输出对应最大次数的质因数
key = []
j = 0
for i in prime_count_b:	
	if i == multiplicity_of_largest_prime_factor:
		key.append(j)
		j = j + 1
	else:
		j = j + 1
#print (key)

for i in key:
	largest_prime_factors.append(prime_count_a[i])
largest_prime_factors = sorted(list(set(largest_prime_factors)))
	
print('The size of the simplest fraction <= 1 built from members of L is:',
      size_of_simplest_fraction
     )
print('From smallest to largest, those simplest fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in simplest_fractions))

print('The size of the most complex fraction <= 1 built from members of L is:',
      size_of_most_complex_fraction
     )
print('From largest to smallest, those most complex fractions are:')
print('\n'.join(f'    {x}/{y}' for (x, y) in most_complex_fractions))

print("The highest multiplicity of prime factors of the latter's denominators is:",
      multiplicity_of_largest_prime_factor
     )

print('These prime factors of highest multiplicity are, from smallest to largest:')
print('   ', largest_prime_factors)
        
