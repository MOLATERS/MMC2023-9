import math 
import matplotlib.pyplot as plt
theta = math.radians(120)
alpha = math.radians(1.5)
d = 200
D = []
W = []
l = []
x = []
y = []
eta = []

for i in range(1, 10):
    l.append((i-5) * d)
    D.append(70 - (i-5) * d * math.tan(alpha))
    x.append(math.sin(theta/2) * D[i-1] / math.sin(math.pi/2-theta/2-alpha))
    y.append(math.sin(theta/2) * D[i-1] / math.sin(math.pi/2-theta/2+alpha))
    W.append(math.sin(theta) * math.cos(alpha)**2 * (70 - (i-5) * d * math.tan(alpha)) / (math.cos(theta/2-alpha) * math.cos(theta/2+alpha)))

for i in range(1, 9):
    eta.append(float(((x[i]+y[i-1]) * math.cos(alpha) - d) / W[i-1]))

plt.figure(1)
plt.plot(l, W)
plt.xlabel('$l(m)$')
plt.ylabel('$W(m)$')
plt.grid()
plt.show()
plt.figure(2)
plt.plot(l[1:], eta)
plt.xlabel('$l(m)$')
plt.ylabel('$\\eta$')
plt.grid()
plt.show()

