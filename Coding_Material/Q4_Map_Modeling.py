import numpy as np
from math import *
import pandas as pd
import networkx

Raw_Number = int(251) * int(4)
Col_Number = int(201) * int(4)
raw_divide = col_divide = int(4)

raw_block = Raw_Number // raw_divide
col_block = Col_Number // col_divide


class Map:

    def __init__(self) -> None:
        self.width_map = np.zeros((Raw_Number, Col_Number), dtype=tuple)
        self.road_map = np.zeros((Raw_Number, Col_Number))
        self.valid_map = np.zeros((Raw_Number, Col_Number),dtype=int)
        self.depth = self.get_depth()
        self.vector_map = np.zeros((Raw_Number,Col_Number),dtype=list)
    
    # 获得每个点的深度矩阵
    def get_depth(self):
        excel_file = "C:\\Users\\Slater\\Desktop\\Math\\B题\\附件1.xlsx"
        # 使用pandas的read_excel函数读取数据
        df = pd.read_excel(excel_file, header=1, index_col=1)
        z = df.values[0:, 1:].astype('float')
        z_ = np.zeros((Raw_Number,Col_Number))
        for i in range(0,raw_block):
            for j in range(0,col_block):
                for t in range (0,raw_divide):
                    for k in range (0,col_divide):
                        z_[i*raw_divide+t,j*col_divide+k] += z[i,j]
        return z_

    # 获得点在当前方向的宽度
    def get_width_by_raw_and_col(self, x, y):
        return self.width_map[x, y]

    # 表示是否被标记
    def set_valid_map(self, x, y) -> int:
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
