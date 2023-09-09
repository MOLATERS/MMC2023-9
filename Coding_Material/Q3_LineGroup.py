import numpy as np
import matplotlib.pyplot as plt
from Q3_basic_math import calculate_Wn_1
import math

# 设置宽度左右两边的比例关系
west_width_percent = math.sin(math.radians(61.5))/(math.sin(math.radians(61.5))+math.sin(math.radians(58.5)))
 
# 设置计算出来的宽度
def dedect_width(y_position):
    return calculate_Wn_1(y_position)

# 计算出可能的n的数量
def Calculate_lines():
    yn_1_west_decide = 0;
    yn_west_decide = 0;
    # while yn_1_west_decide < 4 * 1825:
        