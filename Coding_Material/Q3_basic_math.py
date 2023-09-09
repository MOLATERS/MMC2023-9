import numpy as np
import math

# 问题1计算出Wn
def calculate_Wn_1(y_position):
    theta = math.radians(120)
    alpha = math.radians(1.5)
    W = math.sin(theta) * math.cos(alpha)**2 * (70 - y_position * math.tan(alpha)) / (math.cos(theta/2-alpha) * math.cos(theta/2+alpha))
    return W
# W = math.sin(theta) * math.cos(alpha)**2 * (70 - y_position * math.tan(alpha)) / (math.cos(theta/2-alpha) * math.cos(theta/2+alpha))

