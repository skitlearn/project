import numpy as np
import matplotlib.pyplot as plt
import pwlf
# from sklearn.externals import joblib
import joblib
from sklearn import metrics

x = [
38.0635,
38.2695,
38.3604,
38.5450,
38.8392,
39.0127,
39.1772,
39.1301,
39.2263,
39.3237,
39.4473,
39.4922,
39.5358,
39.5907,
39.6177,
39.7239,
39.8075,
39.9054,
40.1511,
40.4338,
40.9849,
41.2958,
41.3157,
41.4457,
41.7733,
42.5199,
42.7911,
43.9804,
44.8467,
45.6544,
47.7556,
48.0678,
50.0727,
52.7975,
58.2652,
64.7545,
71.1947,
74.3051,
78.5003,
80.4516

]
y = [
28.12,
27.48,
26.79,
26.17,
25.45,
24.72,
24.01,
23.48,
22.83,
21.96,
21.02,
20.62,
20.01,
19.14,
18.50,
17.91,
17.17,
16.62,
15.71,
14.83,
14.15,
13.45,
12.68,
12.01,
11.21,
10.34,
9.86,
8.72,
8.12,
7.57,
6.73,
6.06,
5.46,
4.79,
3.93,
3.24,
2.42,
1.72,
0.96,
0.11

]
x = np.array(x)
y = np.array(y)

# initialize piecewise linear fit with your x and y data
my_pwlf = pwlf.PiecewiseLinFit(x, y)
# fit the data for four line segments
res = my_pwlf.fit(6)
joblib.dump(my_pwlf, 'x82_final.model') # 生成模型
# my_pwlf = joblib.load('xs101_final.model') #加载模型
# predict for the determined points
xHat = np.linspace(37, max(x), num=1000)
# xHat = x
yHat = my_pwlf.predict(xHat)
# yHat = []
# xHat = x
# for i in range(len(x)):
#     temp = my_pwlf.predict(x[i])
#     yHat.append(temp)
# print(metrics.mean_absolute_error(y, yHat))
# plot the results
plt.figure()
plt.plot(x, y, 'p','b')
plt.plot(xHat, yHat,'r')
plt.show()