import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

width = np.linspace(0, 4 * 1852, 100)
height = np.linspace(0, 2 * 1852, 100)
x, y = np.meshgrid(width, height)

z = y * math.tan(math.radians(1.5)) - 2*1850*math.tan(math.radians(1.5)) +110

# 生成颜色映射
cmap = cm.get_cmap('jet')

# 根据z数据生成颜色值
z_min = np.min(z)
z_max = np.max(z)
normalized_z = (z - z_min) / (z_max - z_min)  # 将z数据归一化到[0, 1]范围
color = cmap(normalized_z)  # 根据归一化后的z值获取颜色

# 绘制三维图形
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z,linewidth=0, antialiased=False,shade =True, alpha = 0.5,cmap='cool')
# 设置坐标轴标签
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel('Depth')

plt.show()