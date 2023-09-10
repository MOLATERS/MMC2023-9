import numpy as np
import math

# 问题1计算出Wn
def calculate_Wn_1(y_position):
    theta = math.radians(120)
    alpha = math.radians(1.5)
    Depth = 2 * 1852 * math.tan(math.radians(1.5)) + 110 - y_position * math.tan(math.radians(1.5))
    # print(Depth)
    W = math.sin(theta) * math.cos(alpha)**2 * Depth / (math.cos(theta/2-alpha) * math.cos(theta/2+alpha))
    return W

# print(calculate_Wn_1(2*1852))


#记录每单位的移动对应的测量数量
# def detect_array():
#     detect_array = []
#     for i in range(0,L,step):
#         detect_array.append((i,detect_width(i)))
#     return detect_array
