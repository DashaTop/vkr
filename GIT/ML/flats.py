#!/usr/bin/env python
# coding: utf-8

import statistics
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm

from sklearn.svm import SVR
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import ElasticNetCV, Lasso
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics  import  mean_absolute_error

data = pd.read_csv('./flats.csv', encoding='utf-8')
data.head()


# Замена текстовых параметров на числовые
data['region'].replace('Кировский', 5, inplace = True)
data['region'].replace('Ленинский', 4, inplace = True)
data['region'].replace('Красноперекопский', 3, inplace = True)
data['region'].replace('Фрунзенский', 2, inplace = True)
data['region'].replace('Заволжский', 1, inplace = True)
data['region'].replace('Дзержинский', 0, inplace = True)
data['wall_type'].replace('кирпичный', 5, inplace = True)
data['wall_type'].replace('панельный', 4, inplace = True)
data['wall_type'].replace('блочный', 3, inplace = True)
data['wall_type'].replace('кирпичный', 2, inplace = True)
data['wall_type'].replace('монолитный', 1, inplace = True)
data['wall_type'].replace('деревянный', 0, inplace = True)
data['rooms'].replace('студии', 1, inplace = True)
data['type'].replace('Вторичка', 1, inplace = True)
data['type'].replace('Новостройки', 2, inplace = True)

srarf_area = data['area'].mean()
median_year = data['year'].median()
r = data['region'].median()

data['area'].fillna(srarf_area, inplace = True)
data['year'].fillna(median_year, inplace = True)
data['region'].fillna(r, inplace = True)

data['area'] = data.area.astype('float64')
data['year'] = data.year.astype('int64')
data['rooms'] = data.rooms.astype('int64')
data['region'] = data.region.astype('int64')

#График соотношения жилой площади и стоимости
plt.scatter(data.area, data.price, c='blue', marker= 's')
plt.title('Соотношение жилой площади и стоимости')
plt.xlabel('Площадь')
plt.ylabel('Стоимость')
plt.show()

#График разброса цен
plt.plot(data.price)
plt.show()

#Коэффициент корреляции и график коэффициента
kcorr = data.corr()
sns.heatmap(kcorr)
plt.show()

data = data[data.area < 250]

train, test = train_test_split(data, test_size = 0.20, random_state = 0)

ans = train.price.to_frame()
ans_test = test.price.to_frame()
features = train.drop(['id', 'price'], 1).copy()
features_test = test.drop(['id', 'price'], 1).copy()

scalar = StandardScaler() # Масштабирует выборку из каждого признака вычесть его среднее и поделить на стандартное отклонение, это делает StandardScaler.

features[features.keys()] = scalar.fit_transform(features[features.keys()])
features_test[features_test.keys()] = scalar.fit_transform(features_test[features_test.keys()])

kfold = KFold(n_splits=10, shuffle=True)
random_state = 0

regs = []
regs.append(Lasso())
regs.append(ElasticNetCV(cv=5))
regs.append(SVR(gamma='scale'))
regs.append(KNeighborsRegressor())
regs.append(DecisionTreeRegressor(random_state=random_state))
regs.append(RandomForestRegressor(random_state=random_state, n_estimators=100))
regs.append(GradientBoostingRegressor(max_features='sqrt'))

means = []
errors = []
absolute_errors = []

for reg in tqdm(regs):
    result = np.sqrt(-cross_val_score(
        reg,
        features,
        y=(ans.values.ravel() / np.max(ans.values.ravel())),
        scoring='neg_mean_squared_error',
        cv=kfold,
        error_score='raise'
    ))

    reg.fit(features, ans.values.ravel())

    means.append(result.mean())
    errors.append(result.std())
    absolute_errors.append(int(mean_absolute_error(reg.predict(features_test), ans_test.values.ravel())))

res_frame = pd.DataFrame({
    'CrossValMeans': means,
    'CrossValerrors': errors,
    'AbsoluteErrors': absolute_errors,
    'Algorithm': [
        'LinearRegression',
        'ElasticNetCV',
        'SVR',
        'KNeighborsRegressor',
        'DecisionTreeRegressor',
        'RandomForestRegressor',
        'GradientBoostingRegressor'
    ]
})

print(res_frame)
g = sns.barplot(
    'CrossValMeans',
    'Algorithm',
    data=res_frame,
    palette='Set3',
    orient='h',
    **{'xerr': errors},
    label='medium'
)
g.set_xlabel('Mean Squared Error')
g = g.set_title('Cross validation scores')
plt.show()