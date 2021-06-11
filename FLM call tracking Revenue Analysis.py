#!/usr/bin/env python
# coding: utf-8

# #                     FLM call tracking revenue analysis for 1st quarter 2021
#  

# ##  Business Problem  

# Sales department needs to measure the efficiency of sales calls made by their team  and wanted  to find out the relationships with sales revenues
# The challenge here everyday number of calls are made and tracking the outcome may not be feasible always whether it is turned into business incident or not .
# Call durations are segregated for 1st quarter of 2021 , to be analyzed how effectively the call data is incorporated as significance of sales win or lost . 
# 

# ## Project Objective and Scope

# All call data to be downloaded from ESA server, sales revenue data will be given by the stake holder.
# We will have to find out the trends observed in terms of sellers calls made and acquired revenues 
# Identify the most popular group ,max and minimum seller variables 
# 

# ## Project Approach 

# A typical Lifecycle can be adopted for this assignment, as follows: 
# 1. Data Preparation 
# 2. Exploratory Analysis
# 4. Communicating Results

# ##  Data Preparation  

# 1. All call data to extracted month wise for Jan to Mar 2021 from ESA server
# 
# 2. Monthly collected data will be joined  with unique key of  Jan to Mar 2021  output to be saved  in single file 
# 
# 3. FMS data  to be collected from ESA team since we do not have direct access 
# 
# 4. FMS table data has  all employee details and this has to be merged with call data which has collected  earlier.
# 
# 5. Further  sale revenue data needs to be merged correctly because this has employee wise unique records 
# 
# 6. Call data is bifurcated with start and end data of each call so one employee may have often records 
# 
# 7. Duplicate records will be removed while merging with sales revenue data because adding duplicate records can lead to have more sale revenue over sightly
# 

# In[1]:


import pyodbc 
import jaydebeapi 


# In[2]:


# from jupyterthemes import get_themes
# import jupyterthemes as jt
# from jupyterthemes.stylefx import set_nb_theme
# set_nb_theme('chesterish')


# In[3]:


import jpype
import ibm_db
import ibm_db_dbi
from pandas.io import sql
import pandas.io.sql as psql


# In[4]:


import pandas as pd
from pandas.plotting import scatter_matrix
from pandas import ExcelWriter
from pandas import ExcelFile
from openpyxl import load_workbook
import numpy as np
from scipy.stats import norm, skew
from scipy import stats
import statsmodels.api as sm
import warnings
import datetime
from datetime import datetime as dt
warnings.filterwarnings('ignore')
import seaborn as sns
import scipy.stats as stats
from statsmodels.formula.api import ols
from statsmodels.stats.anova import _get_covariance,anova_lm
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import matplotlib
# %matplotlib inline
# sns.set()


# In[5]:


import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
import numpy as np


# ## ESA server connection 

# In[6]:


# # #To connect to ESA Database which is NetezzaSQL, install odbc driver.
# print (pyodbc.dataSources()) 
# conn = pyodbc.connect('DRIVER={NetezzaSQL};'\
# 'SERVER=;'\
# 'PORT=;'\
# 'DATABASE=;'\
# 'UID=;PWD=;')


# ## Importing data from 1st January 2021 to 31st May  2021

# In[7]:


# # # query1 = 'select * from EDGEDM.CRM_SELLER_CALL_FACT WHERE DATE_ENTERED BETWEEN 2020-01-01 AND 2020-12-01'
# sql = """ SELECT EDGEDM.CRM_SELLER_CALL_FACT.SNAPSHOT_CURR_WEEK_INDC,
# EDGEDM.CRM_SELLER_CALL_FACT.SNAPSHOT_WK_QTRYR_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.CRM_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.CRM_SOURCE,
# EDGEDM.CRM_SELLER_CALL_FACT.ACTIVE_INDC,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_ENTERED,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_MODIFIED,
# EDGEDM.CRM_SELLER_CALL_FACT.CNUM,
# EDGEDM.CRM_SELLER_CALL_FACT.INTERACTION_TYPE,
# EDGEDM.CRM_SELLER_CALL_FACT.DIRECTION,
# EDGEDM.CRM_SELLER_CALL_FACT.STATUS,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_START,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_END,
# EDGEDM.CRM_SELLER_CALL_FACT.START_DAY_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.END_DAY_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.CALL_WEEK_MNEMONIC_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.PARENT_TYPE,
# EDGEDM.CRM_SELLER_CALL_FACT.PARENT_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.TAGS,
# EDGEDM.CRM_SELLER_CALL_FACT.DURATION,
# EDGEDM.CRM_SELLER_CALL_FACT.IW_ROW_UPDT_TS

# FROM EDGEDM.CRM_SELLER_CALL_FACT
# WHERE EDGEDM.CRM_SELLER_CALL_FACT.DATE_START BETWEEN ? AND ? ;"""

# df1 = pd.read_sql_query(sql, conn, params=['2021-01-01','2021-01-01'])


# ## Importing data from 1st January 2021 to 31st March 2021
# 
# Since the data rannge is requed huge momery , we have to extract it month wise 

# In[8]:


# sql = """ SELECT EDGEDM.CRM_SELLER_CALL_FACT.SNAPSHOT_CURR_WEEK_INDC,
# EDGEDM.CRM_SELLER_CALL_FACT.SNAPSHOT_WK_QTRYR_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.CRM_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.CRM_SOURCE,
# EDGEDM.CRM_SELLER_CALL_FACT.ACTIVE_INDC,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_ENTERED,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_MODIFIED,
# EDGEDM.CRM_SELLER_CALL_FACT.CNUM,
# EDGEDM.CRM_SELLER_CALL_FACT.INTERACTION_TYPE,
# EDGEDM.CRM_SELLER_CALL_FACT.DIRECTION,
# EDGEDM.CRM_SELLER_CALL_FACT.STATUS,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_START,
# EDGEDM.CRM_SELLER_CALL_FACT.DATE_END,
# EDGEDM.CRM_SELLER_CALL_FACT.START_DAY_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.END_DAY_KEY,
# EDGEDM.CRM_SELLER_CALL_FACT.CALL_WEEK_MNEMONIC_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.PARENT_TYPE,
# EDGEDM.CRM_SELLER_CALL_FACT.PARENT_ID,
# EDGEDM.CRM_SELLER_CALL_FACT.TAGS,
# EDGEDM.CRM_SELLER_CALL_FACT.DURATION,
# EDGEDM.CRM_SELLER_CALL_FACT.IW_ROW_UPDT_TS

# FROM EDGEDM.CRM_SELLER_CALL_FACT
# WHERE YEAR(EDGEDM.CRM_SELLER_CALL_FACT.DATE_START) = ? AND MONTH(EDGEDM.CRM_SELLER_CALL_FACT.DATE_START) = ?; """


# #### Import data from sql serve for May 2021

# In[9]:


# df_may = pd.read_sql_query(sql, conn, params=[2021,5])
# # df_may.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/df_may.csv', index = False, header=True


# #### Import data from sql serve for APR 2021

# In[10]:


# df_apr = pd.read_sql_query(sql, conn, params=[2021,4])
# # df_apr.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/df_apr.csv', index = False, header=True)


# #### Import data from sql serve for MAR 2021

# In[11]:


# df_mar = pd.read_sql_query(sql, conn, params=[2021,3])
# # df_mar.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/df_mar.csv', index = False, header=True)


# #### Import data from sql serve for FEB 2021

# In[12]:


# df_feb = pd.read_sql_query(sql, conn, params=[2021,2])
# # df_feb.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/df_feb.csv', index = False, header=True)


# #### Import data from sql serve for JAN 2021

# In[13]:


# df_jan = pd.read_sql_query(sql, conn, params=[2021,1])
# df_jan.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/df_jan.csv', index = False, header=True)               


# #### Import to one file all JAN to MAR 2021

# In[14]:


# df1qtr = df_mar.append([df_feb,df_jan],ignore_index = True)
# df2021 = df_may.append([df_apr,df_mar,df_feb,df_jan],ignore_index = True)


# In[15]:


## Store in local drive 
# df1qtr = pd.read_csv ('C:/Users/SuprasannaPradhan/Documents/DIA/df1qtr.csv')
# # # df_jan = pd.read_csv('C:/Users/SuprasannaPradhan/Documents/DIA/df_jan.csv')


# #### Removeing leading zeros from the data key 

# In[16]:


# df1qtr['CNUM'] = df1qtr['CNUM'].apply(lambda x:x.lstrip('0') if type(x) == str else x)


# In[17]:


# df1qtr.count()


# In[18]:


# df_jan['Numeric_CNUM'] = pd.to_numeric(df_jan['CNUM'], errors='coerce')
# mask = df_jan['Numeric_CNUM'].isna()
# df_jan.loc[mask, 'Text_CNUM'] = df_jan.loc[mask, 'CNUM']
# # df_jan.drop(columns=['CNUM'])


# In[19]:


# df_jan['row3'] = df_jan.Numeric_CNUM
# df_jan.loc[df_jan.row3 > 0 , 'row3'] = df_jan.CNUM


# In[20]:


# df_jan['row4'] = df_jan['row3'] * 1  


# In[21]:


# df_jan['Text_CNUM'].fillna('', inplace=True)
# df_jan['Numeric_CNUM'] = df_jan['Numeric_CNUM'].astype(object).fillna('')


# ## Importing FMS data 

# In[22]:


# fms_data = pd.read_csv ('C:/Users/SuprasannaPradhan/Documents/DIA/EDGEDM_DIM_FMS_HIERS.csv')


# ## Merging data set and saved local drive 

# In[23]:


# qtr1_call = pd.merge(left = df1qtr, right=fms_data,how='left', left_on='CNUM', right_on='CNUM',indicator=True)
# qtr1_call.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/qtr1_call.csv', index = False, header=True)


# In[24]:


chunksize = 10000
qtr= pd.read_csv ('C:/Users/SuprasannaPradhan/Documents/DIA/qtr1_call.csv',chunksize=chunksize, iterator=True)
qtr1_call = pd.concat(qtr, ignore_index=True)


# In[25]:


qtr1_call["EMP_FULL_NAME"] = qtr1_call["EMP_FULL_NAME"].str.upper()


# ## Overview of data 

# In[26]:


qtr1_call.columns


# It is very huge data we have been having 5.1 + MB

# In[27]:


# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# qtr1_call


# 
# ## Adding Month and Week variable in the data set 

# In[28]:


q1_date = qtr1_call.groupby(['CNUM'])['DATE_START'].agg(['first','last']).reset_index()
q1_date.head(10)


# In[29]:


#Adding month and weeks in the data set 
q1_date_update = q1_date .iloc[ : , [0,1,2]] 
q1_date_update.columns = ['CNUM','DATE_START_f','DATE_START_e',] 
q1_date_update = q1_date_update.drop(columns=['DATE_START_e'])
q1_date_update["DATE_START_f"] = pd.to_datetime(q1_date_update.DATE_START_f, format='%Y-%m-%d %H:%M:%S')
q1_date_update['DATE_START_f'] = pd.to_datetime(q1_date_update.DATE_START_f, format='%Y-%m-%d')
q1_date_update['DATE_START_f'] = q1_date_update['DATE_START_f'].dt.strftime('%Y-%m-%d')
q1_date_update['MONTH'] = pd.PeriodIndex(q1_date_update['DATE_START_f'], freq='M')
q1_date_update['WEEK'] = pd.PeriodIndex(q1_date_update['DATE_START_f'], freq='W')


# In[30]:


q1_date_update.head(10)


# ## Prepared subset of data set 

# In[31]:


# Subset of data whihc  variables are need for our analysis 
q1_prune = qtr1_call .iloc[ : , [7,8,9,10,11,12,16,18,19,23,24,25,32,36,38,56,72,82]] 
q1_prune.head()


# In[467]:


q1_prune.count()


# In[468]:


# Final merged data 
dt_mrg= pd.merge(q1_prune, q1_date_update, on ='CNUM',how='left')


# In[469]:


dt_mrg.count()


# ## Importing sales revenue data 

# In[470]:


flm_rev = pd.read_excel('C:/Users/SuprasannaPradhan/Documents/DIA/PQ_ALL_Seller_Detail_041521.xlsx')
# flm_rev = pd.read_excel('users.xlsx', sheet_name = [0,1,2])


# In[471]:


flm_rev.head(2)


# ## Seperating Employee names from the  eamil id 

# In[472]:


# Seperating employee name from eemail id 
flm_rev[['EMP_FULL_NAME','COUNTRY_EMP','OTHER_EMP','NONE_EMP']] = flm_rev.Seller.str.split("/",expand=True)
# Seperating FLM  name from  eemail id 
flm_rev[['EMPLOYEE_MGR_L1_NAME ','COUNTRY_MGR','OTHER_MGR']] = flm_rev.FLM.str.split("/",expand=True)


# In[473]:


flm_rev.info()


# ## Subset of revenue data 

# In[474]:


q1_rev = flm_rev.iloc[ : , [21,10,7,9,2,3,25]] 


# In[475]:


q1_rev["EMP_FULL_NAME"] = q1_rev["EMP_FULL_NAME"].str.upper()


# In[476]:


q1_rev.head()


# In[477]:


q1_rev.count()


# ## Data set for call duration 

# In[478]:


dt_grp = dt_mrg.groupby(['EMP_FULL_NAME']).sum()['DURATION'].reset_index()
dt_grp.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/dt_grp.csv', index = False, header=True)


# In[479]:


# # dropping ALL duplicte values
# dt_grp.sort_values("EMP_FULL_NAME", inplace = True) 
# dt_grp.drop_duplicates(subset ="EMP_FULL_NAME",
#                      keep = False, inplace = True)


# In[480]:


dt_grp.head(2)


# In[490]:


cn_grp = dt_mrg.pivot_table(index=['CNUM','EMP_FULL_NAME','MONTH','WEEK'],values=['DURATION'], aggfunc='sum')
cn_grp = cn_grp.reset_index() 
cn_grp['Call_Hours'] =(cn_grp['DURATION']/60)
cn_grp= cn_grp.sort_values('Call_Hours',ascending=False).reset_index(drop=True)


# In[491]:


cn_grp.head()


# ## Data set for number of calls

# In[382]:


q1_grp = dt_mrg.pivot_table(index=['EMP_FULL_NAME'], values=['DURATION'], aggfunc='count')
q1_grp = q1_grp.reset_index() 
q1_grp = q1_grp.rename(columns={'DURATION': 'Number_Of_Calls'})


# In[383]:


q1_grp.head(10)


# In[384]:


dt_grp=pd.merge(dt_grp,q1_grp,on='EMP_FULL_NAME',how='left')


# In[385]:


dt_grp.head()


# In[386]:


# # Creating the merging ID: this column is created with combination of Revenue and call duraton data ,
# dt_rev['MERGING_ID'] = dt_rev['EMP_FULL_NAME'].map(str) + dt_rev['EMPLOYEE_MGR_L1_NAME'].map(str)
# dt_rev['MERGING_ID'] = dt_rev['EMP_FULL_NAME'].map(str) + dt_rev['EMPLOYEE_MGR_L1_NAME'].map(str)


# In[387]:


#merging revenue dataset 
dt_rev=pd.merge(dt_grp,q1_rev,on='EMP_FULL_NAME',how='left',indicator=True)
dt_sale = pd.merge(q1_grp,q1_rev ,on='EMP_FULL_NAME',how='left',indicator=True)


# In[388]:


# dropping all duplicte values of names
dt_rev.sort_values("EMP_FULL_NAME", inplace = True) 
dt_rev.drop_duplicates(subset ="EMP_FULL_NAME",
                     keep = False, inplace = True)


# In[389]:


dt_rev.count()


# ## Call hours and sales revenue for period of 1st quarter(2021-01-01 to 2021-03-31)

# In[390]:


# Checking data set
dt_rev.info()


# In[391]:


# Change columon name 
dt_rev = dt_rev.rename(columns={'EMP_FULL_NAME': 'SELLER','Val Pipe$':'REVENUE','Sub Brand':'Sub_Brand','DURATION':'Call_Minutes'})


# ## Converting to numberic and creating actual amount of revenue columon¶

# In[392]:


dt_rev['REV_AMT'] = pd.to_numeric(dt_rev['REVENUE'] *1000000, errors='coerce')
mask = dt_rev['REV_AMT'].isna()
dt_rev.loc[mask, 'Text'] = dt_rev.loc[mask,'REVENUE']
dt_rev['REV_AMT'] = dt_rev['REV_AMT'].replace(np.nan, 0)
dt_rev['Call_Hours'] =(dt_rev['Call_Minutes']/60)
dt_rev = dt_rev.drop(columns=['_merge','Text','REVENUE'])
dt_rev.info()


# In[393]:


get_ipython().run_cell_magic('HTML', '', '<style type="text/css">\ntable.dataframe td, table.dataframe th {\n    border: 1px  black solid !important;\n  color: black !important;\n}\n</style>')


# In[394]:


dt_rev.head()


# ##  Check Null values of revenue

# In[395]:


# let us chekc the Null vlaues 
check_null=dt_rev.isnull().sum()
check_null


# In[396]:


# #Replace with zero all Nan values
# dt_rev.replace('-', np.nan, inplace=True) 
# dt_rev['REVENUE'] = dt_rev['REVENUE'].replace(np.nan, 0)
# # dt_rev['CALLS_IN_MINUTES'] = dt_rev['CALLS_IN_MINUTES'].replace(np.nan, 0)


# In[397]:


# check_null=dt_rev['REVENUE'].isnull().sum()
# check_null


# In[398]:


dt_rev.head()


# ## Adding Productivity Levels

# In[399]:


def func(x):
   if x > 0:
       return 'Success'
   else:
       return 'Unsuccess'
dt_rev['Productivity'] = dt_rev['REV_AMT'].apply(func)
dt_rev.to_csv (r'C:/Users/SuprasannaPradhan/Documents/DIA/dt_rev.csv', index = False, header=True)


# In[400]:


dt_rev.head()


# ## Nomalizing Hours  and sales value 

# In[492]:


dt_rev['Call_Hours'] = (dt_rev['Call_Hours'] - dt_rev['Call_Hours'].min()) / (dt_rev['Call_Hours'].max() - dt_rev['Call_Hours'].min())    
# dt_rev['NOR_DURATION'] = (dt_rev['DURATION'] - dt_rev['DURATION'].min()) / (dt_rev['DURATION'].max() - dt_rev['DURATION'].min()) 


#    We have created to addtional columons with normalziation of revenue and hours

# ## Univariate analysis

# In[493]:


plt.figure(figsize=(10,8))
sns.pairplot(dt_rev,diag_kind= 'kde')


# ## Checking  Outlier

# In[494]:


plt.figure(figsize=(5,5))
dt_rev.boxplot(column="REV_AMT")


# ## Removing the outlier

# In[495]:


import numpy as np
for col in dt_rev.columns:
    percentiles = dt_rev['REV_AMT'].quantile([0.01, 0.99]).values
    dt_rev['REV_AMT'] = np.clip(dt_rev['REV_AMT'], percentiles[0], percentiles[1])


# In[496]:


plt.figure(figsize=(5,5))
dt_rev.boxplot(column="REV_AMT")


# In[545]:


plt.figure(figsize=(5,5))
dt_rev.boxplot(column="Call_Hours")


# In[546]:


dt_count = dt_rev.pivot_table(index=['Productivity'], values=['Number_Of_Calls'], aggfunc='sum')
dt_count = dt_count.sort_values('Number_Of_Calls',ascending=False).reset_index() 
dt_count


# In[547]:


# count plotof win and lost
# plt.style.use('fivethirtyeight')
dt_rev['Productivity'].hist()
plt.xlabel('Productivity')
plt.ylabel('Count')
plt.title('Productivity v/s COUNT')


# ## Bivariate analysis

# In[548]:


dt_dur = dt_rev.pivot_table(index=['Productivity'], values=['Number_Of_Calls'], aggfunc='sum')
# dt_dur = dt_dur.sort_values('HOURS',ascending=False).reset_index() 
dt_dur


# In[549]:


q1_win = dt_rev.groupby("Productivity")["Number_Of_Calls"].sum()
# data.plot.pie(autopct="%.1f%%");
# Using matplotlib
pie, ax = plt.subplots(figsize=[8,5])
labels = q1_win.keys()
plt.pie(x=q1_win, autopct="%.1f%%", explode=[0.05]*2, labels=labels, pctdistance=0.5)
plt.title("Productivity % by Number of Calls made for Qurter 2021", fontsize=14);
pie.savefig("q1GeoPieChart.png")


# ## Scatter plot - REVENUE by Number of Calls

# In[550]:


fig, ax = plt.subplots(figsize=(10,8))
ax.scatter(dt_rev['Number_Of_Calls'], dt_rev['REV_AMT'])
ax.set_xlabel('Number of call made for 1st quarter of 2021')
ax.set_ylabel('Revenue for 1st quarter of 2021')
plt.show()


# ## Line plot - HOURS Vs REVENUE

# In[551]:


plt.figure(figsize=(10,8))
sns.lineplot(x="REV_AMT", y="Call_Hours", data=dt_rev)
plt.show()


# ## Revenue Vs Revenue  by Productivity

# In[552]:


# Plot
plt.figure(figsize=(10,8))
sns.scatterplot(data=dt_rev, x="Call_Hours", y="REV_AMT", hue="Productivity", palette="deep")


# In[556]:


# Plot
plt.figure(figsize=(10,8))
sns.scatterplot(data=dt_rev, x='Number_Of_Calls', y="REV_AMT", hue="Productivity", palette="deep")


# ## Checking Win/Lost  by Duratioin 

# In[557]:


plt.figure(figsize=(10,8))
sns.boxplot(x="Productivity",y="Number_Of_Calls" ,data=dt_rev, palette="Set3")
fig.tight_layout()
plt.show()


# In[558]:


plt.figure(figsize=(10,8))
sns.boxplot(x="Productivity",y="Call_Hours" ,data=dt_rev, palette="Set3")
fig.tight_layout()
plt.show()


# In[559]:


# from sklearn.preprocessing import StandardScaler
# std_scale = StandardScaler()
# std_scale
# dt_rev['N_VAL_PIPE'] = std_scale.fit_transform(dt_rev[['N_VAL_PIPE']])


# ##  Anova one way

# In[560]:


formula = 'REV_AMT ~ (Number_Of_Calls)'
model = ols (formula,dt_rev).fit()
aov_tab =  anova_lm(model)
print(aov_tab)


# In[561]:


formula = 'REV_AMT ~ (Call_Hours)'
model = ols (formula,dt_rev).fit()
aov_tab =  anova_lm(model)
print(aov_tab)


# Assume in our case that we say no changes are impacted to call duration due these variables
# P value is here gater then  the 0.05 .
# 
# 
# 

# ## Anova two  way

# In[562]:


formula = 'REV_AMT ~ (Number_Of_Calls) + (Call_Hours)+ (Call_Minutes) + (Number_Of_Calls):(Call_Hours)'
model = ols (formula,dt_rev).fit()
aov_tab =  anova_lm(model,type=2)
print(aov_tab)


# Hereby we observed that no variables are having significant relationship with revenue 

# ## Pearson’s Correlation Coefficient

# In[563]:


from scipy.stats import pearsonr


# In[564]:


# # Apply the pearsonr()
list1 = dt_rev['REV_AMT']
list2 = dt_rev['Call_Hours']
stat,p = pearsonr(list1, list2)
print('stat=%.3f, p=%.3f'% (stat, p))

if p >0.05:
    print('Probably independent')
else:
    print('Probably dependent')


# ## Average /SD

# In[565]:


avg = dt_rev.describe().transpose()


# In[566]:


avg


# In[567]:


x=(2.74529e+06)
print("{:f}".format(x)) 


# In[568]:


dt_sum = dt_rev[['Call_Minutes','Number_Of_Calls','REV_AMT','Call_Hours']]
dt_sum.sum().reset_index()
# dt_sum.sum(axis = 0, skipna = True).reset_index()


# ## Covariance

# In[569]:


from numpy import cov

list1 = dt_rev['REV_AMT']
list2 = dt_rev['Number_Of_Calls']
covariance = cov(list1, list2)
print(covariance)


# A value of +1.00 would be a perfect (very strong) positive correlation

# ##  Standarad Correlation 

# In[570]:


corrMatrix = dt_rev.corr()
corrMatrix


# In[571]:


sns.heatmap(corrMatrix, annot=True)
plt.show()


# The value of 0.02 shows a positive but weak linear relationship between the two variables. Let’s confirm this with the linear regression correlation tes

# ## Liner Correlation

# In[572]:


## STATSMODELS ###
# create a fitted model
lm1 = smf.ols(formula='REV_AMT ~ Call_Hours', data=dt_rev).fit()
# print the coefficients
lm1.params


# In[573]:


from scipy.stats import linregress


# In[574]:


linregress(dt_rev['REV_AMT'], dt_rev['Number_Of_Calls'])


# In[575]:


linregress(dt_rev['REV_AMT'], dt_rev['Call_Hours'])


# In[576]:


### SCIKIT-LEARN ###
# create X and y
feature_cols = ['Call_Hours']
X = dt_rev[feature_cols]
y = dt_rev.REV_AMT
# instantiate and fit
lm2 = LinearRegression()
lm2.fit(X, y)
# print the coefficients
print(lm2.intercept_)
print(lm2.coef_)


# In[577]:


### STATSMODELS ###
# print the confidence intervals for the model coefficients
lm1.conf_int()


# The "true" coefficient is either within this interval or it isn't, but there's no way to actually know
# We estimate the coefficient with the data we do have, and we show uncertainty about that estimate by giving a range that the coefficient is probably within

# In[578]:


### STATSMODELS ###
# print the p-values for the model coefficients
lm1.pvalues


# In[579]:


### STATSMODELS ###
# print a summary of the fitted model
lm1.summary()


# if the p-value turns out to be less than 0.05, you can reject the null hypothesis and state that β1 is indeed significant.

# ## Adding dummie for Productivity

# In[580]:


dummies=pd.get_dummies(dt_rev[["Productivity"]],columns=["Productivity"],prefix=["Productivity"],drop_first=True).head()
columns=["Productivity"]
dt_rev = pd.concat([dt_rev,dummies],axis=1)


# In[581]:


dt_rev.head()


# In[582]:


q1_geo = dt_rev.groupby("Geo")["Number_Of_Calls"].sum()
q1_geo
# data.plot.pie(autopct="%.1f%%");
# Using matplotlib
pie, ax = plt.subplots(figsize=[5,5])
labels = q1_geo.keys()
plt.pie(x=q1_geo, autopct="%.1f%%", explode=[0.05]*4, labels=labels, pctdistance=0.5)
plt.title("Total Number_Of_Calls made by Geo for Qurter 2021", fontsize=14);
pie.savefig("q1GeoPieChart.png")


# In[583]:


dt_geo = dt_rev.pivot_table(index=['Geo'], values=['Number_Of_Calls'], aggfunc='sum')
dt_geo = dt_geo.sort_values('Number_Of_Calls',ascending=False).reset_index() 
dt_geo


# In[584]:


plt.figure(figsize=(15,8))
sns.catplot(y="Geo", hue="Productivity", kind="count",palette="pastel", edgecolor=".6",data=dt_rev)


# In[585]:


dt_gct = dt_rev.pivot_table(index=['Geo'], values=['Productivity'], aggfunc='count')
dt_gct = dt_gct.sort_values('Productivity',ascending=False).reset_index() 
dt_gct


# In[586]:


# plt.figure(figsize=(8,8))
sns.barplot(x='Geo', y= 'Number_Of_Calls',data=dt_rev,hue='Productivity',ci=None)


# In[587]:


dt_gct = dt_rev.pivot_table(index=['Productivity','Geo'], values=['Number_Of_Calls'], aggfunc='sum')
dt_gct = dt_gct.sort_values('Number_Of_Calls',ascending=False).reset_index() 
dt_gct.head(10)


# In[588]:


dt_gct = dt_rev.pivot_table(index=['Productivity','Geo'], values=['Call_Hours'], aggfunc='sum')
dt_gct = dt_gct.sort_values('Call_Hours',ascending=False).reset_index() 
dt_gct.head(10)


# In[589]:


q1_mkt = dt_rev.groupby('Mkt').sum()['Number_Of_Calls'].reset_index()
q1_mkt = q1_mkt.sort_values('Number_Of_Calls',ascending=False).reset_index(drop=True)
q1_mkt.head(10)


# In[590]:


mkt = q1_mkt['Mkt'].head(12)
dur = q1_mkt['Number_Of_Calls'].head(12)
# Figure Size
fig, ax = plt.subplots(figsize =(12, 8)) 
# Horizontal Bar Plot
ax.barh(mkt, dur)
# Remove axes splines
for s in ['top', 'bottom', 'left', 'right']:
    ax.spines[s].set_visible(False)

# Remove x, y Ticks
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')
# Add padding between axes and labels
ax.xaxis.set_tick_params(pad = 5)
ax.yaxis.set_tick_params(pad = 15)
# Add x, y gridlines
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)
# Show top values 
ax.invert_yaxis()
# Add annotation to bars
for i in ax.patches:
    plt.text(i.get_width()+0.2, i.get_y()+0.5,
             str(round((i.get_width()), 2)),
             fontsize = 10, fontweight ='bold',
             color ='grey')
# Add Plot Title
ax.set_title('Number of calls by Market  ',
             loc ='left', )
# Add Text watermark
fig.text(0.9, 0.15, 'Jeeteshgavande30', fontsize = 12,
         color ='grey', ha ='right', va ='bottom',
         alpha = 0.5)
# Show Plot
plt.show()


# In[591]:


# Mkt  wisn and lost
plt.figure(figsize=(6,10))
sns.countplot(y ='Mkt', hue = "Productivity", data = dt_rev)
# Show the plot
plt.show()


# In[592]:


# Mkt Hours with win and lost
plt.figure(figsize=(12,5))
sns.pointplot(x='Mkt', y= 'Number_Of_Calls',data=dt_rev,hue='Productivity',ci=None)


# In[593]:


# Segment wise win and lost 
sns.pointplot(x='Segment', y= 'Call_Hours',data=dt_rev,hue='Productivity',ci=None)


# In[594]:


dt_win = dt_rev.pivot_table(index=['Productivity','SELLER'], values=['Call_Hours'], aggfunc='sum')
dt_win = dt_win.sort_values('Call_Hours',ascending=False).reset_index() 


# In[595]:


dt_win.head(10)


# ![image-3.png](attachment:image-3.png)
# 
