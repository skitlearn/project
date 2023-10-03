# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn import ensemble
from sklearn import svm
from sklearn import neighbors
import joblib
from sklearn.gaussian_process import GaussianProcessRegressor
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import mean_squared_error,r2_score
# # 定义样本和特征数量
# num_sample=1000
# num_feature=1
# # weight=[2,-3.4]
# weight=-3.4
# b_true=4.3
# # 生成曲线
# feature=np.random.normal(size=(num_sample,num_feature))
# # label=weight[0]*feature[:,0]+weight[1]*feature[:,1]+b_true+np.random.normal(size=(num_sample,num_feature))
# label=weight*feature+b_true+np.random.normal(size=(num_sample,num_feature))

# Split the data into training/testing sets
X_train = [
[55.0301],
[56.2702],
[58.1452],
[58.7604],
[59.6120],
[60.1334],
[60.4755],
[61.2974],
[61.9455],
[62.8487],
[63.2784],
[63.9078],
[64.7708],
[66.5933],
[66.9055],
[67.5791],
[68.9374],
[69.4005],
[71.1880],
[71.2677],
[77.0399],
[97.0905],
[100.7431]

]
xs = [
55.0301,
56.2702,
58.1452,
58.7604,
59.6120,
60.1334,
60.4755,
61.2974,
61.9455,
62.8487,
63.2784,
63.9078,
64.7708,
66.5933,
66.9055,
67.5791,
68.9374,
69.4005,
71.1880,
71.2677,
77.0399,
97.0905,
100.7431
]

# X_train = np.transpose(X_train).tolist()    # 矩阵转list
X_test = X_train

# Split the targets into training/testing sets
y_train = [
27.54,
25.45,
24.06,
22.95,
22.11,
21.28,
20.45,
19.19,
18.22,
16.41,
15.86,
13.91,
13.21,
11.68,
10.85,
9.74,
8.76,
7.93,
6.54,
5.42,
3.06,
1.25,
0.00
]
y_test = y_train

yy = []
reg = svm.SVR(kernel ='poly',degree = 2,gamma ='scale')
reg.fit(X_train,y_train)
joblib.dump(reg, 'reg.model')
# reg = joblib.load('my_pwlf.model')
# X_train = np.transpose(X_train).tolist()
xx = np.linspace(0, 150, num=1000, endpoint=True, retstep=False, dtype=None)
for j in range(len(xx)):
    yy.append(reg.predict([[xx[j]]]))
# y_predict=reg.predict()
# print(y_predict)
# print('the score of model : %.2f'
#       % reg.score(X_test,y_test))

# # w=reg.coef_
# # b=reg.intercept_
# # x1=np.linspace(-5,5,1000)
# # # x2=np.linspace(-5,5,1000)
# # y=w[0]*x1+b

ax = plt.subplot(111)
# ax.plot(X_train,y_train,color='g')
ax.plot(xx,yy,color='b')
ax.plot(xs,y_train,color='r')
# ax.set_zlabel('Z')
# 坐标轴
ax.set_ylabel('water content')
ax.set_xlabel('Gray value')

plt.show()
