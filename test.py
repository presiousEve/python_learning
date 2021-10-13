import sys 
import numpy as np
import copy

filename = input('input file name: ')
maze = []
with open(filename, 'r') as f:
    for line in f.readlines():
        linestr = line.split()
        line_list = list(''.join(linestr))
        #print (line_list)
        if line_list != []:
            maze.append(list(map(int, line_list)))
#print (maze)
def display_maze(maze):
    double_maze = np.zeros([len(maze) * 2 - 1, len(maze[0]) * 2 - 1], dtype = int)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                double_maze[2 * i][2 * j] = 1
                double_maze[2 * i][2 * j + 1] = 1
                double_maze[2 * i][2 * j + 2] = 1
            elif maze[i][j] == 2:
                double_maze[2 * i][2 * j] = 1
                double_maze[2 * i + 1][2 * j] = 1
                double_maze[2 * i + 2][2 * j] = 1
            elif maze[i][j] == 3:
                double_maze[2 * i][2 * j] = 1
                double_maze[2 * i + 1][2 * j] = 1
                double_maze[2 * i + 2][2 * j] = 1
                double_maze[2 * i][2 * j + 1] = 1
                double_maze[2 * i][2 * j + 2] = 1
                #print (double_maze)
    return double_maze
double_maze = display_maze(maze)

#print (double_maze)

#---------------------------funtion 1: counting gate---------------------------------
list_gate = []
for i in range(len(double_maze)):
	for j in range(len(double_maze[i])):
		if i == 0 or i == len(double_maze) - 1:			
			if double_maze[i][j] == 0 and j % 2 == 1:
				list_gate.append((i, j))
				if i == 0:
					list_gate.append((i + 1, j))
				else:
					list_gate.append((i - 1, j))
		if j == 0 or j == len(double_maze[i]) - 1:
			if double_maze[i][j] == 0 and i % 2 == 1:
				list_gate.append((i, j))
				if j == 0:
					list_gate.append((j + 1, j))
				else:
					list_gate.append((j - 1, j))
#print (list_gate)

#---------------------------funtion 2: connected wall---------------------------------
cpoy1_double_maze = copy.deepcopy(display_maze(maze))

def bolt1(i, j):
	if not cpoy1_double_maze[i][j]:
		return 
	cpoy1_double_maze[i][j] = 0
	if j - 1 >= 0:
		bolt1(i, j - 1)
	if i - 1 >= 0:
		bolt1(i - 1, j)
	if j + 1 < len(cpoy1_double_maze[i]):
		bolt1(i, j + 1)
	if i + 1 < len(cpoy1_double_maze):
		bolt1(i + 1, j)

connected_wall  = 0
for i in range(len(cpoy1_double_maze)):
	for j in range(len(cpoy1_double_maze[i])):
		if cpoy1_double_maze[i][j]:
			#print (i, j)
			connected_wall += 1
			bolt1(i, j)

#---------------------------funtion 3:  inaccessible inner points---------------------------------
cpoy2_double_maze = copy.deepcopy(display_maze(maze))

def bolt2(i, j, l):
	if cpoy2_double_maze[i][j]:
		return
	cpoy2_double_maze[i][j] = 1
	l.append((i, j))
	if j - 1 >= 0:
		bolt2(i, j - 1, l)
	if i - 1 >= 0:
		bolt2(i - 1, j, l)
	if j + 1 < len(cpoy1_double_maze[i]):
		bolt2(i, j + 1, l)
	if i + 1 < len(cpoy1_double_maze):
		bolt2(i + 1, j, l)
	return l

zero_area = []
l = []
for i in range(len(cpoy2_double_maze)):
	for j in range(len(cpoy2_double_maze[i])):
		if cpoy2_double_maze[i][j] == 0:
			l = bolt2(i, j, l)
			zero_area.append(l)
			l = []

graph = dict()
for i in range(len(double_maze)):	
	for j in range(len(double_maze[i])):
		children = []
		if double_maze[i][j] == 0:				
			if i != 0:
				if double_maze[i - 1][j] == 0:
					children.append((i - 1, j))
			if i !=len(double_maze) - 1:
				if double_maze[i + 1][j] == 0:
					children.append((i + 1, j))
			if j != 0:
				if double_maze[i][j - 1] == 0:
					children.append((i, j - 1))
			if j != len(double_maze[i]) - 1:
				if double_maze[i][j + 1] == 0:
					children.append((i, j + 1))
			graph[(i,j)] = children			
#print (graph)

def BFS(graph, s):
	queue = []
	queue.append(s)
	seen = set()
	seen.add(s)
	while (len(queue) > 0):
		vertex = queue.pop(0)
		#print (vertex)
		nodes = graph[vertex]
		for w in nodes:
			if w in nodes:
				if w not in seen:
					queue.append(w)
					seen.add(w)
	return seen

def routes(graph, double_maze):#所有有门的通路，里面有重复的，
	routes = []
	for i in list_gate:
		if i[0] % 2  == 1 and i[1] % 2 == 1:
			s = i
			routes.append(list(BFS(graph, s)))
	return routes
routes = routes(graph, double_maze)

list_accessible = []
list_zero_area = []
for i in routes:
	for j in i:
		#print (i)
		list_accessible.append(j)
for i in zero_area:
	for j in i:
		list_zero_area.append(j)
inaccessible =  set(list_zero_area) - set(list_accessible)
inaccessible_area = []
for i in inaccessible:
	if i[0] % 2  == 1 and i[1] % 2 == 1:
		inaccessible_area.append(i)
#print (inaccessible_area)

#---------------------------funtion 4: accessible areas---------------------------------
list_temp = []#存放不可进入的点坐标，如果不可进入的点都是单个不是一片区域则用inaccessible_area
copy_zero_area = copy.deepcopy(zero_area)
for i in inaccessible_area:
	for j in zero_area:
		if i in j :
			if j not in list_temp:
				list_temp.append(j)
if list_temp:
	accessible = len(zero_area) - len(list_temp)
else:
	accessible = len(zero_area) - len(inaccessible_area)

#---------------------------funtion 5: sets of accessible cul-de-sacs that are all connected.---------------------------------
#将矩阵单元变为记录方向次数，墙为‘A’
copy3_double_maze = []
for i in range(len(double_maze)):	
	row = []
	for j in range(len(double_maze[i])):		
		if double_maze[i][j] == 1 or (i, j) in inaccessible_area:
			row.append('A')
			#print ((i, j))
			continue
		else:
			if double_maze[i][j] == 0 and (i, j) not in inaccessible_area:
				row.append(len(graph[(i, j)]))
	copy3_double_maze.append(row)
#print (graph)

#门的通路多算一个
for i in range(len(copy3_double_maze)):
	for j in range(len(copy3_double_maze[i])):
		if i == 0:
			if str(copy3_double_maze[i][j]).isdigit():
				copy3_double_maze[i][j] += 1
		if j == 0:
			if str(copy3_double_maze[i][j]).isdigit():
				copy3_double_maze[i][j] += 1
		if i == len(copy3_double_maze) - 1:
			if str(copy3_double_maze[i][j]).isdigit():
				copy3_double_maze[i][j] += 1
		if j == len(copy3_double_maze[i]) - 1:
			if str(copy3_double_maze[i][j]).isdigit():
				copy3_double_maze[i][j] += 1

#print (list_accessible)
#如果为1就这个设为墙，旁边数字 - 1
#用while循环，次数不超过所有accessible点
a = 0
while a < len(list_accessible):
	for i in range(len(copy3_double_maze)):
		for j in range(len(copy3_double_maze[i])):
			if copy3_double_maze[i][j] == 1:
				if i != 0:
					if str(copy3_double_maze[i - 1][j]).isdigit() and copy3_double_maze[i - 1][j] != -1:
						copy3_double_maze[i - 1][j] = copy3_double_maze[i - 1][j] -  1
				if i !=len(double_maze) - 1:
					if str(copy3_double_maze[i + 1][j]).isdigit() and copy3_double_maze[i + 1][j] != -1:
						copy3_double_maze[i + 1][j] = copy3_double_maze[i + 1][j] -  1
				if j != 0:
					if str(copy3_double_maze[i][j - 1]).isdigit() and copy3_double_maze[i][j - 1] != -1:
						copy3_double_maze[i][j - 1] = copy3_double_maze[i][j - 1] - 1
				if j != len(double_maze[i]) - 1:
					if str(copy3_double_maze[i][j + 1]).isdigit() and copy3_double_maze[i][j + 1] != -1:
						copy3_double_maze[i][j + 1] = copy3_double_maze[i][j + 1] - 1
				copy3_double_maze[i][j] = -1
	a += 1

cul_de_sacs = 0
list_all_cul_de_sacs = []
for i in range(len(copy3_double_maze)):
	for j in range(len(copy3_double_maze[i])):
		if copy3_double_maze[i][j] == -1:
			list_all_cul_de_sacs.append((i, j))
#print (list_all_cul_de_sacs)

grid = np.zeros([len(maze) * 2 - 1, len(maze[0]) * 2 - 1], dtype = int)
m = 0
n = 0
for i in list_all_cul_de_sacs:
	m = i[0]
	n = i[1]
	if copy3_double_maze[m][n] == -1:
		grid[m][n] = 1
#print (grid)

def bolt3(i, j):
	if not grid[i][j]:
		return
	grid[i][j] = 0
	if j - 1 >= 0:
		bolt3(i, j - 1)
	if i - 1 >= 0:
		bolt3(i - 1, j)
	if j + 1 < len(grid[i]):
		bolt3(i, j + 1)
	if i + 1 < len(grid):
		bolt3(i + 1, j)
area_cul_de_sacs = 0

for i in range(len(grid)):
	for j in range(len(grid[i])):
		if grid[i][j] == 1:
			area_cul_de_sacs += 1
			bolt3(i, j)
#print (area_cul_de_sacs)

#---------------------------funtion 6: entry-exit paths---------------------------------
#print (copy3_double_maze)

gate = []#找出是出口的坐标，不包括里面的点
for i in list_gate:
	if i[0] == 0 or i[1] == 0 or i[0] == len(double_maze) - 1 or i[1] == len(double_maze[0]) - 1:
		gate.append(i)
print (gate)

g = 0
two_door = []
for p in routes:#如果这条通路里有两个门，并除去两门，除去-1，里面没有‘3’，就是可行的通路
	g = 0
	for q in p:
		if q in gate:
			g += 1
	if g == 2:
		two_door.append(p)#只有两个门的通路

#去掉里面的死路
path1 = []
remove_1 = set()
for i in two_door:
	remove_1 = set(i) - set(list_all_cul_de_sacs)
	if remove_1:
		path1.append(remove_1)
	else:
		path1.append(i)

#去掉有岔路的
path2 = []
for i in path1:
	for j in i:
		if copy3_double_maze[j[0]][j[1]] == 3:
			if j[0] == 0 or j[1] == 0 or j[0] == len(double_maze) - 1 or j[1] == len(double_maze[0]) - 1:
				continue
			else:
				break
	path2.append(i)

#去掉重复
path3 = [path2[0]]
for i in path2:
	if i not in path3:
		path3.append(i)
#print (path3)
'''
for i in range(len(copy3_double_maze)):
	for j in range(len(copy3_double_maze[i])):
		if copy3_double_maze[i][j] == 4:
			if i % 2 == 0 and j % 2 == 0:
				#print ((int(j / 2),int(i / 2)))

#print (list_all_cul_de_sacs)
for i in list_all_cul_de_sacs:
	if i[0] % 2 == 1 and i[1] % 2 == 1:
		#print ((i[1] / 2),(i[0] / 2))
'''
p = []
for i in path3:
	for j in i:
		p.append(j)

grid2 = np.zeros([len(maze) * 2 - 1, len(maze[0]) * 2 - 1], dtype = int)

for i in p:
	grid2[i[0]][i[1]] = 1
print (grid2)

path = []
x_path = []
for i in range(len(grid2)):
	path = []
	for j in range(len(grid2[i])): 
		if grid2[i][j] == 1:
			path.append((i, j))
			print ((i,j))
			if j == len(grid2[i]) - 1:
				if len(path) > 1:
					x_path.append(path)
					path = []
		elif len(path) > 1:
			print (path)
			x_path.append(path)
			path = []
		else:
			path = []
print (x_path)
'''
path = []
y_path = []
for j in range(len(grid2[i])):
	path = []
	for i in range(len(grid2)): 
		if grid2[i][j] == 1:
			path.append((i, j))
			print ((i,j))
			if j == len(grid2[i]) - 1:
				if len(path) > 1:
					y_path.append(path)
					path = []
		elif len(path) > 1:
			print (path)
			y_path.append(path)
			path = []
		else:
			path = []
print (y_path)
'''
for i in x_path:
	m = i[0][0] / 2
	if i[0][0] == 0:
		m = i[0][0] / 2 - 1
	if i[0][1] == len(i) - 1:
		m = i[0][1] / 2 + 1

	n = i[0][1] / 2
	if i[0][1] == 0:
		n = i[0][1] / 2 - 1
	if i[0][1] == len(i) - 1:
		n = i[0][1] / 2 + 1

	p = i[-1][0] / 2
	if i[-1][0] == 0:
		p = i[-1][0] / 2 - 1
	if i[-1][0] == len(i) - 1:
		p = i[-1][1] / 2 + 1

	q = i[-1][1] / 2
	if i[-1][1] == 0:
		q = i[-1][1] / 2 - 1
	if i[-1][1] == len(i) - 1:
		q = i[-1][1] / 2 + 1
	
	print ((n,m))
	print ((q,p))
'''
for i in y_path:
	m = i[0][0] / 2
	if i[0][0] == 0:
		m = i[0][0] / 2 - 1
	if i[0][0] == len(i) - 1:
		m = i[0][1] / 2 + 1

	n = i[0][0] / 2
	if i[0][1] == 0:
		n = i[0][0] / 2 - 1
	if i[0][1] == len(i) - 1:
		n = i[0][1] / 2 + 1

	p = i[-1][0] / 2
	if i[-1][0] == 0:
		p = i[-1][0] / 2 - 1
	if i[-1][0] == len(i) - 1:
		p = i[-1][1] / 2 + 1

	q = i[-1][1] / 2
	if i[-1][1] == 0:
		q = i[-1][1] / 2 - 1
	if i[-1][1] == len(i) - 1:
		q = i[-1][1] / 2 + 1
	
	print ((n,m))
	print ((q,p))
'''	



