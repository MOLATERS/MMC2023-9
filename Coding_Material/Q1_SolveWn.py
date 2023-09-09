## 实现方法
import math

def calculate_Wn(alpha, theta, Dn):
    numerator = math.sin(theta/2) / math.sin((math.pi - theta)/2 - alpha) + math.sin(theta/2) / math.sin((math.pi- theta)/2 + alpha)
    # 计算Wn
    Wn = Dn * numerator * math.cos(alpha)
    return Wn
import numpy as np
import matplotlib.pyplot as plt 

x=[1,2,3,1.5,4,2.5,6,4,3,5.5,5,2]
y=[3,4,8,4.5,10,5,15,9,5,16,13,3]

plt.scatter(x,y,color="red")
plt.title("Scatter Plot of the data")
plt.xlabel("X")
plt.ylabel("Y")

linear_model=np.polyfit(x,y,1)
linear_model_fn=np.poly1d(linear_model)
x_s=np.arange(0,7)
plt.plot(x_s,linear_model_fn(x_s),color="green")

plt.show()
# 示例用法
alpha = 1.5  # 你的alpha值
theta = 120 # 你的theta值
Dn = 70 # 你的Dn值

result = calculate_Wn(math.radians(alpha), math.radians(theta), Dn)
print("Wn =", result)

