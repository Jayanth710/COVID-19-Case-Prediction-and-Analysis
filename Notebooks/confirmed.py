# -*- coding: utf-8 -*-
"""Confirmed.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dhgOKatzTa-TlD9i4itw3xruk-Un1OYO

**Importing** **Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import BayesianRidge
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.model_selection import train_test_split

"""**Datasets and Preprocessing**

#### Analysis of confirmed cases in World and India
"""

#Confirmed Cases in World and India

world_covid_confirmed=pd.read_csv('/content/time_series_covid19_confirmed_global1.csv')
world_covid_confirmed.drop(columns=['Province/State','Lat','Long'],inplace=True)
India_covid_confirmed=world_covid_confirmed[world_covid_confirmed['Country/Region']=='India']
print(India_covid_confirmed)
world_covid_confirmed

#columns

cols=world_covid_confirmed.keys()
cols=cols[1:]
cols

#Access all No.of Confirmed Cases daily in World

world_confirmed=[]
cov_confirmed=world_covid_confirmed.values
for i in range(1,len(cols)+1):
  world_confirmed.append(cov_confirmed[:,i].sum())
world_confirmed=np.array(world_confirmed).reshape(-1,1)
world_confirmed

#Access all Confirmed Cases Daily in India

India_confirmed=[]
ind_confirmed=world_covid_confirmed[world_covid_confirmed['Country/Region']=='India'].values
for i in range(1,len(cols)+1):
  India_confirmed.append(ind_confirmed[:,i].sum())
India_confirmed=np.array(India_confirmed).reshape(-1,1)
India_confirmed

#Days

days = np.array([i for i in range(len(world_confirmed))]).reshape(-1, 1)
days

#Converting Dates

dates=pd.to_datetime(cols)
dates

"""**Graphs**"""

#Graph for Confirmed Cases in World

plt.figure(figsize=(12, 8))
plt.plot(dates,world_confirmed)
plt.title('Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.xticks(size=15)
plt.show()

#Graph for Confirmed Cases in India

plt.figure(figsize=(12, 8))
plt.plot(dates,India_confirmed)
plt.title('Coronavirus Confirmed Cases Over Time in India', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in million)', size=20)
plt.xticks(size=15)
plt.show()

"""#Prediction"""

days_in_future = 15
prediction_days = np.array([i for i in range(len(days)+days_in_future)]).reshape(-1, 1)
start = '1/22/2020'
start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
prediction_dates = []
for i in range(len(prediction_days)):
    prediction_dates.append((start_date + datetime.timedelta(days=i)).strftime('%m/%d/%Y'))
prediction_dates

"""**Confirmed  Cases**"""

xtrain_world_confirmed,xtest_world_confirmed,ytrain_world_confirmed,ytest_world_confirmed = train_test_split(days,world_confirmed,test_size=0.35)
xtrain_ind_confirmed,xtest_ind_confirmed,ytrain_ind_confirmed,ytest_ind_confirmed = train_test_split(days,India_confirmed,test_size=0.35)

"""**Linear Regression**"""

accuracy_world=[]
accuracy_india=[]
model=['Linear Regression','Polynomial Regression','Bayesian Ridge','SVR']

train_world=[]
train_india=[]
test_world=[]
test_india=[]

# World

lmodel_world_confirmed=LinearRegression()
lmodel_world_confirmed.fit(xtrain_world_confirmed,ytrain_world_confirmed)
lmodel_world_confirmed_test = lmodel_world_confirmed.predict(xtest_world_confirmed)
lmodel_world_confirmed_predict = lmodel_world_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(lmodel_world_confirmed_test, ytest_world_confirmed))
print('MSE:',metrics.mean_squared_error(lmodel_world_confirmed_test,ytest_world_confirmed))
print('Training score:',lmodel_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed))
print('Testing score:',lmodel_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed))
print('R2 :',metrics.r2_score(lmodel_world_confirmed_test,ytest_world_confirmed))
print('Co-efficient:',lmodel_world_confirmed.coef_)
print('Intercept:',lmodel_world_confirmed.intercept_)
accuracy_world.append((metrics.r2_score(lmodel_world_confirmed_test,ytest_world_confirmed))*100)
train_world.append(lmodel_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed)*100)
test_world.append(lmodel_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed)*100)

# India
lmodel_ind_confirmed=LinearRegression()
lmodel_ind_confirmed.fit(xtrain_ind_confirmed,ytrain_ind_confirmed)
lmodel_ind_confirmed_test=lmodel_ind_confirmed.predict(xtest_ind_confirmed)
lmodel_ind_confirmed_predict=lmodel_ind_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(lmodel_ind_confirmed_test, ytest_ind_confirmed))
print('MSE:',metrics.mean_squared_error(lmodel_ind_confirmed_test,ytest_ind_confirmed))
print('R2 :',metrics.r2_score(lmodel_ind_confirmed_test,ytest_ind_confirmed))
print('Training score:',lmodel_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed))
print('Testing score:',lmodel_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed))
print('Co-efficient:',lmodel_ind_confirmed.coef_)
print('Intercept:',lmodel_ind_confirmed.intercept_)
accuracy_india.append((metrics.r2_score(lmodel_ind_confirmed_test,ytest_ind_confirmed))*100)
train_india.append(lmodel_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed)*100)
test_india.append(lmodel_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed)*100)

#Graph for Linear Predicted Confirmed Cases in World

plt.figure(figsize=(12, 8))
plt.plot(days,world_confirmed)
plt.plot(prediction_days,lmodel_world_confirmed_predict,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Linear Regression Predictions'])
plt.xticks(size=15)
plt.show()

#Graph for Linear Predicted Confirmed Cases in India

plt.figure(figsize=(12, 8))
plt.plot(days,India_confirmed)
plt.plot(prediction_days,lmodel_ind_confirmed_predict,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in India', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Linear Regression Predictions'])
plt.xticks(size=15)
plt.show()

#Prediction Cases in World

lmodel_world_confirmed_predict = lmodel_world_confirmed_predict.reshape(1,-1)[0]
df_world_confirmed_linear_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Linear Regression Predicted # of Confirmed Cases Worldwide': np.round(lmodel_world_confirmed_predict[-(days_in_future):])})
df_world_confirmed_linear_predict

#Prediction in India

lmodel_ind_confirmed_predict = lmodel_ind_confirmed_predict.reshape(1,-1)[0]
df_ind_confirmed_linear_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Linear Regression Predicted # of Confirmed Cases in India': np.round(lmodel_ind_confirmed_predict[-(days_in_future):])})
df_ind_confirmed_linear_predict

"""**Polynomial Regression**"""

# To find Best Degree

#World

error_confirmed=[]
for i in range(0,20):
  pol=PolynomialFeatures(degree=i)
  pol_world_confirmed=pol.fit_transform(xtrain_world_confirmed)
  pol_world_confirmed_test=pol.fit_transform(xtest_world_confirmed)
  lmodel=LinearRegression()
  lmodel.fit(pol_world_confirmed,ytrain_world_confirmed)
  pol_world_confirmed_predict=lmodel.predict(pol_world_confirmed_test)
  e=metrics.mean_absolute_error(pol_world_confirmed_predict,ytest_world_confirmed)
  error_confirmed.append(e)
plt.plot(range(0,20),error_confirmed)
plt.show()

#best degree=2

pol=PolynomialFeatures(degree=2)
pol_world_confirmed=pol.fit_transform(xtrain_world_confirmed)
pol_world_confirmed_test=pol.fit_transform(xtest_world_confirmed)
pol_world_confirmed_predict_days=pol.fit_transform(prediction_days)
pmodel=LinearRegression()
pmodel.fit(pol_world_confirmed,ytrain_world_confirmed)
pol_world_confirmed_predict=pmodel.predict(pol_world_confirmed_test)
pol_world_confirmed_days=pmodel.predict(pol_world_confirmed_predict_days)
print('MAE:', metrics.mean_absolute_error(pol_world_confirmed_predict, ytest_world_confirmed))
print('MSE:',metrics.mean_squared_error(pol_world_confirmed_predict,ytest_world_confirmed))
print('R2 :',metrics.r2_score(pol_world_confirmed_predict,ytest_world_confirmed))
print('Training score:',pmodel.score(pol_world_confirmed,ytrain_world_confirmed))
print('Testing score:',pmodel.score(pol_world_confirmed_test,ytest_world_confirmed))
print('Co-efficient:',pmodel.coef_)
print('Intercept:',pmodel.intercept_)
accuracy_world.append((metrics.r2_score(pol_world_confirmed_predict,ytest_world_confirmed))*100)
train_world.append(pmodel.score(pol_world_confirmed,ytrain_world_confirmed)*100)
test_world.append(pmodel.score(pol_world_confirmed_test,ytest_world_confirmed)*100)

#Graph for Polynomial Predicted Confirmed Cases in World

plt.figure(figsize=(12, 8))
plt.plot(days,world_confirmed)
plt.plot(prediction_days,pol_world_confirmed_days,linestyle='dashed')
plt.title('Polynomial Predicted Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Polynomial Regression Predictions'])
plt.xticks(size=15)
plt.show()

#predicted Cases

pol_world_confirmed_days = pol_world_confirmed_days.reshape(1,-1)[0]
df_world_confirmed_poly_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Polynomial Regression Predicted # of Confirmed Cases Worldwide': np.round(pol_world_confirmed_days[-(days_in_future):])})
df_world_confirmed_poly_predict

#India

error_confirmed=[]
for i in range(0,20):
  pol=PolynomialFeatures(degree=i)
  pol_ind_confirmed=pol.fit_transform(xtrain_ind_confirmed)
  pol_ind_confirmed_test=pol.fit_transform(xtest_ind_confirmed)
  lmodel=LinearRegression()
  lmodel.fit(pol_ind_confirmed,ytrain_ind_confirmed)
  pol_ind_confirmed_predict=lmodel.predict(pol_ind_confirmed_test)
  e=metrics.mean_absolute_error(pol_ind_confirmed_predict,ytest_ind_confirmed)
  error_confirmed.append(e)
plt.plot(range(0,20),error_confirmed)
plt.show()

#best Degree=4

pol=PolynomialFeatures(degree=4)
pol_ind_confirmed=pol.fit_transform(xtrain_ind_confirmed)
pol_ind_confirmed_test=pol.fit_transform(xtest_ind_confirmed)
pol_ind_confirmed_predict_days=pol.fit_transform(prediction_days)
pmodel=LinearRegression()
pmodel.fit(pol_ind_confirmed,ytrain_ind_confirmed)
pol_ind_confirmed_predict=pmodel.predict(pol_ind_confirmed_test)
pol_ind_confirmed_days=pmodel.predict(pol_ind_confirmed_predict_days)
print('MAE:', metrics.mean_absolute_error(pol_ind_confirmed_predict, ytest_ind_confirmed))
print('MSE:',metrics.mean_squared_error(pol_ind_confirmed_predict,ytest_ind_confirmed))
print('R2 :',metrics.r2_score(pol_ind_confirmed_predict,ytest_ind_confirmed))
print('Training score:',pmodel.score(pol_ind_confirmed,ytrain_ind_confirmed))
print('Testing score:',pmodel.score(pol_ind_confirmed_test,ytest_ind_confirmed))
print('Co-efficient:',pmodel.coef_)
print('Intercept:',pmodel.intercept_)
accuracy_india.append((metrics.r2_score(pol_ind_confirmed_predict,ytest_ind_confirmed))*100)
train_india.append(pmodel.score(pol_ind_confirmed,ytrain_ind_confirmed)*100)
test_india.append(pmodel.score(pol_ind_confirmed_test,ytest_ind_confirmed)*100)

#Graph for Polynomial Predicted Confirmed Cases in India

plt.figure(figsize=(12, 8))
plt.plot(days,India_confirmed)
plt.plot(prediction_days,pol_ind_confirmed_days,linestyle='dashed')
plt.title('Polynomial Predicted Coronavirus Confirmed Cases Over Time in India', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Polynomial Regression Predictions'])
plt.xticks(size=15)
plt.show()

#predicted Cases in India

pol_ind_confirmed_days = pol_ind_confirmed_days.reshape(1,-1)[0]
df_ind_confirmed_poly_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Polynomial Regression Predicted # of Confirmed Cases India': np.round(pol_ind_confirmed_days[-(days_in_future):])})
df_ind_confirmed_poly_predict

#Bayesian Ridge

#To get Best Parameters

reg_world_confirm=BayesianRidge()
reg_world_confirm.fit(xtrain_world_confirmed,ytrain_world_confirmed)
print(reg_world_confirm.get_params)

#World

reg_world_confirmed=BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, alpha_init=None,
              compute_score=False, copy_X=True, fit_intercept=True,
              lambda_1=1e-06, lambda_2=1e-06, lambda_init=None, n_iter=300,
              normalize=False, tol=0.001, verbose=False)
reg_world_confirmed.fit(xtrain_world_confirmed,ytrain_world_confirmed)
reg_world_confirmed_test = reg_world_confirmed.predict(xtest_world_confirmed)
reg_world_confirmed_predict_days = reg_world_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(reg_world_confirmed_test, ytest_world_confirmed))
print('MSE:',metrics.mean_squared_error(reg_world_confirmed_test, ytest_world_confirmed))
print('R2 :',metrics.r2_score(reg_world_confirmed_test, ytest_world_confirmed))
print('Training score:',reg_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed))
print('Testing score:',reg_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed))
accuracy_world.append((metrics.r2_score(reg_world_confirmed_test, ytest_world_confirmed))*100)
train_world.append(reg_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed)*100)
test_world.append(reg_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed)*100)

#Graph for Bayesian Predicted Confirmed Cases in World

plt.figure(figsize=(12, 8))
plt.plot(days,world_confirmed)
plt.plot(prediction_days,reg_world_confirmed_predict_days,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Bayesian Ridge Predictions'])
plt.xticks(size=15)
plt.show()

reg_world_confirmed_predict_days = reg_world_confirmed_predict_days.reshape(1,-1)[0]
df_world_confirmed_reg_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Bayesian Ridge Predicted # of Confirmed Cases Worldwide': np.round(reg_world_confirmed_predict_days[-(days_in_future):])})
df_world_confirmed_reg_predict

#To get Parameters

reg_ind_confirm=BayesianRidge()
reg_ind_confirm.fit(xtrain_ind_confirmed,ytrain_ind_confirmed)
print(reg_ind_confirm.get_params)

#India

reg_ind_confirmed=BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, alpha_init=None,
              compute_score=False, copy_X=True, fit_intercept=True,
              lambda_1=1e-06, lambda_2=1e-06, lambda_init=None, n_iter=300,
              normalize=False, tol=0.001, verbose=False)
reg_ind_confirmed.fit(xtrain_ind_confirmed,ytrain_ind_confirmed)
reg_ind_confirmed_test = reg_ind_confirmed.predict(xtest_ind_confirmed)
reg_ind_confirmed_predict_days = reg_ind_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(reg_ind_confirmed_test, ytest_ind_confirmed))
print('MSE:',metrics.mean_squared_error(reg_ind_confirmed_test, ytest_ind_confirmed))
print('R2 :',metrics.r2_score(reg_ind_confirmed_test, ytest_ind_confirmed))
print('Training score:',reg_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed))
print('Testing score:',reg_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed))
accuracy_india.append((metrics.r2_score(reg_ind_confirmed_test, ytest_ind_confirmed))*100)
train_india.append(reg_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed)*100)
test_india.append(reg_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed)*100)

#Graph for Bayesian Predicted Confirmed Cases in India

plt.figure(figsize=(12, 8))
plt.plot(days,India_confirmed)
plt.plot(prediction_days,reg_ind_confirmed_predict_days,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'Bayesian Ridge Predictions'])
plt.xticks(size=15)
plt.show()

reg_ind_confirmed_predict_days = reg_ind_confirmed_predict_days.reshape(1,-1)[0]
df_ind_confirmed_reg_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'Bayesian Ridge Predicted # of Confirmed Cases India': np.round(reg_ind_confirmed_predict_days[-(days_in_future):])})
df_ind_confirmed_reg_predict

#SVM

#World

svm_world_confirmed = SVR(shrinking=True, kernel='poly',gamma=0.01, epsilon=1,degree=3, C=0.1)
svm_world_confirmed.fit(xtrain_world_confirmed, ytrain_world_confirmed)
svm_world_confirmed_predict = svm_world_confirmed.predict(xtest_world_confirmed)
svm_world_confirmed_predict_days=svm_world_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(svm_world_confirmed_predict, ytest_world_confirmed))
print('MSE:',metrics.mean_squared_error(svm_world_confirmed_predict, ytest_world_confirmed))
print('R2 :',metrics.r2_score(svm_world_confirmed_predict, ytest_world_confirmed))
print('Training score:',svm_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed))
print('Testing score:',svm_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed))
accuracy_world.append((metrics.r2_score(svm_world_confirmed_predict, ytest_world_confirmed))*100)
train_world.append(svm_world_confirmed.score(xtrain_world_confirmed,ytrain_world_confirmed)*100)
test_world.append(svm_world_confirmed.score(xtest_world_confirmed,ytest_world_confirmed)*100)

#Graph for SVM Predicted Confirmed Cases in World

plt.figure(figsize=(12, 8))
plt.plot(days,world_confirmed)
plt.plot(prediction_days,svm_world_confirmed_predict_days,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in World', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'SVM Predictions'])
plt.xticks(size=15)
plt.show()

svm_world_confirmed_predict_days = svm_world_confirmed_predict_days.reshape(1,-1)[0]
df_world_confirmed_svm_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'SVM Predicted # of Confirmed Cases Worldwide': np.round(svm_world_confirmed_predict_days[-(days_in_future):])})
df_world_confirmed_svm_predict

#India

svm_ind_confirmed = SVR(shrinking=True, kernel='poly',gamma=0.01, epsilon=1,degree=3, C=0.1)
svm_ind_confirmed.fit(xtrain_ind_confirmed, ytrain_ind_confirmed)
svm_ind_confirmed_predict = svm_ind_confirmed.predict(xtest_ind_confirmed)
svm_ind_confirmed_predict_days=svm_ind_confirmed.predict(prediction_days)
print('MAE:', metrics.mean_absolute_error(svm_ind_confirmed_predict, ytest_ind_confirmed))
print('MSE:',metrics.mean_squared_error(svm_ind_confirmed_predict, ytest_ind_confirmed))
print('R2 :',metrics.r2_score(svm_ind_confirmed_predict, ytest_ind_confirmed))
print('Training score:',svm_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed))
print('Testing score:',svm_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed))
accuracy_india.append((metrics.r2_score(svm_ind_confirmed_predict, ytest_ind_confirmed))*100)
train_india.append(svm_ind_confirmed.score(xtrain_ind_confirmed,ytrain_ind_confirmed)*100)
test_india.append(svm_ind_confirmed.score(xtest_ind_confirmed,ytest_ind_confirmed)*100)

#Graph for SVM Predicted Confirmed Cases in India

plt.figure(figsize=(12, 8))
plt.plot(days,India_confirmed)
plt.plot(prediction_days,svm_ind_confirmed_predict_days,linestyle='dashed')
plt.title('Predicted Coronavirus Confirmed Cases Over Time in India', size=30)
plt.xlabel('Days Since 1/22/2020', size=20)
plt.ylabel('No.of Cases(in Croces)', size=20)
plt.legend(['Confirmed Cases', 'SVM Predictions'])
plt.xticks(size=15)
plt.show()

svm_ind_confirmed_predict_days = svm_ind_confirmed_predict_days.reshape(1,-1)[0]
df_ind_confirmed_svm1_predict = pd.DataFrame({'Date': prediction_dates[-(days_in_future):], 'SVM Predicted # of Confirmed Cases India': np.round(svm_ind_confirmed_predict_days[-(days_in_future):])})
df_ind_confirmed_svm1_predict

#Bar Graph
wid=0.25

#Accuracy of World

plt.figure(figsize=(8,6))
plt.bar(model,accuracy_world,width=wid)
plt.title('Accuracy of Confirmed Cases in World of Different Models',size=20)
plt.xlabel('Model',size=15)
plt.ylabel('Accuracy( % )',size=15)
plt.show()

#Accuracy of India

plt.figure(figsize=(8,6))
plt.bar(model,accuracy_india,width=wid)
plt.title('Accuracy of Confirmed Cases in India of Different Models',size=20)
plt.xlabel('Model',size=15)
plt.ylabel('Accuracy( % )',size=15)
plt.show()

plt.figure(figsize=(10,6))
plt.plot(model,accuracy_world)
plt.plot(model,accuracy_india)
plt.title('Accuracy of Confirmed Cases in World and India of Different Models', size=30)
plt.xlabel('Model', size=20)
plt.ylabel('Accuracy( % )', size=20)
plt.legend(['World', 'India'])
plt.yticks(size=20)
plt.show()

#Group plots for Train,Test Of World

wid=0.25
world1=np.arange(len(train_world))
plt.figure(figsize=(10,6))
plt.bar(world1, train_world, width=wid)
plt.bar(world1+wid,test_world, width=wid)
plt.title('Train and Test Accuracy of Confirmed Cases in World',size=20)
plt.xlabel('Model',size=15)
plt.ylabel('Accuracy( % )',size=15)
plt.xticks((world1+wid/2),model)
plt.legend(['Train','Test'])
plt.show()

#Group Bar plots for India

ind1=np.arange(len(train_india))
plt.figure(figsize=(10,6))
plt.bar(model, train_india, width=wid)
plt.bar(ind1+wid,test_india, width=wid)
plt.title('Train and Test Accuracy Confirmed Cases in India',size=20)
plt.xlabel('Model',size=15)
plt.ylabel('Accuracy( % )',size=15)
plt.xticks(ind1+wid/2,model)
plt.legend(['Train','Test'])
plt.show()