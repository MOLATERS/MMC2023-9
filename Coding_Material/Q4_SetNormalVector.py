# 实现PCA分析和法向量计算，并加载数据集中的文件进行验证
import open3d as o3d
import numpy as np
from pyntcloud import PyntCloud
from pandas import DataFrame


# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

def PCA(data, correlation=False, sort=True):
    # data => (10000, 3)  data_mean => (1, 3)
    data_mean = np.mean(data, axis=0)  # 对列求均值
    # normalize_data => (10000, 3)
    normalize_data = data - data_mean  # 数据归一化操作
    # H => (3, 3)
    H = np.dot(normalize_data.transpose(), normalize_data)
    # eigenvectors => (3,3)  eigenvalues => (3,)  eigenvectors_transpose => (3,3)
    eigenvectors, eigenvalues, eigenvectors_transpose = np.linalg.svd(H)  # SVD分解
    # 将特征值从大到小进行排序，便于提取主成分向量
    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors, normalize_data


def set_normal_vector():
    raw_point_cloud_matrix = np.loadtxt('C:\\Users\\Slater\\Desktop\\Math\\Coding_Material\\data.txt')
    raw_point_cloud_matrix_part = raw_point_cloud_matrix[:, 0:3]
    raw_point_cloud = DataFrame(raw_point_cloud_matrix_part)  # 选取每一列的第0至第2个元素
    raw_point_cloud.columns = ['x', 'y', 'z']
    point_cloud_pynt = PyntCloud(raw_point_cloud)
    point_cloud_o3d = point_cloud_pynt.to_instance("open3d", mesh=False)
    eigenvalues, eigenvectors, normalize_data = PCA(raw_point_cloud_matrix_part)
    vector = np.mat(eigenvectors[:, 0:2])
    vector_transpose = vector.transpose()
    primary_orientation_ = eigenvectors[:, 0]
    second_orientation = eigenvectors[:, 1]
    point = [[0, 0, 0], primary_orientation_, second_orientation]
    lines = [[0, 1], [0, 2]]
    colors = [[1, 0, 0], [0, 1, 0]]
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(point), lines=o3d.utility.Vector2iVector(lines))
    line_set.colors = o3d.utility.Vector3dVector(colors)
    # 循环计算每个点的法向量
    # *********************************************************************************
    # 从点云中获取点，只对点进行处理
    points = point_cloud_pynt.points
    # print('total points number is:', points.shape[0])
    normals = []
    # 由于最近邻搜索，此处允许直接调用open3d中的函数
    pcd_tree = o3d.geometry.KDTreeFlann(point_cloud_o3d)
    # 每一点的法向量计算，通过PCA降维，对应最小特征值的成分向量近似为法向量
    for i in range(points.shape[0]):
        [_, idx, _] = pcd_tree.search_knn_vector_3d(point_cloud_o3d.points[i], 15)
        k_nearest_point = np.asarray(point_cloud_o3d.points)[idx, :]
        w, v, _ = PCA(k_nearest_point)
        normals.append(v[:, 2])
        # if i%100==0:
        #    print(normals[i])
    normals = np.array(normals, dtype=np.float64)
    # 此处把法向量存放在了normals中
    point_cloud_o3d.normals = o3d.utility.Vector3dVector(normals)
    # 法向量可视化，根据open3d文档，需要在显示窗口按住键'n'才可以看到法向量
    # o3d.visualization.draw_geometries([point_cloud_o3d])
    return normals
