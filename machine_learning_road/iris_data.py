import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets



# 数据集 0-setosa、1-versicolor、2-virginica
scikit_iris = datasets.load_iris()
# 转换成pandas的DataFrame数据格式，方便观察数据
iris = pd.DataFrame(data=np.c_[scikit_iris['data'], scikit_iris['target']], columns=np.append(scikit_iris.feature_names, ['y']))

# print(iris.head(2))
# print(iris.isnull().sum())
# print(scikit_iris.feature_names)


# 训练
from sklearn.neighbors import KNeighborsClassifier
# 选择全部特征训练模型
X = iris[scikit_iris.feature_names]
# label
y = iris['y']

# 选择全部特征训练模型
knn = KNeighborsClassifier(n_neighbors=1)
# label
knn.fit(X, y)

# 测试一个新的数据
value = knn.predict([[3, 2, 2, 5]])
# print(value)


# 评估模型
from sklearn.model_selection import train_test_split
from sklearn import metrics

# 分割训练-测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=4)

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X_train, y_train)

y_pred_on_train = knn.predict(X_train)
y_pred_on_test = knn.predict(X_test)

print(metrics.accuracy_score(y_train, y_pred_on_train))
print('accuracy: ：{}'.format(metrics.accuracy_score(y_test, y_pred_on_test)))
