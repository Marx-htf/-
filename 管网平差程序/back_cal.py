import time
time_1 = time.process_time()#程序运行，开始计时

import numpy as np
import pingcha
A = pingcha.C
#print(A)
q = pingcha.init_q
print('初始流量:\n',q)
Q = pingcha.dot_set_quantity
#print(Q)
#allpath_list = [[0, 2, 3, 1], [0, 2, 4, 3, 1], [2, 4, 3]]这是测试init_input.py文件测试留下的
allpath_list = pingcha.allpath_list
#allpath_list点转换成线编号,存入pathlist_p，用管段标号表示环路
pathlist_p = []
for i in allpath_list:
    l = []
    for j in range(len(i)):
        a = [i[j-1], i[j]]
        for n in range(len(pingcha.path_set)):
            if a[1]==pingcha.path_set[n][0] and a[0]==pingcha.path_set[n][1]:
                l.append(n)
                break
            elif a[0]==pingcha.path_set[n][0] and a[1]==pingcha.path_set[n][1]:
                l.append(-n)
            else:
                None
    pathlist_p.append(l)
#print(pathlist_p)#挑选出的闭合环路
'''
pingcha.py找出环中的管道是没有方向性的，这段代码是给管段定方向的。
规定流量是从小号节点流向大号节点为正，反之为负。
这样环就可以表示成一个有方向性的环了。
而且之后的流量方向也是以此为基准进行计算的。
'''

l = [[0 for i in range(len(pingcha.path_set))] for j in range(len(pathlist_p))]
for i in range(len(pathlist_p)):
    for j in pathlist_p[i]:
        if j >= 0:
            l[i][j] = 1
        else:
            l[i][-j] = -1
L = np.array(l)
#print(L)
s = [64*pingcha.length_set[i]/(3.1415926**2*100**2*pingcha.diameter_set[i]) for i in range(len(q))]
h = [s[i]*(q[i]**2) for i in range(len(q))]
#print('h:', h)

x = 0
t = 1#闭合环路的水头误差，当所有环路小于0.01m，即完成平差

'''
这整个while循环就是在平差计算，每算完一轮就检查一次水损最大环的水损，所有环水损都小于0.01就全部完成了
这里面就是流量方向性的问题比较难解决，关系复杂点。
但只要记住管段流量是小号节点流向大号节点为正值，应该就不会难理解。
'''
while t > 0.01:
    x+=1
    closure_error_list = []#各环的闭合差组成的列表
    for a in pathlist_p:
        closure_error = 0#a环的闭合差
        sum_sq = 0#环路sq之和
        for b in a:
            sum_sq += s[abs(b)]*abs(q[abs(b)])
            if b >= 0:#可能会有bug，0号管没法判定方向
                closure_error += h[abs(b)]
            else:
                closure_error -= h[abs(b)]
        closure_error_list.append(closure_error)
        rivision_q = closure_error/(2*sum_sq)#校正流量
        for b in a:
            if (b>=0 and q[abs(b)]>0) or\
               (b<0 and q[abs(b)]<0):
                q[abs(b)] -= rivision_q
            elif (b<0 and q[abs(b)]>0) or\
                 (b>=0 and q[abs(b)]<0):
                q[abs(b)] += rivision_q

            #根据经济流速选管径
            t1 = 0
            while True:
                t1 += 1
                if t1 == 4:#这里差不多循环4次就可以选出经济管径了，多了运行时间长，少了选不到
                    break
                v = abs((q[abs(b)]*1000))/(3.1415926*(pingcha.diameter_set[abs(b)]/2)**2)#流速
                if v<0.6:
                    if pingcha.diameter_set[abs(b)] <= 100:
                        break
                    else:
                        pingcha.diameter_set[abs(b)] -= 50
                elif v>0.9:
                    if pingcha.diameter_set[abs(b)] >= 400:
                        break
                    else:
                        pingcha.diameter_set[abs(b)] += 50
                else:
                    #print(pingcha.diameter_set[abs(b)])#尝试输出看程序选择管径时的变化
                    #print(v)#这里可以尝试输出，检验是否经济流速
                    break
                #print(pingcha.diameter_set[abs(b)])#尝试输出看程序选择管径时的变化
                #print(v)#这里可以尝试输出，检验是否经济流速
                    
        #print(rivision_q)#查看一下每次平差的校正流量
        h = [s[i]*(q[i]**2) for i in range(len(q))]
    t = max([abs(i) for i in closure_error_list])
    print('第', x,'次平差')
    #print('h:', h)
    print('管段流量:\n', q)
    print('管径:', [i for i in pingcha.diameter_set])
    #print('closure_error_list:', closure_error_list)
    print('环路最大水头闭合差:', t)

time_2 = time.process_time()#程序结束，停止计时
print('耗时:',time_2-time_1)#输出运行时间

'''
使用init_input.py第一部分示例代码的运行最终结果：
"
初始流量:
 [-42.72727273 -57.27272727 -32.72727273 -18.18181818 -19.09090909
  -0.90909091]
[[0, -1, -3, 2], [0, -1, -4, 5, 2], [3, -4, 5]]
第 1 次平差
管段流量:
 [-45.45897921 -54.54102079 -35.45897921 -17.19603964 -17.34498114
  -2.65501886]
管径: [300, 300, 250, 200, 200, 100]
环路最大水头闭合差: 0.6945441770862086
第 2 次平差
管段流量:
 [-45.25836147 -54.74163853 -35.25836147 -17.27833334 -17.46330519
  -2.53669481]
管径: [300, 300, 250, 200, 200, 100]
环路最大水头闭合差: 0.051971709557047996
第 3 次平差
管段流量:
 [-45.2718711  -54.7281289  -35.2718711  -17.27096966 -17.45715924
  -2.54284076]
管径: [300, 300, 250, 200, 200, 100]
环路最大水头闭合差: 0.0036149345716680603
耗时: 0.140625
"
'''
