import numpy as np
import init_input

class dot(object):
    def __init__(self, number, quantity_of_flow):
        self.n = number
        self.q = quantity_of_flow
class path(object):
    def __init__(self, number, start, finish, quantity_of_flow, diameter, length):
        self.n = number
        self.s = start
        self.f = finish
        self.q = quantity_of_flow
        self.d = diameter
        self.l = length
class net(object):
    def __init__(self, dot_set, path_set):
        self.dote_set = dot_set
        self.path_set = path_set

'''管网模型参数'''
dot_set = init_input.dot_set
dot_set_quantity = init_input.dot_set_quantity
path_set = init_input.path_set
diameter_set = init_input.diameter_set
length_set = init_input.length_set
graph = init_input.graph
#这里没什么，就是把init_input.py的参数复制过来

'''创建节点类'''
dot_list = []  # dot类列表
for i in range(len(dot_set)):
    dot(i, dot_set_quantity[i]).n = i
    dot(i, dot_set_quantity[i]).q = dot_set_quantity[i]
    #print(dot(i, dot_set_quantity[i]).n, dot(i, dot_set_quantity[i]).q)
    D = dot(i, dot_set_quantity[i])
    dot_list.append(D)
#print(D)
'''
每个点作为一个类，有两个属性，n和q，n是编号，q是流量，有正负之分
所有的D类（点）存入dot_list列表
'''

'''创建管道类，初始流量为0'''
path_list = []  # path类列表
for i in range(len(path_set)):
    path(i, path_set[i][0], path_set[i][1], 0, diameter_set[i], length_set[i]).s = path_set[i][0]
    path(i, path_set[i][0], path_set[i][1], 0, diameter_set[i], length_set[i]).f = path_set[i][1]
    #print(i, path_set[i][0], path_set[i][1], 0)
    L = dot(i, path(i, path_set[i][0], path_set[i][1], 0, diameter_set[i], length_set[i]))
    path_list.append(L)
A = np.zeros((len(dot_set), len(dot_set)))  # A是节点连接矩阵
for i in path_set:
    A[i[0]][i[1]] = 1
    A[i[1]][i[0]] = 1
#print(A)
'''
管道L作为一个类，有属性n是编号，父类q(就是开头的path类)有特性n,s,f,q,d,l
所有L存入path_list列表
生成下面的表格
管段标号/流入端/流出端/流量（这里是0，占位，之后会赋值）
0 0 1 0
1 0 2 0
2 1 3 0
3 2 3 0
4 2 4 0
5 3 4 0

形成相连节点矩阵，显然是对称矩阵
A = 
[[0. 1. 1. 0. 0.]
 [1. 0. 0. 1. 0.]
 [1. 0. 0. 1. 1.]
 [0. 1. 1. 0. 1.]
 [0. 0. 1. 1. 0.]]
'''

#****************************************************************************
# 假设某些管段流量，再求初始管段流量
v = len(dot_set)
e = len(path_set)
r = 2 + e - v
#print(v, e, r)
'''
三个参数是图论里的欧拉定理的三个参数，为建立矩阵大小做准备
'''
C = np.zeros((v, e))
for i in range(len(path_set)):
    m = 1
    for j in path_set[i]:
        C[j][i] = m
        m = -1
#print(C)
#解方程，得出一组初始流量
init_q, useless1, u2, u3 = np.linalg.lstsq(C, dot_set_quantity, rcond=0)
#print(init_q)
'''
根据path_set，得到（管道-节点）矩阵，横轴代表管段标号，纵轴代表节点标号，流进流出节点有正负1区分
C=
[[ 1.  1.  0.  0.  0.  0.]
 [-1.  0.  1.  0.  0.  0.]
 [ 0. -1.  0.  1.  1.  0.]
 [ 0.  0. -1. -1.  0.  1.]
 [ 0.  0.  0.  0. -1. -1.]]

numpy库当中的一个函数，目的就是为了根据节点流量得到一个未平差的管段流量解
init_q=
[-42.72727273 -57.27272727 -32.72727273 -18.18181818 -19.09090909 -0.90909091] 
'''

# 搜索所有环算法***************************************************************
# 找到所有从start到end的路径
def findAllPath(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]

    paths = []  # 存储所有路径
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPath(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

allpath_list = []
for i in range(len(dot_set)):
    for j in range(i + 1, len(dot_set)):
        if A[i][j] == 1:
            allpath = findAllPath(graph, i, j)
            allpath_list.append(allpath)

i = True
while i == True:
    if len(allpath_list) != 1:
        allpath_list[0].extend(allpath_list[1])
        del allpath_list[1]
    else:
        i = False
allpath_list = allpath_list[0]

for i in range(len(allpath_list) - 1):
    if len(allpath_list[i]) == 2:
        allpath_list[i] = []
        continue
    for j in range(i + 1, len(allpath_list)):
        if sorted(allpath_list[i]) == sorted(allpath_list[j]):
            allpath_list[j] = []

if len(allpath_list[-1]) == 2:
    allpath_list[-1] = []
m = 0
for i in allpath_list:
    if i == []:
        m += 1
for i in range(m):
    allpath_list.remove([])
#print(allpath_list)
'''
这一大段代码写的并不好，应该有更好的算法，我没时间去想了
大概意思就是：
根据graph字典不断遍历，找到所有的环，不管大环还是小环
得到一个结果
allpath_list=
[[0, 2, 3, 1], [0, 2, 4, 3, 1], [2, 4, 3]]
'''
