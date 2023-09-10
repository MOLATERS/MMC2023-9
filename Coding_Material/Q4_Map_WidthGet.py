from Q4_Map_Modeling import *
from math import *
from Q4_SetNormalVector import *
import numpy as np

# 基本参数设置
theta = radians(120)  # 表示测量张角
alpha = np.zeros((Raw_Number, Col_Number))  # 表示海底平面斜坡坡度
beta = np.zeros((Raw_Number, Col_Number))  # 表示法向量的投影和测线方向的夹角
alpha_ = np.zeros((Raw_Number, Col_Number))  # 表示等效的\alpha大小
gamma = np.zeros((Raw_Number, Col_Number))  # 表示宽度在当前行进方向的左右分布系数（表示deep的部分）
Height = 5 * 1852  # 表示的是地图的长度（单位：m）x
Width = 4 * 1852  # 表示的是地图的宽度（单位：m）y
Step = 0.02 * 1852 / raw_divide  # 表示的是各单位的移动步长（单位：m）
Map = Map()  # 初始化扫描地图
Ita = []  # 记录出现过的重复率
W = np.zeros((Raw_Number, Col_Number))  # 表示存储宽度的矩阵
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

# 读取向量


def ReadVectors():
    normals = set_normal_vector()
    for i in range(len(normals)):
        raw = i // 201
        col = i % 201
        for k in range(raw_divide):
            for t in range(col_divide):
                Map.vector_map[raw*raw_divide+k][col*col_divide+t] = normals[i]
    return normals

# 计算出角度


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

# 计算角度的函数


def Calculate_angle(vector1, vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    l_x = sqrt(vector1.dot(vector1))
    l_y = sqrt(vector2.dot(vector2))
    dian = vector1.dot(vector2)
    cos_ = dian / (l_x * l_y)
    angle = acos(cos_)
    return angle

# 计算W的函数


def Calculate_W(theta, raw, col):
    D = Map.depth
    w = sin(theta)*cos(alpha_[raw, col])**2/(cos(theta/2 -
                                                 alpha_[raw, col])*cos(theta/2+alpha_[raw, col])) * D[raw, col]
    return w

# 文件存储函数


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace(
            '[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")

# 计算宽度函数


def Calculate_Width():
    ReadVectors()
    H = len(Map.vector_map)
    W_ = len(Map.vector_map[0])
    for i in range(0,raw_block):
        for j in range(0,col_block):
            for k in range(0,raw_divide):
                for t in range(0,col_divide):
                    beta[i*raw_divide+k, j*raw_divide+t], alpha[i*raw_divide+k, j*col_divide+t] = Calculate_alpha_beta(Map.vector_map[i*raw_divide+k, j*col_divide+t], "Verticle")
                    alpha_[i*raw_divide+k, j*col_divide+t] = atan(tan(alpha[i*raw_divide+k, j*col_divide+t])*(sin(beta[i*raw_divide+k, j*raw_divide+t])))
                    gamma[i*raw_divide+k, j*col_divide+t] = cos(theta/2+alpha_[i*raw_divide+k, j*col_divide+t]) / \
                        (cos(theta/2+alpha_[i*raw_divide+k, j*col_divide]) + cos(theta/2-alpha_[i*raw_divide+k, j*col_divide]))                    
                    Get_width(theta, i*raw_divide+k, j*col_divide+t, gamma)
    return Map.width_map

# 展示矩阵


def ShowArray(array):
    array = np.array(array)
    for i in range(len(array)):
        print(array[i, :])
