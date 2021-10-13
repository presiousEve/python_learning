#!/usr/bin/env python
import sys 
import numpy as np
import copy

#读maze文件
class MazeError(Exception):
    def __init__(self, message):
        self.message = message
class Maze:
	def __init__(self, filename):
		maze = []
		self.filename = filename
		try:
			with open(filename, 'r') as f:
				for line in f.readlines():
					linestr = line.split()
					line_list = list(''.join(linestr))
					#print (line_list)
					if line_list != []:
						maze.append(list(map(int, line_list)))
		except FileNotFoundError:
			print ('There is no such file.')
			sys.exit()
		#print (maze)
		#文件为空或长度不在范围内或每行长度不同
		length = []
		if maze:
			for i in maze:
				length.append(len(i))
			if len(set(length)) != 1:
				raise MazeError('Incorrect input.')	
		else:
			raise MazeError('Incorrect input.')

		if len(maze) < 2 or len(maze) > 31:
			raise MazeError('Incorrect input.')
		if len(maze[0]) < 2 or len(maze[0]) > 41:
			raise MazeError('Incorrect input.')		

		#判断是否为数字并是 0123		
		for i in maze:
			for j in i:
				if str(j).isdigit():
					if j == 0 or j == 1 or j == 2 or j == 3:
						continue
					else:
						raise MazeError('Incorrect input.')
				else:
					raise MazeError('Incorrect input.')
	
		#判断末行末列		
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				if i == len(maze) - 1:
					if maze[i][j] == 2 or maze[i][j] == 3:
					 	 raise MazeError('Input does not represent a maze.')
				if j == len(maze[0]) -1:
					if maze[i][j] == 1 or maze[i][j] == 3:
						raise MazeError('Input does not represent a maze.')

		self.maze = maze
		self.list_gate = 0
		self.connected_wall = 0
		self.count_inacc = 0
		self.accessible = 0
		self.area_cul_de_sacs = 0
		self.path3 = 0
		
	def before(self):
		maze = self.maze

		#---------------------------double maze---------------------------------
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
				elif (i, j) not in inaccessible_area:
					row.append(len(graph[(i, j)]))
			copy3_double_maze.append(row)
		#print (copy3_double_maze)

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
		#print (gate)

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
		#print (len(path3))

		self.list_gate = list_gate
		self.connected_wall = connected_wall
		self.inaccessible_area = inaccessible_area
		self.accessible = accessible
		self.area_cul_de_sacs = area_cul_de_sacs
		self.path3 = path3

		self.double_maze = double_maze
		self.copy3_double_maze = copy3_double_maze
		self.list_all_cul_de_sacs = list_all_cul_de_sacs
		self.maze = maze

	def analyse(self):
		self.before()
		list_gate = self.list_gate
		connected_wall = self.connected_wall
		inaccessible_area = self.inaccessible_area
		accessible = self.accessible
		area_cul_de_sacs = self.area_cul_de_sacs
		path3 = self.path3

		
		#---------------------------prints---------------------------------
		if len(list_gate) == 0:
			print ('The maze has no gate.')
		elif len(list_gate) == 1:
			print ('The maze has a single gate.')
		else:
			print (f'The maze has {int(len(list_gate) / 2)} gates.')
		
		#2
		if connected_wall == 0:
			print ('The maze has no wall.')
		elif connected_wall == 1:
			print ('The maze has walls that are all connected.')
		else:
			print (f'The maze has {connected_wall} sets of walls that are all connected.')
		
		#3
		count_inacc = len(inaccessible_area)
		if count_inacc == 0:
			print ('The maze has no inaccessible inner point.')
		elif count_inacc == 0:
			print ('The maze has a unique inaccessible inner point.')
		else:
			print (f'The maze has {count_inacc} inaccessible inner points.')
		
		#4
		if accessible == 0:
			print ('The maze no accessible area.')
		elif accessible == 1:
			print ('The maze has a unique accessible area.')
		else:
			print (f'The maze has {accessible} accessible areas.')
		
		#5
		if area_cul_de_sacs == 0:
			print ('The maze has no accessible cul-de-sac..')
		elif area_cul_de_sacs == 1:
			print ('The maze has accessible cul-de-sacs that are all connected..')
		else:
			print (f'The maze has {area_cul_de_sacs} sets of accessible cul-de-sacs that are all connected.')
		
		#6
		if len(path3) == 0:
			print ('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
		if len(path3) == 1:
			print ('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
		else:
			print (f'The maze has {len(path3)} entry-exit paths with no intersections not to cul-de-sacs.')

	def display(self):
		self.before()
		filename = self.filename
		double_maze = self.double_maze
		copy3_double_maze = self.copy3_double_maze
		list_all_cul_de_sacs = self.list_all_cul_de_sacs
		path3 = self.path3
		maze = self.maze

		display_file=filename.split('.')[0]+'.tex'
		with open(display_file, 'w') as play_file:
			print('\\documentclass[10pt]{article}\n'
					'\\usepackage{tikz}\n'
					'\\usetikzlibrary{shapes.misc}\n'
					'\\usepackage[margin=0cm]{geometry}\n'
					'\\pagestyle{empty}\n'
					'\\tikzstyle{every node}=[cross out, draw, red]\n'
					'\n'
					'\\begin{document}\n'
					'\n'
					'\\vspace*{\\fill}\n'
					'\\begin{center}\n'
					'\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]', file =  play_file)
			play_file.write('% Walls\n')
			#找横的墙
			wall = []
			x_wall = []#所有横着的连接的墙的坐标[[]]
			for i in range(len(double_maze)):
				wall = []
				for j in range(len(double_maze[i])): 
					if double_maze[i][j] == 1:
						wall.append((i, j))
						if j == len(double_maze[i]) - 1:
							if len(wall) > 1:
								x_wall.append(wall)
								wall = []
					elif len(wall) > 1:
						x_wall.append(wall)
						wall = []
					else:
						wall = []

			wall = []
			y_wall = []

			for j in range(len(double_maze[i])):
				wall = []
				for i in range(len(double_maze)):
					if double_maze[i][j] == 1:
						wall.append((i, j))
						if i == len(double_maze) - 1:
							if len(wall) > 1:
								y_wall.append(wall)
								wall = []
					else:
						if double_maze[i][j] == 0:
							if len(wall) > 1:
								y_wall.append(wall)
								wall = []
							else:
								wall = []
			for i in x_wall:
				m = i[0][0] / 2
				n = i[0][1] / 2
				p = i[len(i) - 1][0] / 2
				q = i[len(i) - 1][1] / 2
				play_file.write('    \\draw ('+str(int(n))+','+str(int(m))+') -- ('+str(int(q))+','+str(int(p))+');\n')
			for i in y_wall:
				m = i[0][0] / 2
				n = i[0][1] / 2
				p = i[len(i) - 1][0] / 2
				q = i[len(i) - 1][1] / 2
				play_file.write('    \\draw ('+str(int(n))+','+str(int(m))+') -- ('+str(int(q))+','+str(int(p))+');\n')

			play_file.write('% Pillars\n')
			for i in range(len(copy3_double_maze)):
				for j in range(len(copy3_double_maze[i])):
					if copy3_double_maze[i][j] == 4:
						if i % 2 == 0 and j % 2 == 0:
							play_file.write('    \\fill[green] ('+str(int(j / 2))+','+str(int(i / 2))+') circle(0.2);\n')

			play_file.write('% Inner points in accessible cul-de-sacs\n')
			for i in list_all_cul_de_sacs:
				if i[0] % 2 == 1 and i[1] % 2 == 1:
					play_file.write('    \\node at ('+str(i[1] / 2)+','+str(i[0] / 2)+') {};\n')

			play_file.write('% Entry-exit paths without intersections\n')
			p = []
			for i in path3:
				for j in i:
					p.append(j)

			grid2 = np.zeros([len(maze) * 2 - 1, len(maze[0]) * 2 - 1], dtype = int)

			for i in p:
				grid2[i[0]][i[1]] = 1

			path = []
			x_path = []
			for i in range(len(grid2)):
				path = []
				for j in range(len(grid2[i])): 
					if grid2[i][j] == 1:
						path.append((i, j))
						if j == len(grid2[i]) - 1:
							if len(path) > 1:
								x_path.append(path)
								path = []
					elif len(path) > 1:
						x_path.append(path)
						path = []
					else:
						path = []

			path = []
			y_path = []

			for j in range(len(grid2[i])):
				path = []
				for i in range(len(grid2)):
					if grid2[i][j] == 1:
						path.append((i, j))
						if i == len(grid2) - 1:
							if len(path) > 1:
								y_path.append(path)
								path = []
					else:
						if grid2[i][j] == 0:
							if len(path) > 1:
								y_path.append(path)
								path = []
							else:
								path = []
			for i in x_path:
				m = i[0][0]
				n = i[0][1]
				p = i[-1][0]
				q = i[-1][1]
				if m % 2 == 1 and n % 2 == 1 and p % 2 == 1 and q % 2 == 1:
					m = m / 2
					if m == 0:
						m = -0.5
					if m == len(grid2[0]) - 1:
						m = m + 1.0

					n = n / 2
					if n == 0:
						n = -0.5
					if n == len(grid2) - 1:
						n = n + 1.0

					p = p / 2
					if p == 0:
						p = -0.5
					if p == len(grid2[0]) - 1:
						p = p + 1.0

					q = q / 2
					if q == 0:
						q = -0.5
					if q == len(grid2) - 1:
						q = q + 1.0
				play_file.write('    \\draw[dashed, yellow] ('+str(n)+','+str(m)+') -- ('+str(q)+','+str(p)+');\n')

			for i in y_path:
				m = i[0][0]
				n = i[0][1]
				p = i[-1][0]
				q = i[-1][1]
				if m % 2 == 1 and n % 2 == 1 and p % 2 == 1 and q % 2 == 1:
					m = m / 2
					if m == 0:
						m = -0.5
					if m == len(grid2[0]) - 1:
						m = m + 1.0

					n = n / 2
					if n == 0:
						n = -0.5
					if n == len(grid2) - 1:
						n = n + 1.0

					p = p / 2
					if p == 0:
						p = -0.5
					if p == len(grid2[0]) - 1:
						p = p + 1.0

					q = q / 2
					if q == 0:
						q = -0.5
					if q == len(grid2) - 1:
						q = q + 1.0
				play_file.write('    \\draw[dashed, yellow] ('+str(n)+','+str(m)+') -- ('+str(q)+','+str(p)+');\n')

			play_file.write('\\end{tikzpicture}\n'
					'\\end{center}\n'
					'\\vspace*{\\fill}\n'
					'\n'
					'\\end{document}\n')






