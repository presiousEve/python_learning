# Uses Global Temperature Time Series, avalaible at
# http://data.okfn.org/data/core/global-temp, stored in the file monthly_csv.csv,
# assumed to be stored in the working directory.
# Prompts the user for the source, a year or a range of years, and a month.
# - The source is either GCAG or GISTEMP.
# - The range of years is of the form xxxx -- xxxx (with any number of spaces,
#   possibly none, around --) and both years can be the same,
#   or the first year can be anterior to the second year,
#   or the first year can be posterior to the first year.
# We assume that the input is correct and the data for the requested month
# exist for all years in the requested range.
# Then outputs:
# - The average of the values for that source, for this month, for those years.
# - The list of years (in increasing order) for which the value is larger than that average.
# 
# Written by Yuting GUO and Eric Martin for COMP9021


import sys
import os
import csv
import re
import numpy as np


filename = 'monthly_csv.csv'
if not os.path.exists(filename):
    print(f'There is no file named {filename} in the working directory, giving up...')
    sys.exit()

source = input('Enter the source (GCAG or GISTEMP): ')
year_or_range_of_years = input('Enter a year or a range of years in the form XXXX -- XXXX: ')
month = input('Enter a month: ')
average = 0
years_above_average = []

#将文件存入list
file_list = []
linestr_list = []
with open('monthly_csv.csv','r') as file:
	for line in file.readlines():
		linestr = line.strip()#去掉换行符\n
		linestr_list = linestr.split(',')#按照‘，’分割的str切片
		file_list.append(linestr_list)
file_list.pop(0)#删除文件的第一行是表头

#将日期中的-去掉
for i in file_list:
	#i[1] = i[1].split('-')
	i[1] = i[1].replace('-','')#将日期中的-替换掉
#print (file_list)

#将输入的年份或范围转化为字符串
#year_or_range_of_years = year_or_range_of_years.split('--')#也能直接去掉--返回一个list切片，但是这里考虑的是如果输入的不是严格是--，就容易出错
#用模式匹配直接将非数字元素踢出去返回一个str
year_or_range_of_years_list = filter(str.isdigit, list(year_or_range_of_years))#filter目标函数是可迭代对象
year_or_range_of_years = ''.join(year_or_range_of_years_list)#直接输出list报错，迭代进str输出
#print (year_or_range_of_years)

#将输入的年份放在一个列表里
if year_or_range_of_years:
	list_input_year = [int(year_or_range_of_years[0:4])]
	if len(year_or_range_of_years) == 8:
		list_input_year.append(int(year_or_range_of_years[4:8]))
	else:
		list_input_year.append(list_input_year[0])
	list_input_year = sorted(list_input_year)
#print (list_input_year)

#定义一个月份字典
month_dict = {
	'January': '01',
	'February': '02',
	'March': '03',
	'April': '04',
	'May': '05',
	'June': '06',
	'July': '07',
	'August': '08',
	'September': '09',
	'October': '10',
	'November': '11',
	'December': '12',
}

if month:
	month_num = month_dict[month]			

list_mean = []
while list_input_year[1] + 1 != list_input_year[0]:	
	for i in file_list:
		if i[0] == source:#如果来源相同
			if i[1][0:4] == str(list_input_year[0]):#如果和年份相同				
				if i[1][4:6] == month_num:#如果月份相同
					list_mean.append((i[1][0:4], float(i[2])))#将后面的数存入一个list
					#print (list_mean)
					list_input_year[0] += 1#年份自增

					

mean_average=[]
for i in list_mean:
	mean_average.append(i[1])
#print (mean_average)					
average = np.mean(mean_average)	

for i in list_mean:
	if i[1] > average:
		years_above_average.append(int(i[0]))
	
	
print(f'The average anomaly for {month} in this range of years is: {average:.2f}.')
print('The list of years when the temperature anomaly was above average is:')
print(years_above_average)
