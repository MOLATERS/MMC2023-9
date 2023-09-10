from Q4_Map_Modeling import *
from math import *
from Q4_SetNormalVector import *
import numpy as np
# 基本参数设置
theta = radians(120)  # 表示测量张角
alpha = np.zeros((251, 201))  # 表示海底平面斜坡坡度
beta = np.zeros((251, 201))  # 表示法向量的投影和测线方向的夹角
alpha_ = np.zeros((251, 201))  # 表示等效的\alpha大小
gamma = np.zeros((251, 201))  # 表示宽度在当前行进方向的左右分布系数（表示deep的部分）
Height = 5 * 1852  # 表示的是地图的长度（单位：m）x
Width = 4 * 1852  # 表示的是地图的宽度（单位：m）y
Step = 0.02 * 1852  # 表示的是各单位的移动步长（单位：m）
Map = Map()  # 初始化扫描地图
Ita = []  # 记录出现过的重复率
W = np.zeros((251, 201))  # 表示存储宽度的矩阵
# 记录从什么位置进行寻路

# 定位参数设置 注意这里输入的是对应的模块坐标


def Get_width(theta, x_position, y_position, gamma):
    raw = x_position
    col = y_position
    raw = int(raw)
    col = int(col)
    width = Calculate_W(theta, raw, col)  # 这里需要加上对应的函数
    Map.set_width_map(
        raw, col, width*gamma[raw, col], width*(1-gamma[raw, col]))
    return raw, col, width*gamma[raw, col], width*(1-gamma[raw, col])


# 寻路算法
def find_path(Direction):
    if (Direction == 'Verticle'):
        left_edge = 0
        right_edge = Width
        road_map = np.zeros((251, 201))
        for col in range(0, 201):
            road_map = np.copy(Map.road_map)  # 得到路径地图
            for raw in range(0, 251):
                i = col * Step  # 表示y的数值
                j = raw * Step  # 表示x的数值
                raw = int(raw)
                col = int(col)
                # 检查当前区域是否被检测到过
                if Map.valid_map[raw][col] == 0:
                    road_map[raw][col] = 1  # 设置当前的节点为路径节点
                    width = Map.get_width_by_raw_and_col(raw, col)  # 得到宽度
                    left_area = width[0] // Step
                    right_area = width[1] // Step
                    left_edge_math = i - width[0]  # 表示左侧的具体值
                    right_edge_math = i + width[1]  # 表示右侧的具体值
                    left_edge = col - left_area if col > left_area else 0  # 左位置
                    right_edge = col + right_area if col + \
                        right_area < Width // Step else (Width // Step)-1  # 右位置
                    left_edge = int(left_edge)
                    right_edge = int(right_edge)
                    # 找到并修改成已经检查的区域块
                    change_node = np.arange(left_edge, right_edge+1)
                    for c in change_node:
                        Map.set_valid_map(raw, c)

                    # 检查重叠率
                    for t in range(left_edge, col):
                        if (road_map[raw][t] == 1):
                            left_node_width = Map.get_width_by_raw_and_col(
                                raw, t)
                            ita = (t*Step+left_node_width[1]-(i-left_edge_math)) / (
                                left_node_width[0]+left_node_width[1])
                            if ita >= 0.2:
                                break
                            Ita.append(ita)
                else:
                    break
            if (raw == 251):
                Map.road_map = np.copy(road_map)
        return
    elif (Direction == "Horizen"):
        for j in np.arange(0, Height+1, Step):
            road_map = Map.road_map  # 得到路径地图
            for i in np.arange(0, Width+1, Step):
                col = i // Step  # 设置对应的列
                raw = j // Step  # 设置对应的行

                # 检查当前区域是否被检测到过
                if (Map.valid_map[raw][col] == 0):
                    road_map[raw][col] = 1  # 设置当前的节点为路径节点
                    width = Map.get_width_by_raw_and_col(raw, col)  # 得到宽度
                    up_area = width[0] // Step  # 得到左侧宽度
                    down_area = width[1] // Step  # 得到右侧宽度
                    up_edge = col - up_edge if col > up_area else 0  # 左位置
                    down_edge = col + down_edge if col + \
                        down_area < Height//Step else Height//Step-1  # 右位置

                    # 找到并修改成已经检查的区域块
                    change_node = np.arange(down_edge, up_edge)
                    Map.set_valid_map(change_node, col)

                    # 检查重叠率
                    for t in range(down_edge, raw):
                        if (road_map[t][col] == 1):
                            down_node_width = Map.get_width_by_raw_and_col(
                                t, col)
                            ita = (t + down_node_width[1]-down_edge) / \
                                (down_node_width[0] + down_node_width[1])
                            if ita >= 0.2:
                                break
                            else:
                                if (t == Width):
                                    Map.road_map = road_map
                            Ita.append(ita)
                else:
                    break
        return


def ReadVectors():
    normals = set_normal_vector()
    for i in range(len(normals)):
        raw = i // 201
        col = i % 201
        Map.vector_map[raw][col] = normals[i]
    return normals


def Calculate_alpha_beta(Normal_vector, Direction):
    line_direction = np.zeros(3)
    if (Direction == "Verticle"):
        line_direction = np.array((1, 0, 0))
    elif (Direction == "Horizen"):
        line_direction = np.array((0, 1, 0))
    z = np.array((0, 0, 1))
    b = np.array((Normal_vector[0], Normal_vector[1], 0))
    n = np.array((Normal_vector[0], Normal_vector[1], Normal_vector[2]))
    cal_beta = Calculate_angle(line_direction, b)
    cal_alpha = Calculate_angle(n, z)
    return cal_beta, cal_alpha


def Calculate_angle(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    l_x = sqrt(vector1.dot(vector1))
    l_y = sqrt(vector2.dot(vector2))
    dian = vector1.dot(vector2)
    cos_ = dian / (l_x * l_y)
    angle = acos(cos_)
    return angle


def Calculate_W(theta, raw, col):
    D = Map.depth
    w = sin(theta)*cos(alpha_[raw, col])**2/(cos(theta/2 -
                                                 alpha_[raw, col])*cos(theta/2+alpha_[raw, col])) * D[raw, col]
    return w


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace(
            '[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")


def Calculate_Width():
    ReadVectors()
    H = len(Map.vector_map)
    W_ = len(Map.vector_map[0])
    for i in range(H):
        for j in range(W_):
            beta[i, j], alpha[i, j] = Calculate_alpha_beta(
                Map.vector_map[i, j], "Verticle")
            alpha_[i, j] = atan(tan(alpha[i, j])*(sin(beta[i, j])))
            gamma[i, j] = cos(theta/2+alpha_[i, j]) / \
                (cos(theta/2+alpha_[i, j]) + cos(theta/2-alpha_[i, j]))
            Get_width(theta, i, j, gamma)
    return Map.width_map


def ShowArray(array):
    array = np.array(array)
    for i in range(len(array)):
        print(array[i, :])


Calculate_Width()
find_path("Verticle")
map = Map.road_map
print(map)
print(len(map), len(map[0]))
