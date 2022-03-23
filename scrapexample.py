import requests
from bs4 import BeautifulSoup
import re
import pandas 
import numpy as np

#scrape pages for weeks 1-17
search=[]
base_url="https://www.fantasypros.com/nfl/stats/qb.php?ownership=y&range=week&week="
for page in range(1,18):
    print(base_url+str(page))
    r=requests.get(base_url+str(page))
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    sts = soup.find_all("tr", re.compile("mpb-player-"))
    for item in sts:
        g={}
        g['Week']=page
        g['PlayerName']=item.find_all("a", {'class':'player-name'})[0].text
        g['Completions']=item.find_all('td', {'class':'center'})[0].text
        g['Passing Attempts']=item.find_all('td', {'class':'center'})[1].text
        g['Completion %']=item.find_all('td', {'class':'center'})[2].text
        g['Passing Yds']=item.find_all('td', {'class':'center'})[3].text
        g['Yds Per Attempt']=item.find_all('td', {'class':'center'})[4].text
        g['Passing TDs']=item.find_all('td', {'class':'center'})[5].text
        g['Interceptions']=item.find_all('td', {'class':'center'})[6].text
        g['Sacks Taken']=item.find_all('td', {'class':'center'})[7].text
        g['Rushing Attemps']=item.find_all('td', {'class':'center'})[8].text
        g['Rushing Yds']=item.find_all('td', {'class':'center'})[9].text
        g['Rushing TDs']=item.find_all('td', {'class':'center'})[10].text
        g['Fumbles']=item.find_all('td', {'class':'center'})[11].text
        search.append(g)

#create Dataframe from 'search' data
df=pandas.DataFrame(search)

#convert columns to float
df.iloc[:, 2:]=df.iloc[:,2:].astype(float)
df.dtypes

#Apply scoring settings to stats and create new column to tabulate 
df['Fantasy Scoring'] = (df['Completions'] * 0.2) - ((df['Passing Attempts'] - df['Completions']) * 0.1)  + (df['Passing Yds'] * 0.05) + (df['Passing TDs'] * 6) - (df['Interceptions'] * 3) - (df['Sacks Taken'] * 0.2) + (df['Rushing Attemps'] * 0.1) + (df['Rushing Yds'] * 0.1) + (df['Rushing TDs'] * 6) - (df['Fumbles'] * 4)
df.loc[df['Passing Yds'] >= 350, 'Fantasy Scoring'] = df['Fantasy Scoring'] + 3
df.loc[df['Passing Yds'] >= 450, 'Fantasy Scoring'] = df['Fantasy Scoring'] + 10
df.loc[df['Rushing Yds'] >= 100, 'Fantasy Scoring'] = df['Fantasy Scoring'] + 3
df.loc[df['Rushing Yds'] >= 200, 'Fantasy Scoring'] = df['Fantasy Scoring'] + 10

#replace 0's with NaN 
df.replace(0, np.nan, inplace=True)

#Calculate numbers
Number_games = df.groupby(['PlayerName'])['Fantasy Scoring'].count()
Total_Fantasy = df.groupby(['PlayerName'])['Fantasy Scoring'].sum()
Avg_Fantasy = df.groupby(['PlayerName'])['Fantasy Scoring'].mean()
STD_Fantasy = df.groupby(['PlayerName'])['Fantasy Scoring'].std()
min_Fantasy = df.groupby(['PlayerName'])['Fantasy Scoring'].min()
max_Fantasy = df.groupby(['PlayerName'])['Fantasy Scoring'].max()
Quartile1 = df.groupby(['PlayerName'])['Fantasy Scoring'].quantile(.25)
Quartile3 = df.groupby(['PlayerName'])['Fantasy Scoring'].quantile(.75)
IQR = Quartile3 - Quartile1

#create new dataframe for cumulative numbers from above 
dfqb1 = pandas.concat([Number_games, Total_Fantasy, Avg_Fantasy,STD_Fantasy, min_Fantasy, max_Fantasy, Quartile1, Quartile3, IQR], axis=1)
dfqb1.columns = ['Games Played', 'Total Scoring', 'Average', 'STD', 'Minimum', 'Maximum', 'Quartile 1', 'Quartile 3', 'IQR']
dfqb1.to_csv(r"C:\...\qbfantasy2021.csv")

#Only keep QBs with 10 games or more to keep relevant players only
dfqb1 = dfqb1[dfqb1.Games>=10]

#Round Average score values to nearest whole number for easier comparisons between players of similar averages 
dfqb1.Average = dfqb1.Average.round() 
dfqb1.IQR = dfqb1.IQR.round(1)

#Sort values by average column and then IQR & create rankings file
dfqb1 = dfqb1.sort_values(['Average', 'IQR'], ascending=[False, True])
dfqb1 = dfqb1.drop(['STD','Minimum','Maximum','Quartile 1','Quartile 3'], 1)
dfqb1['Ranking'] = dfqb1['Average'].rank(ascending=False)
columnmove = dfqb1.pop('Ranking')
dfqb1.insert(0,'Ranking',columnmove)

#Save files as CSV and HTML table
dfqb1.to_csv(r"C:\...\qbranks2021.csv", encoding='utf-8', index=False)
dfqb1.to_html(r"C:\...\qbranks2021.html", index=False)

