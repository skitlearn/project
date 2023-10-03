#学习课程
#python
#学习时间: 2022-12-02  13:56
#学习课程
#python
#学习时间: 2022-09-23  15:48


import numpy as np
import matplotlib.pyplot as plt
import pwlf
# from sklearn.externals import joblib
import joblib
from sklearn import metrics

x = np.array([
104.8370,
105.0710,
108.4533,
109.5396,
110.1186,
110.3607,
111.5656,
112.7491,
113.4425,
115.4256,
115.6881,
116.8840,
117.7755,
119.1085,
120.8885,
121.9553,
123.2052,
124.3391,
125.4094,
126.4758,
128.8058,
130.4550,
131.6785,
133.0876,
134.4194,
135.7453,
137.0364,
141.3198,
141.3208,
143.1065,
145.5100,
148.4771,
153.1514,
157.8699,
167.3988,
172.0701,
177.5608,
182.4206,
184.1138,
187.7943,
199.9256,
])

y = np.array([
23.24,
22.38,
21.74,
21.08,
20.58,
20.07,
19.58,
18.99,
18.56,
17.81,
17.74,
17.45,
17.11,
16.57,
16.03,
15.56,
15.05,
14.69,
13.96,
13.73,
13.31,
12.77,
12.26,
11.69,
11.29,
10.87,
10.41,
9.87,
9.44,
8.90,
7.77,
7.19,
6.34,
5.64,
4.83,
4.06,
3.20,
2.43,
1.67,
1.22,
0.82,
])

x = np.array(x)
y = np.array(y)

# initialize piecewise linear fit with your x and y data
my_pwlf = pwlf.PiecewiseLinFit(x, y)
# fit the data for four line segments
res = my_pwlf.fit(6)
joblib.dump(my_pwlf, '../xs82_ceshi.model') # 生成模型
# predict for the determined points
xHat = np.linspace(40, max(x), num=1000)
# xHat = x
yHat = my_pwlf.predict(xHat)


plt.figure()
plt.plot(x,  y, 'o', color='blue', markersize=3)
plt.plot(xHat, yHat, 'r')
plt.xlabel("Gray value", fontsize=13, fontweight='bold')
plt.ylabel("Water content(,)", fontsize=13, fontweight='bold')
plt.show()