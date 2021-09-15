# Is Singapore’s annual fertility rate less affected by marriages?

Introduction
------------------------------------------------
To investigate the looming population issues that Singapore faces, the Singapore government identifies the unwillingness to settle down or lack of marriages as a cause for plummeting fertility rates in the country. We aim to verify the cause of low fertility rates in Singapore by examining the association between marriages in Singapore and fertility rates. Using a combination of linear regression and ratio analysis, we derive two measures of correlations to gauge different aspects of the relationship between marriage and fertility in Singapore. The findings reveal that the relationship between marriage and fertility are still functional but not as relevant as before.

Metrics computed and used in this research:
1. Coefficient of correlation
2. Ratio of % Change in Fertility Rate to % Change in Marriage Rates

Datasets
------------------------------------------------
The first dataset used for this research study was ‘Marriage Rates, Annual’ from Singapore’s Department of Statistics. It is a CSV formatted file detailing the marriage rate in Singapore for both genders and the crude marriage rate from 1980 to 2017. The marriage rates in this dataset refers to the percentage of Singaporean male or female married for every 1,000 unmarried Singaporeans in a year.

In this research, we will be using marriage rates for male and females only for the independent variable of marriages. The variable ‘crude marriage rates’ was not utilised because it was calculated based on resident marriages where both the groom and brides are Singapore residents. Including crude marriages would narrow our definition of marriages in this study as it only reflects a sample rather than the entire Singaporean population. Hence, we will only use male and female marriage rates only to prevent any distortion of our study results.

The second dataset for this research study was ‘Births and Fertility Rates, Annual’ from Singapore’s Department of Statistics. It is also another CSV formatted file which includes data of the annual number of live-births and total fertility rate dated from 1960 to 2017. 

In this research, we used the variables ‘Total Fertility Rate’ and ‘Net Reproduction Rate’ to reflect the dependent variable ‘annual fertility rate’. Total Fertility Rate is the number of live births per female in their reproductive years.Net Reproduction Rate refers to the average number of daughters born per female in their reproductive years.Both datasets were read into data frames using pandas function, pandas.read_csv() and cleaned accordingly. Both datasets also have years from 1980 to 2017 marked as columns and the years can be common feature to merge both datasets. The treatment of the datasets will be further elaborated in the data cleaning segment of this report.

Both datasets were sourced from https://www.singstat.gov.sg/ on September 2018.
