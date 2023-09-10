from Q4_Map_WidthGet import *
import matplotlib.pyplot as plt
import seaborn as sns
percent = 0.40 # 用于记录ita限高

# 寻路算法
def find_path(Direction,percent):
    if (Direction == 'Verticle'):
        # 各种变量的初始化
        left_edge = 0
        right_edge = Width
        road_map = np.zeros((Raw_Number,Col_Number))
        ita = -999
        for col in range(0, Col_Number):
            valid_map = np.copy(Map.valid_map)  # 将valid_map进行复制
            road_map = np.copy(Map.road_map)  # 得到路径地图
            Ita_temp = []
            for raw in range(0, Raw_Number):
                i = col * Step  # 表示y的数值
                j = raw * Step  # 表示x的数值
                raw = int(raw)
                col = int(col)
                
                # 检查当前区域是否被检测到过
                if Map.valid_map[raw][col] == 0:
                    road_map[raw][col] = 1  # 设置当前的节点为路径节点
                    width = Map.get_width_by_raw_and_col(raw, col)  # 得到宽度
                    left_edge_math = i - width[0] # 表示左侧的具体值
                    right_edge_math = i + width[1] # 表示右侧的具体值
                    left_edge = int(left_edge_math//Step) if left_edge_math >= 0 else 0  # 左位置
                    right_edge = int(right_edge_math//Step) if right_edge_math <= Width else int(Width//Step-1)  # 右位置
                    left_edge = left_edge + 1 if left_edge*Step<left_edge else left_edge
                    right_edge = right_edge + 1 if right_edge*Step<right_edge else right_edge
                    
                    # 找到并修改成已经检查的区域块
                    change_node = range(left_edge, right_edge+1)
                    for c in change_node:
                        valid_map[raw][c] += 1

                    # 检查重叠率
                    for t in range(1, col+1):
                        if ( int(road_map[raw][col-t]) == 1 ):
                            left_node_width = Map.get_width_by_raw_and_col(raw, col-t)
                            delta = (col-t)*Step+left_node_width[1]-left_edge_math
                            # delta = 
                            ita = delta / sum(left_node_width)
                            break
                    
                    # 判断选择是否合法
                    Ita_temp.append(ita)
                    if ita >= percent:
                        break
                else:
                    break
            # 判断当前路径是否能够到
            if (raw == Raw_Number-1):
                Map.road_map = np.copy(road_map)
                Map.valid_map = np.copy(valid_map)
                Ita.append(Ita_temp)
        return
    
    elif (Direction == "Horizen"):
        # 各种变量的初始化
        up_edge = 0
        down_edge = Width
        road_map = np.zeros((Raw_Number,Col_Number))
        ita = -999
        for raw in range(0, Raw_Number):
            valid_map = np.copy(Map.valid_map)  # 将valid_map进行复制
            road_map = np.copy(Map.road_map)  # 得到路径地图
            Ita_temp = []
            for col in range(0, Col_Number):
                i = col * Step  # 表示y的数值
                j = raw * Step  # 表示x的数值
                raw = int(raw)
                col = int(col)
                
                # 检查当前区域是否被检测到过
                if Map.valid_map[raw][col] == 0:
                    road_map[raw][col] = 1  # 设置当前的节点为路径节点
                    width = Map.get_width_by_raw_and_col(raw, col)  # 得到宽度
                    up_edge_math = j - width[0] # 表示左侧的具体值
                    down_edge_math = j + width[1] # 表示右侧的具体值
                    up_edge = int(up_edge_math//Step) if up_edge_math >= 0 else 0  # 左位置
                    down_edge = int(down_edge_math//Step) if down_edge_math <= Height else int(Height//Step-1)  # 右位置
                    up_edge = up_edge + 1 if up_edge*Step<up_edge else up_edge
                    down_edge = down_edge + 1 if down_edge*Step<down_edge else down_edge
                    
                    # 找到并修改成已经检查的区域块
                    change_node = range(up_edge, down_edge+1)
                    for c in change_node:
                        valid_map[c][col] += 1

                    # 检查重叠率
                    for t in range(1, raw+1):
                        if ( int(road_map[raw-t][col]) == 1 ):
                            up_node_width = Map.get_width_by_raw_and_col(raw-t, col)
                            delta = (raw-t) * Step + up_node_width[1] - up_edge_math
                            # delta = 
                            ita = delta / sum(up_node_width)
                            break
                    
                    # 判断选择是否合法
                    Ita_temp.append(ita)
                    if ita >= percent:
                        break
                else:
                    break
            # 判断当前路径是否能够到
            if (col == Col_Number-1):
                Map.road_map = np.copy(road_map)
                Map.valid_map = np.copy(valid_map)
                Ita.append(Ita_temp)
        return

def Calculate_Cover():
    count = 0
    for i in range(len(Map.valid_map)):
        for j in range(len(Map.valid_map[0])):
            if(Map.valid_map[i][j] != 0):
                count+=1
    return count*Step**2/(Width*Height)

def Calculate_Ita():
    count = 0
    count_ita = 0
    for item in Ita:
        for i in item:
            count_ita+=1
            if i > 0.2:
                count+=1
    return count / count_ita,count

def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace(
            '[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")
    
def Calculate_Path():
    count = 0
    for j in range(len(Map.road_map[0])):
            if(Map.road_map[0][j] == 1):
                count+=1
    return count

def Calculate_Path_2():
    count = 0
    for j in range(len(Map.road_map)):
        if(Map.road_map[j][0] == 1):
            count+=1
    return count

Calculate_Width()
find_path("Horizen",percent)
# text_save("map_verticle.txt", Map.valid_map.astype(int) + Map.road_map.astype(int)*3)
i_ta,count= Calculate_Ita()
cover =Calculate_Cover()
path_number = Calculate_Path_2()
# text_save("map_verticle_ita.txt",
#           [f"超过20%的部分:{i_ta},\n覆盖率:{cover},\n超过20%的长度:{i_ta*Step},\n一共有{path_number}条路，\n设置参数为percent(阈值):{percent}\n分割的数目为{raw_divide}*{col_divide}"])
print(f"超过20%的部分:{i_ta},\n覆盖率:{cover},\n超过20%的长度:{count*Step},\n一共有{path_number}条路{path_number*Height},\n设置参数为percent(阈值):{percent}\n分割的数目为{raw_divide}*{col_divide}")
sns.heatmap(Map.valid_map.astype(int) + Map.road_map.astype(int)*3,cmap="coolwarm")
# # print(Calculate_Cover())
# # print(Calculate_Ita())
plt.axis('off')
plt.show()


