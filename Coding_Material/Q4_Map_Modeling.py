import numpy as np
from math import *
import pandas as pd
import networkx

# 基本参数设置
theta = radians(120)  # 表示测量张角
alpha = radians(1.5)  # 表示海底平面斜坡坡度
beta = radians(90)  # 表示法向量的投影和测线方向的夹角
alpha_ = atan(tan(alpha) * sin(beta))  # 表示等效的\alpha大小
gamma = cos(theta / 2 + alpha_) / (cos(theta / 2 + alpha_) + cos(theta / 2 - alpha_))  # 表示宽度在当前行进方向的左右分布系数（表示deep的部分）
Height = 5 * 1852  # 表示的是地图的长度（单位：m）x
Width = 4 * 1852  # 表示的是地图的宽度（单位：m）y
Step = 0.02 * 1852  # 表示的是各单位的移动步长（单位：m）


class Map:

    def __init__(self) -> None:
        self.width_map = np.zeros((251, 201), dtype=tuple)
        self.road_map = np.zeros((251, 201))
        self.valid_map = np.zeros((251, 201),dtype=int)
        self.depth = self.get_depth()
        self.vector_map = np.zeros((251,201),dtype=list)
    
    # 获得每个点的深度矩阵
    def get_depth(self):
        excel_file = "C:\\Users\\Slater\\Desktop\\Math\\B题\\附件1.xlsx"
        # 使用pandas的read_excel函数读取数据
        df = pd.read_excel(excel_file, header=1, index_col=1)
        z = df.values[0:, 1:].astype('float')
        return np.array(z)

    # 获得点在当前方向的宽度
    def get_width_by_raw_and_col(self, x, y):
        return self.width_map[x, y]

    # 表示是否被标记
    def set_valid_map(self, x, y) -> int:
        # x = np.array(x)
        # y = np.array(y)
        # for i in x:
        #     for j in y:
        x = int(x)
        y = int(y)
        self.valid_map[x, y] += 1
        return self.valid_map[x, y]

    # 标记是合法的路径
    def set_road_map(self, x, y) -> bool:
        if self.road_map[x, y] == 1:
            return False
        self.road_map[x, y] = 1
        return True

    # 设置深度的数据
    def set_width_map(self, x, y, value_left, value_right) -> bool: 
        x = int(x)
        y = int(y)
        # print(x,y)
        self.width_map[x, y] = (value_left, value_right)
        # print(self.width_map)
        return True
