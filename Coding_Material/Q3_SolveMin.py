import numpy as np
from scipy.optimize import minimize
import math

# 定义目标函数
def objective(n):
    return n

# 定义约束条件
def constraint1(n, D, y, gamma, L):
    n = int(n)
    Wi = np.zeros(n + 1)  # 初始化Wi数组
    delta = np.zeros(n)   # 初始化delta数组
    # 计算Wi和delta数组
    for i in range(int(n)):
        Wi[i] = ((np.sin(theta / 2) / np.sin((np.pi - theta) / 2 - alpha)) +
                 (np.sin(theta / 2) / np.sin((np.pi - theta) / 2 + alpha))) * D[i]
        delta[i] = y[i] + Wi[i] * (1 - gamma) - (y[i + 1] - Wi[i + 1] * gamma)

    # 返回约束条件的结果
    return np.sum(Wi) - np.sum(delta) - L

def constraint2(n, D, y, gamma):
    n = int(n)
    return y[0] - (D[0] * gamma)

def constraint3(n, D, y, gamma, L):
    n = int(n)
    Wi = np.zeros(n + 1)  # 初始化Wi数组

    # 计算最后一个Wi
    Wi[n] = ((np.sin(theta / 2) / np.sin((np.pi - theta) / 2 - alpha)) +
              (np.sin(theta / 2) / np.sin((np.pi - theta) / 2 + alpha))) * D[n]

    return L - y[n] - (Wi[n] * (1 - gamma))

def constraint4(n, delta, Wi):
    n = int(n)
    for i in range(n):
        if not (0.1 <= delta[i] / Wi[i] <= 0.2):
            return delta[i] / Wi[i] - 0.2
    return 0

def constraint5(n, delta, Wi):
    n = int(n)
    for i in range(n):
        if not (0.1 <= delta[i] / Wi[i + 1] <= 0.2):
            return delta[i] / Wi[i + 1] - 0.2
    return 0

def constraint6(delta):
    return delta  # delta必须非负

# 初始化参数
n0 = 1
theta = np.deg2rad(1.5)
alpha = np.deg2rad(0)
L = 1825 * 4
n = 20  # 可以根据需要设置n的初始值
y = np.linspace(0, L, n + 1)  # 初始化y数组
D = y * math.tan(math.radians(1.5)) - 2*1850*math.tan(math.radians(1.5)) +110  # 初始化D数组
numerator = math.sin(theta/2) / math.sin((math.pi - theta)/2 - alpha) + math.sin(theta/2) / math.sin((math.pi- theta)/2 + alpha)
    # 计算Wn
Wi = D * numerator * math.cos(alpha)
gamma = np.sin(np.deg2rad(61.5)) / (np.sin(np.deg2rad(61.5)) + np.sin(np.deg2rad(58.5)))


# 最小化目标函数
constraints = [
    {'type': 'eq', 'fun': constraint1, 'args': (D, y, gamma, L)},
    {'type': 'eq', 'fun': constraint2, 'args': (D, y, gamma)},
    {'type': 'eq', 'fun': constraint3, 'args': (D, y, gamma, L)},
    {'type': 'ineq', 'fun': constraint4, 'args': (D, y)},
    {'type': 'ineq', 'fun': constraint5, 'args': (D, y)},
    {'type': 'ineq', 'fun': constraint6},
]

result = minimize(objective, n0, constraints=constraints)

# 输出结果
print("最小值n:", result.x[0])
