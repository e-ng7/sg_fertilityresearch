#Research Question: Is Singapore's fertility rate less affected by marriages?
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#THIS IS THE FIRST DATASET IN DATAFRAME DF1
#Using pandas function read_csv, I read my first dataset ‘Marriage Rates, Annual’ and included other parameters.
#skiprows is to remove the unnecessary columns and rows written by Singapore Department of Statistics
df = pd.read_csv('marriages.csv', skiprows = 4, index_col = 0)
df = df.drop(df.index[22 : 26])
df = df[~df.isin(['NaN']).any(axis = 'columns')] #Here I used isin and ~df to remove any NaN columns

#After loading my dataset and removing the unnecessary data, I proceeded to create my dataframe
#I used df.loc to indicate the rows I wanted to use for my dataframe like Male General Marriage Rate and Female General Marriage Rate
df = df.loc[[' Male General Marriage Rate (Per 1,000 Unmarried Resident Males 15-49) ',
' Female General Marriage Rate (Per 1,000 Unmarried Resident Females 15-49) ']]
#Then I renamed the dataframe indexes that I chose because the original names in the csv files were too long
df = df.rename(index = {' Male General Marriage Rate (Per 1,000 Unmarried Resident Males 15-49) ' : 'Marriage Rates (Males)'})
df = df.rename(index = {' Female General Marriage Rate (Per 1,000 Unmarried Resident Females 15-49) ' : 'Marriage Rates (Females)'})
df = df.T #I transpose the dataframe to make the years e.g. 1985 the index and the Marriage Rates the columns in the dataframe
df = df.reset_index().rename(columns={'Years': [df.index]})
#I reset the index back to the original indexes so a common df index will be recognised when I concatenate later with my second dataset
#The two datasets would be combined with the years as a common index

#THIS IS THE 2ND DATASET IN DATAFRAME DF2
#I read my second dataset 'Births and Fertility Rates, Annual' with similar data cleaning because the dataset was from the same source
#and had the same unnecessary headers.
df2 = pd.read_csv('birth_fertility_rates.csv', skiprows = 4, index_col = 0)
df2 = df2.drop(df2.index[22 : 26])
#In this dataset, the time series was from 1960 to 2017.
#Since the first dataset of marriages does not have any data from 1960 to 1979, the timeline for this research study will begin from 1980 to 2017.
#Therefore, we remove the first 20 years in this dataset of fertility rates by using the df2.drop()
df2 = df2.drop(df2.columns[0 : 20], axis = 1)
df2 = df2.drop(df2.columns[-1], axis = 1) #Remove additional unnamed column that brings no value to the study
df2 = df2[~df2.isin(['NaN']).any(axis = 'columns')]
df2 = df2.loc[[' Total Fertility Rate (Per Female) ', ' Net Reproduction Rate (Per Female) ']]
#Likewise to the first dataset, I choose the index or rows I want from this dataset for my dataframe df2 and transpose the dataframe
df2 = df2.T
df2 = df2.reset_index().rename(columns={'Years': [df.index]})

#I combine both datasets into one dataframe by using pandas concatenate into a third dataframe (df3).
#Upon concatenating both dataframes df and df2, I clean the new dataframe df3
df3 = pd.concat([df, df2], axis = 1, sort = False, join_axes = [df.index])
#Using df3.columns, I rename the columns of df3 as there are two 'index' columns and I need to remove one index.
#I renamed the duplicated index column as index2 so pandas could recognise it as a duplicate when I drop it.
#After renaming the columns, I select the columns I want in df3
df3.columns = ['index','Marriage Rates (Males)','Marriage Rates (Females)','index2',' Total Fertility Rate (Per Female) ', ' Net Reproduction Rate (Per Female) ']
df3 = df3.loc[:, ['index','Marriage Rates (Males)','Marriage Rates (Females)',' Total Fertility Rate (Per Female) ', ' Net Reproduction Rate (Per Female) ']]
#Dataframe df3 is the full dataframe of all the dataset used.
#I duplicated df3 to create another dataframe dfmain slicing away years to create a 5 years interval between timeseries of dataframe
dfmain = df3.loc[::5, ['index','Marriage Rates (Males)','Marriage Rates (Females)',' Total Fertility Rate (Per Female) ', ' Net Reproduction Rate (Per Female) ']]
#I changed the data types of all values in the dataframes df3 and dfmain with pd.to_numeric to ensure they are suitable for other functions like corr() and mean()
dfmain = dfmain.apply(pd.to_numeric, errors = 'coerce')
df3 = df3.apply(pd.to_numeric, errors = 'coerce')
df3 = df3.set_index(['index'])
dfmain = dfmain.set_index(['index'])
#I use the pandas function .corr() to calculate the coefficient of correlation of the entire dataframe df3 to find the correlation between variables for the timeline 1980 to 2017
df_correlation = df3.corr()
#I also calculated the mean of the dataframe to benchmark the results later
df3_mean = df3.mean()
#In my Sensitivity Analysis, I calculate the ratio of changes in marriage rates against the changes in fertility rates to measure the strength of correlation every 5 years.
#I first calculate the changes in variables over the period using the .astype(float) ensure all data in the dataframe are suitable for function .diff()
#With parameter periods = 1, I subtract the marriage rate in year 1980 from the rate in year 1985 to find the % change over the 5 year period
dfmain['% Change in Marriage Rates (M)'] = dfmain['Marriage Rates (Males)'].astype(float).diff(periods = 1)
dfmain['% Change in Marriage Rates (F)'] = dfmain['Marriage Rates (Females)'].astype(float).diff(periods = 1)
dfmain['% Change in Total Fertility Rate'] = dfmain[' Total Fertility Rate (Per Female) '].astype(float).diff(periods = 1)
dfmain['% Change in Net Reproduction Rate'] = dfmain[' Net Reproduction Rate (Per Female) '].astype(float).diff(periods = 1)

#Using iloc, I proceed to slice the main dataframe dfmain, into two new dataframes df4 andf df5 because they hold different values
#df4 retains the original dataset values and df5 has the % changes in variables over the years
df3.index.name = 'Year'
dfmain.index.name = 'Year'
df4 = dfmain.iloc[:, :4]
df5 = dfmain.iloc[:, 4:]
#I complete the ratio calculation by dividing the calculated % changes in fertility rate over the % changes in marriage rates to derive the ratio
#The computed ratios are added into dataframe df5 as absolute values
df5['Times Change in Fertility for 1% Male Marriage'] = (df5['% Change in Total Fertility Rate']/df5['% Change in Marriage Rates (M)'] *10).abs()
df5['Times Change in Fertility for 1% Female Marriage'] = (df5['% Change in Total Fertility Rate']/df5['% Change in Marriage Rates (F)'] *10).abs()

#Again, I split the dataframe df5 into two new dataframes df6 and df7 to separate my ratios for sensitivity analysis
df6 = df5.iloc[:, :4]
df7 = df5.iloc[:, 4:]

#Here, I print all my data frames out
print("\nCoefficient of Correlation between Variables from 1980 to 2017:")
print("=" * 150)
print(df_correlation)
print("\nMean of Variables:")
print("=" * 50)
print(df3_mean)
print(df4)
print("\nSensitivity Analysis")
print('=' * 120)
print(df6)
print(df7)

# Plotting subplot visual representations of the trend analysis for both Marriage Rates and Fertility Rates
#I first create the main figure plot
fig = plt.figure(figsize = (20, 15))
fig.suptitle("Is Singapore's fertility rate less affected by marriages?", fontsize=16) #I place the research question as my main title

#This is the first subplot that shows the trend of decrasing fertility rates over the years from 1980 to 2017
sfg = fig.add_subplot(221)
sfg.axhline(df3_mean[' Total Fertility Rate (Per Female) '], color = 'black', linewidth = 3, label = 'Mean')
df3[[' Total Fertility Rate (Per Female) ']].plot(kind='bar', title ="Fertility Rates", figsize=(15, 10), legend=True, fontsize=12, ax=sfg, color = 'pink',)
df3[[' Net Reproduction Rate (Per Female) ']].plot(kind='bar', title ="Fertility Rates", figsize=(15, 10), legend=True, fontsize=12, ax=sfg, color = 'grey')

#This is the second subplot that shows the trend of decreasing marriage rates over the years from 1980 to 2017
sfg2 = fig.add_subplot(222)
df3[['Marriage Rates (Females)']].plot(kind='line', title ="Marriage Rates", figsize=(15, 10), legend=True,
fontsize = 12, ax = sfg2, marker = 'o', markerfacecolor = 'black', color = 'navy', use_index = True, grid = True)
df3[['Marriage Rates (Males)']].plot(kind='line', title ="Marriage Rates", figsize=(15, 10), legend=True,
fontsize = 12, ax = sfg2, marker = 'o', markerfacecolor = 'gold', color = 'red', grid = True)

#This is the third subplot of a scatter plot showing the association between marriage and fertility rates
sfg3 = fig.add_subplot(223)
plt.title("Correlation between Fertility & Marriage")
plt.scatter([df3['Marriage Rates (Males)']], [df3[' Total Fertility Rate (Per Female) ']], label = 'Male Marriage Rates', color ='green')
plt.scatter([df3['Marriage Rates (Females)']], [df3[' Total Fertility Rate (Per Female) ']],
 color ='red', marker = "x", label = 'Female Marriage Rates')
plt.legend(loc = 'best', fontsize = 12)
plt.xlabel('Marriage Rates')
plt.ylabel('Fertility Rates')

#This is the fourth subplot illustrating the change in ratios over the years
sfg4 = fig.add_subplot(224)
df7[['Times Change in Fertility for 1% Male Marriage']].plot(kind='line', title ="Sensitivity Analysis", figsize=(15, 10), legend=True,
fontsize = 12, ax = sfg4, marker = 'o', markerfacecolor = 'black', color = 'skyblue', use_index = True, grid = True)
df7[['Times Change in Fertility for 1% Female Marriage']].plot(kind='line', figsize=(15, 10), legend=True,
fontsize = 12, ax = sfg4, marker = 'X', markerfacecolor = 'grey', color = 'black', use_index = True, grid = True)
plt.subplots_adjust(hspace=0.45)
plt.show()
