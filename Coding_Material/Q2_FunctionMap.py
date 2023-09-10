import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.ndimage import gaussian_filter1d

theta = 120*np.pi/180
alpha = 1.5*np.pi/180
beta = np.arange(0, math.radians(360), math.radians(5))
alpha_ = np.arctan(np.tan(alpha)*(np.sin(beta)))


d = 200
D = np.zeros((72, len(alpha_)))
W = np.zeros((len(alpha_), 72))
l = np.zeros(72)
for i in range(72):
    l[i] = i*d
    for j in range(len(alpha_)):
        D[i, j] = 120 - i*d*np.tan(alpha_[j])

W = np.sin(theta)*np.cos(alpha_)**2/(np.cos(theta/2-alpha_)*np.cos(theta/2+alpha))*D


fig2 = plt.figure(1)
# y_smoothed = gaussian_filter1d(W[:,4], sigma=5)
plt.grid()
# plt.plot(beta*180/math.pi, W[:,0])
plt.plot(l, W[:,55])
plt.xlabel('$l(M)$')
# plt.xlabel('$\\beta (degree)$')
plt.ylabel('$W(m)$')


beta, l = np.meshgrid(beta, l)
fig = plt.figure(2)
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X=beta*180/math.pi,Y=l,Z=W,cmap='cool',linewidth=0, antialiased=False,shade =True, alpha = 0.5)
ax.set_xlabel('$\\beta(degree)$')
ax.set_ylabel('$l(m)$')
ax.set_zlabel('$W(m)$')
plt.show()
