'''
dot_set = [0, 1, 2, 3, 4]
dot_set_quantity = [-100, 10, 20, 50, 20]
path_set = [[0, 1],
            [0, 2],
            [1, 3],
            [2, 3],
            [2, 4],
            [3, 4]]
diameter_set = [200, 200, 200, 200, 200, 200]#管径列表
length_set = [300, 300, 300, 300, 300, 300]#管长列表
#生成图
graph = {}
for k in dot_set:
    graph[k] = []
#print(graph)
for k, v in path_set:
    graph[k].append(v)
    graph[v].append(k)
#print(graph)
"""
生成字典，以点为键，相邻点的列表为值结果为
graph = {0: [1, 2], 1: [0, 3], 2: [0, 3, 4], 3: [1, 2, 4], 4: [2, 3]}
"""

'''
dot_set = [i for i in range(13)]
dot_set_quantity = [-440,
                    50, 40, 50, 30, 20,
                    30, 25, 50, 25, 50,
                    30, 40]
#按节点标号顺序，0为流入节点，列表是节点流量
path_set = [[0, 11],
            [0, 12],
            [1,2],
            [1,4],
            [2,3],
            
            [2,8],
            [3,11],
            [4,5],
            [4,7],
            [5,6],
            
            [5,9],
            [6,10],
            [7,8],
            [7,9],
            [8,11],
            
            [8,12],
            [9,10],
            [10,12]
            ]
#管段两头为节点号，小号在前大号在后，首位要从0按升序排列
diameter_set = [250 for i in range(18)]#管径列表，初始都为250
length_set = [400, 200, 400, 200, 200,
              200, 200, 200, 200, 200,
              200, 200, 200, 200, 200,
              400, 200, 200]#管长列表


#生成图
graph = {}
for k in dot_set:
    graph[k] = []
#print(graph)
for k, v in path_set:
    graph[k].append(v)
    graph[v].append(k)
#print(graph)



