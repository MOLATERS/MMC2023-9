import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

theta = 120 * np.pi / 180
alpha = 1.5 * np.pi / 180
beta = np.arange(0, 361, 5) * np.pi / 180
alpha_ = np.arctan(np.tan(alpha) * np.sin(beta))
D = np.arange(75, 75.5,0.05)
W = np.zeros((len(beta), len(D)))

for i in range(len(beta)):
    for j in range(len(D)):
        W[i, j] = np.sin(theta) * np.cos(alpha_[i]) ** 2 / (np.cos(theta / 2 - alpha_[i]) * np.cos(theta / 2 + alpha_[i])) * D[j]

beta = beta * 180 / np.pi
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
beta, D = np.meshgrid(beta, D)
ax.plot_surface(beta, D, W.T, linewidth=0, antialiased=False,shade =True, alpha = 0.5,cmap='cool')
ax.set_xlabel('$\\beta(degree)$')
ax.set_ylabel('$D(m)$')
ax.set_zlabel('$W(m)$')
plt.show()