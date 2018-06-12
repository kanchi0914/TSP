import math
import numpy as np
import matplotlib.pyplot as plt

#最適解の確認
def opt_check(dataname):
    root = []
    f = open(dataname)
    lines = f.readlines()
    print (lines)
    datalen = len(lines)
    f.close()
    for i in range(datalen):
        sp = lines[i].split()
        root.append(int(sp[0]) - 1)
    return root

#データの読み込みと初期化
def init_data(dataname):
    root = []
    ex_root = []
    f = open(dataname)
    lines = f.readlines()
    datalen = len(lines)
    f.close()
    data = np.zeros((datalen, 2))
    for i in range (datalen):
        ex_root.append(i)
        sp = lines[i].split()
        data[i,0] = sp[1]
        data[i,1] = sp[2]

    return data, datalen, root, ex_root

#グラハムスキャン
def convex(data):

    #y座標最小のものを探す
    min = 0
    for i in range(datalen):
        if (data[min, 1] > data[i, 1]):
            min = i
        elif (data[min, 1] == data[i, 1] and  data[min, 0] < data[i, 0]):
            min = i

    #反時計周りでの角度を調べる
    angle = np.zeros((datalen,2))
    for i in range(datalen):
        if (i == min):
            angle[i] = [0, i]
        else:
            theta = math.atan2((data[i, 1] - data[min, 1]), data[i, 0] - data[min, 0])
            if (theta < 0):
                theta = (2 * math.pi) + theta;
            angle[i] = [theta, i]

    #角度順にソート
    sorted = angle[angle[:,0].argsort(), :]

    stack = []
    stack.extend([sorted[0, 1], sorted[1, 1], sorted[2, 1]])

    for i in range(3, datalen):
        stacktop = len(stack)
        while(True):
            theta1 = math.atan2(data[int(stack[stacktop - 1]), 1] - data[int(stack[stacktop - 2]), 1],
                                data[int(stack[stacktop - 1]), 0] - data[int(stack[stacktop - 2]), 0])
            if (theta1 < 0): theta1 = 2 * math.pi + theta1
            theta2 = math.atan2(data[int(sorted[i, 1]), 1] - data[int(stack[stacktop - 1]), 1],
                                data[int(sorted[i, 1]), 0] - data[int(stack[stacktop - 1]), 0])
            if (theta2 <= 0): theta2 = 2 * math.pi + theta2
            if (theta2 - theta1 < 0):
                del stack[stacktop - 1]
                stacktop -= 1
            else:
                break
        stack.append(sorted[i, 1])

    for i in range (len(stack)):
        stack[i] = int(stack[i])
    return stack

#角度を計算
def angle(x, y):

    dot_xy = np.dot(x, y)
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos = dot_xy / (norm_x*norm_y)
    rad = np.arccos(cos)
    theta = rad * 180 / np.pi

    return theta

#最近挿入法
def insertion(root, ex_root):

    for i , number in enumerate(root):
        ex_root.remove(number)

    while (True):
        min = 0
        costratio = [0 for i in range(len(root))]
        minNum = [0 for i in range(len(root))]
        for i in range (len(root)):
            for j in range(0, len(ex_root)):
                if j == 0 or min > cal_cost(root[i - 1], root[i], ex_root[j]):
                    min = (cal_cost(root[i - 1], root[i], ex_root[j]))
                    minNum[i] = ex_root[j]
            costratio[i] = cal_costratio(root[i - 1],root[i], minNum[i])

        ratiomin = 9999
        ratiominNum = 0

        for i in range (len(root)):
            if ratiomin > costratio[i]:
                ratiomin = costratio[i]
                ratiominNum = i

        root.insert(ratiominNum, minNum[ratiominNum])
        ex_root.remove(minNum[ratiominNum])

        if not ex_root:
            break

    return root

#Nearest Neighbor法
def nearest_n(data, datalen, root, ex_root):

    root.append(0)
    ex_root.remove(0)

    for i in range(datalen - 1):
        min_len = 0
        min_Num = 0
        for j in range(len(ex_root)):
            if j == 0 or min_len > np.linalg.norm([data[root[i]] - data[ex_root[j]]]):
                print (ex_root[j])
                min_len = np.linalg.norm([data[root[i]] - data[ex_root[j]]])
                min_Num = ex_root[j]
        root.append(min_Num)
        ex_root.remove(min_Num)

    return root

#2-opt法
def opt_2(data, datalen, root):

    total = 0
    while True:
        count = 0
        for i in range(datalen - 2):
            i1 = i + 1
            for j in range(i + 2, datalen):
                if j == datalen - 1:
                    j1 = 0
                else:
                    j1 = j + 1
                if i != 0 or j1 != 0:
                    l1 = np.linalg.norm([data[root[i]] - data[root[i1]]])
                    l2 = np.linalg.norm([data[root[j]] - data[root[j1]]])
                    l3 = np.linalg.norm([data[root[i]] - data[root[j]]])
                    l4 = np.linalg.norm([data[root[i1]] - data[root[j1]]])
                    if l1 + l2 > l3 + l4:
                        new_root = root[i1:j+1]
                        root[i1:j+1] = new_root[::-1]
                        count += 1
        total += count
        print (root)
        if count == 0: break

    return root

#追加コストを計算
def cal_cost(i,j,k):
    return np.linalg.norm([data[i] - data[k]]) + np.linalg.norm([data[k] - data[j]])\
           - np.linalg.norm([data[i] - data[j]])

#コスト比を計算
def cal_costratio(i,j,k):
    return (np.linalg.norm([data[i] - data[k]]) + np.linalg.norm([data[k] - data[j]])) / np.linalg.norm([data[i] - data[j]])

#総コスト計算
def cal_totalcost(data, root):
    totalcost = 0
    for i in range(len(root)):
        totalcost += np.linalg.norm(([data[root[i]] - data[root[i-1]]]))
    return totalcost

#図にプロット
def autoplot(root):
    plt.scatter(data[:, 0], data[:, 1])
    initnum = 0
    beforenum = 0
    for i, number in enumerate(root):
        plt.scatter(data[int(number), 0], data[int(number), 1], c='red')
        if i == 0:
            beforenum = number
            initnum = number
        else:
            plt.plot([data[int(beforenum), 0], data[int(number), 0]], [data[int(beforenum), 1], data[int(number), 1]], 'r')
            beforenum = number

    plt.plot([data[int(beforenum), 0], data[int(initnum), 0]], [data[int(beforenum), 1], data[int(initnum), 1]], 'r')
    plt.show()
    plt.close()

if __name__ == '__main__':

    dataname = 'berlin52.txt'
    type = 4  #1: NN法、2: CHI法、3: NN法＋2-opt法、
                #4:CHI法＋2-opt法
    data, datalen, root, ex_root = init_data(dataname)

    if type == 1:
        root = nearest_n(data, datalen, root, ex_root)
    elif type == 2:
        root = convex(data)
        root = insertion(root, ex_root)
    elif type == 3:
        root = nearest_n(data, datalen, root, ex_root)
        root = opt_2(data, datalen, root)
    elif type == 4:
        root = convex(data)
        root = insertion(root, ex_root)
        root = opt_2(data, datalen, root)

    print (cal_totalcost(data, root))
    autoplot(root)




