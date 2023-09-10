import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 指定Excel文件的路径
excel_file = "C:\\Users\\Slater\\Desktop\\Math\\B题\\附件1.xlsx"

# 使用pandas的read_excel函数读取数据
df = pd.read_excel(excel_file, header=1, index_col=1)
z = df.values[0:, 1:].astype('float')

# 生成x, y坐标
x = np.linspace(0, 4, z.shape[1])
y = np.linspace(5, 0, z.shape[0])
x, y = np.meshgrid(x, y)

# 生成颜色映射
cmap = cm.get_cmap('jet')

# 根据z数据生成颜色值
z = -z
# 注意深度的表示
z_min = np.min(z)
z_max = np.max(z)
normalized_z = (z - z_min) / (z_max - z_min)  # 将z数据归一化到[0, 1]范围
color = cmap(normalized_z)  # 根据归一化后的z值获取颜色

# 绘制三维图形
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z,linewidth=0, antialiased=False,shade =True, alpha = 0.5,facecolors=color)
# 设置坐标轴标签
ax.set_xlabel('$x(m)$')
ax.set_ylabel('$y(m)$')
ax.set_zlabel('$Depth(m)$')

# 显示图形
plt.show()